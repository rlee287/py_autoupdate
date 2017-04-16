from __future__ import absolute_import, print_function

from datetime import datetime
from logging import WARNING
import multiprocessing
import os
import pprint
import re
import shutil
from sys import version_info
import tempfile
import warnings

# Module in different place depending on python version
if version_info[0]==2: # pragma: no branch
    from urlparse import urlparse,urlunparse
else:
    from urllib.parse import urlparse, urlunparse

from pkg_resources import parse_version, SetuptoolsVersion, PEP440Warning
from setuptools.archive_util import unpack_archive, UnrecognizedFormat

import requests

from ._file_glob import copy_glob
from .exceptions import ProcessRunningException, CorruptedFileWarning


class Launcher(object):
    """Creates a :class:`Launcher` object.

    :param str filepath: Path to file to execute
    :param str url: Base URL from which to download new versions

    .. note::
       This must be an HTTPS url. HTTP urls are silently changed into HTTPS.

       Parameters, queries, and fragments will be stripped from the URL.

    :param str newfiles: Name of archive with new versions to download from
     site
    :param int log_level: Logging level for the built in logger
    :param tuple args: ``args`` passed to the launched code
    :param dict kwargs: ``kwargs`` passed to the launched code

    .. note::

       The supported archive formats are ``.zip``, ``.tar.gz``,
       and ``.tar.bz2``.

    When the code is launched, certain variables are already defined as
    follows:

    +-------------+-------------------------------------------------+
    |Variable Name|Value Description                                |
    +=============+=================================================+
    |``filepath`` |Path to the file that was initially launched     |
    +-------------+-------------------------------------------------+
    |``url``      |Base url to check and download new versions      |
    +-------------+-------------------------------------------------+
    |``check_new``|Method to check for updated code                 |
    +-------------+-------------------------------------------------+
    |``pid``      |PID of parent process that spawns the code       |
    +-------------+-------------------------------------------------+
    |``log``      |Logger for Pyautoupdate and for the executed code|
    +-------------+-------------------------------------------------+
    |``args``     |``args`` tuple for the spawned code              |
    +-------------+-------------------------------------------------+
    |``kwargs``   |``kwargs`` dict for the spawned code             |
    +-------------+-------------------------------------------------+

    .. warning::

       The :class:`Launcher` uses :class:`multiprocessing.Process`
       to run the code.

       Please ensure that all ``args`` and ``kwargs`` can be pickled.
    """

    version_doc = "version.txt"
    version_check_log = "version_check.log"
    file_list = "filelist.txt"
    updatedir=".pyautodownloads"
    queue_update = ".queue"
    queue_replace = ".replace"

    def __init__(self, filepath, url,
                 newfiles='project.zip',
                 log_level=WARNING,
                 *args,**kwargs):
        self.log=multiprocessing.get_logger()
        self.log.setLevel(log_level)
        # Create handle to self.log only if necessary
        if len(self.log.handlers)==0:
            # Create handler to sys.stderr
            multiprocessing.log_to_stderr()
        self.log.info("Initializing launcher")
        self.log.debug("Validating files")

        # Check that self.version_doc is valid
        if not self.version_doc_validator():
            self.log.error("{0} does not have a valid version number!\n"
                           "{0} is a reserved file name.\n"
                           "It will be overwritten by this program!\n"
                           "If the {0} is corrupted,\n"
                           "Please use the logfile at {1} to restore it."
                           .format(self.version_doc,self.version_check_log))
            warnings.warn("{0} is corrupted!".format(self.version_doc),
                          CorruptedFileWarning,
                          stacklevel=2)

        # Check that self.version_log is valid
        open(self.version_check_log, 'a').close() # "Touch" self.version_log
        if not self.version_log_validator():
            self.log.warning("Log file at {0} is corrupted!\n"
                             "{0} is a reserved file name.\n"
                             "Please ensure that your program is "
                             "not using it.".format(self.version_check_log))
            warnings.warn("{0} is corrupted!"
                          .format(self.version_check_log),
                          CorruptedFileWarning,
                          stacklevel=2)

        self.log.debug("Validating arguments")
        # Check that filepath is specified
        if len(filepath) != 0:
            self.filepath = filepath
        else:
            raise ValueError("Filepath must not be empty")

        # Check that URL is specified
        if len(url) == 0:
            raise ValueError("URL must not be empty")
        self.url = url

        # URL parsing section
        schemaobj=urlparse(self.url)
        # Add https schema if necessary and replace http with https
        if schemaobj.scheme not in ["","https","http"]:
            raise ValueError("Url must be http or https")
        if schemaobj.scheme == "":
            self.url="https://"+self.url
            schemaobj=urlparse(self.url)
        # Intended behavior is to remove parameters, query, and fragment
        self.url=urlunparse(("https",schemaobj.netloc,schemaobj.path,
                             "","",""))
        # Append slash to end of URL if it is not present
        if not url.endswith("/"):
            self.url = self.url + "/"

        # Check for valid newfiles
        if len(os.path.normpath(newfiles).split(os.path.sep))>1:
            raise ValueError("newfiles should be a single archive name")
        elif not newfiles.endswith((".zip",".tar.gz",".tar.bz2")):
            raise ValueError("newfiles must be a zip, gzip, or bzip file")
        else:
            self.newfiles = newfiles

        # Initialize other variables
        self.update = multiprocessing.Lock()
        self.pid = os.getpid()
        self.args = args
        self.kwargs = kwargs
        self.__process = multiprocessing.Process(target=self._call_code,
                                                 args=self.args,
                                                 kwargs=self.kwargs)
        self.past_terminated=False
        self.__process_alive=multiprocessing.Event()
        assert not self.__process_alive.is_set()
        self.log.info("Launcher initialized successfully")

####################### Filename getters and validators ######################

    def version_doc_validator(self):
        """Validates the file containing the current version number.

        :return: Whether the version_doc is a proper version
        :rtype: bool
        """
        # Version is valid only if it exists
        version_valid=os.path.isfile(self.version_doc)
        if version_valid:
            try:
                # If statement earlier signifies that version file must exist
                with open(self.version_doc,"r") as version_check:
                    # Read and parse version
                    vers=version_check.read()
                    if len(vers)>0:
                        vers_obj=parse_version(vers)
                        if not isinstance(vers_obj,SetuptoolsVersion):
                            raise PEP440Warning
            except PEP440Warning: # Thrown if file has invalid version
                version_valid=False
        return version_valid

    def version_log_validator(self):
        """Validates the file containing the version history.

        :return: Whether the version_log is formatted properly
        :rtype: bool
        """
        valid_log=True
        # Match log file against regex
        with open(self.version_check_log,"r") as log_file:
            log_syntax=re.compile(
                r"Old .+?\|(New .+?|Up to date|Server invalid)\|Time .+?")
            version=log_file.read()
            if version!="\n" and len(version)>0:
                has_match=re.match(log_syntax,version)
                valid_log=bool(has_match)
        return bool(valid_log)

########################### Process manipulation #############################

    @property
    def process_is_alive(self):
        """Property indicating whether the process is alive"""
        return self.__process.is_alive()

    @property
    def process_code_running(self):
        """Property indicating whether the user code is alive

           .. note::
              This is diferent from ``Launcher.process_is_alive`` because the
              process takes time to start up before running the user code.
        """
        return self.__process_alive.is_set()

    @property
    def process_pid(self):
        """Property indicating the process PID, if it exists"""
        return self.__process.pid

    @property
    def process_exitcode(self):
        """Property indicating the process exitcode, if it exists"""
        if self.past_terminated:
            # SIGTERM is signal 15 on Linux
            # Preserve compatibility on Windows
            return -15
        else:
            return self.__process.exitcode

    def process_join(self,timeout=None):
        """Joins the process"""
        self.log.info("Joining process")
        self.__process.join(timeout)

    def process_terminate(self):
        """Terminates the process.

        .. warning::
           All the provisos of :meth:`multiprocessing.Process.terminate`
           apply.

           Attempts are made in the code to ensure that internal variables
           inside the Launcher class are properly cleaned up. However, there is
           little protection for user supplied code in case of termination.

        :return: Whether process was terminated
        :rtype: bool
        """
        # TODO: Troubleshoot xfail test
        if self.process_is_alive:
            self.log.warning("Terminating Process")
            self.__process.terminate()
            self.__process_alive.clear()
            # Release lock to avoid update deadlock later
            self.log.debug("Releasing code lock after termination")
            self.update.release()
            # Reinitialize process now because is_alive is not properly reset
            # After a process termination
            self.log.debug("Reinitializing process object after termination")
            self.__process = None
            self.__process = multiprocessing.Process(target=
                                                     self._call_code,
                                                     args=self.args,
                                                     kwargs=self.kwargs)
            self.past_terminated=True
            return True
        else:
            self.log.warning("Attempted to terminate dead process")
            return False

########################### Code execution methods ###########################

    def _call_code(self, *args, **kwargs):
        """Internal function to execute the user code.

           This is internally used as target of a
           :class:`multiprocessing.Process` instance.

           :param tuple args: ``*args`` tuple from self.args
           :param dict kwargs: ``**kwargs`` dict from self.kwargs

           .. warning::

              End users should never call this directly.
              Please use the :meth:`run` method instead.
        """
        # Open code file
        # Acquire lock here to avoid TOCTTOU issues with opened code file
        # multiprocessing.get_logger again since this is not pickleable
        local_log=multiprocessing.get_logger()
        local_log.debug("Acquiring code lock to run code")
        self.update.acquire()
        with open(self.filepath, mode='r') as code_file:
            code = code_file.read()
        localvar = vars(self).copy()
        # Manipulate __dict__ attribute to add handle to check_new
        localvar["check_new"] = self.check_new
        # Remove handle to process object and lock
        # Neither should not be tampered with in child process code
        del localvar["_Launcher__process"]
        del localvar["_Launcher__process_alive"]
        del localvar["update"]
        del localvar["past_terminated"]
        # Pass in args, kwargs, and logger
        localvar["args"]=args
        localvar["kwargs"]=kwargs
        localvar["log"]=local_log
        local_log.debug("Starting process with"
                        " the following local variables:\n"+
                        pprint.pformat(localvar))
        # Execute code in file
        local_log.info("Starting code from file")
        try:
            self.__process_alive.set()
            exec(code, dict(), localvar)
        finally:
            local_log.debug("Releasing code lock after running code")
            self.update.release()
            self.__process_alive.clear()
            # Reset past_terminated to False
            # (if terminated and rerun, past_terminated should be false)
            self.past_terminated=False

    def run(self, background=False):
        """Runs the user code.

           If background is ``False``, returns the Process's exitcode.

           :param bool background: Whether to run code in background

           :return: the exit code if background is ``False``
           :rtype: :class:`int` or :class:`None`
        """
        # Find the right error to raise depending on python version
        self.log.info("Checking file existence")
        try:
            error_to_raise=FileNotFoundError
        except NameError:
            error_to_raise=IOError
        if not os.path.isfile(self.filepath):
            raise error_to_raise("No file at {0}".format(self.filepath))
        self.log.info("Checking process status")
        if self.process_is_alive:
            self.log.error("Process is already running")
            raise ProcessRunningException
        elif self.process_pid is None:
            # Process has not run yet
            self.log.info("Process has not run yet")
            self.log.info("Starting process")
            # self.log is not pickleable
            # The variable will be reinstantiated inside _call_code
            # Temporarily remove here and reinstantiate after start
            del self.log
            try:
                self.__process.start()
            finally:
                self.log=multiprocessing.get_logger()
            self.log.info("Process started")
            if not background:
                self.process_join()
                # Exit code can be used by program that calls the launcher
                return self.process_exitcode
        elif self.process_exitcode is not None:
            # Process has already terminated
            # Reinitialize the process instance
            self.log.info("Process has already finished")
            self.log.info("Reinitializing process object")
            self.__process = multiprocessing.Process(target=
                                                     self._call_code,
                                                     args=self.args,
                                                     kwargs=self.kwargs)
            # Recursion, since this will reset @property properties
            self.run(background)
        else: # pragma: no cover
            # Should never happen
            self.log.error("Process exitcode exists without PID!")
            self.log.error("The application is probably in an unstable state.")

######################### New code retrieval methods #########################

    def check_new(self):
        """Retrieves the latest version number from the remote host.

           :return: Whether a newer version is available
           :rtype: bool

           .. note::
              This function internally uses setuptool's ``parse_version``
              to compare versions.

              Any versioning scheme described in :pep:`440` can be used.
        """
        self.log.info("Checking for updates")
        request_time=datetime.utcnow()
        # If self.queue_update is already present, return false
        # TODO: Check again?
        if os.path.isfile(self.queue_update):
            with open(self.queue_update, 'r') as new_version:
                newver=new_version.read()
            newver_obj=parse_version(newver)
            newver=newver.rstrip("\n")
            return isinstance(newver_obj,SetuptoolsVersion)
        else:
            versionurl=self.url+self.version_doc
            # Get new files
            self.log.debug("Retrieving new version from {0}"
                           .format(versionurl))
            get_new=requests.get(versionurl, allow_redirects=True)
            get_new.raise_for_status()
            newver=get_new.text
            newver=newver.rstrip("\n")
            newver_obj=parse_version(newver)
        # Read in old version
        with open(self.version_doc, 'r') as old_version:
            oldver=old_version.read()
        oldver=oldver.rstrip("\n")
        # Compare old version with new version
        invalid=not isinstance(newver_obj,SetuptoolsVersion)
        # Check if new version is valid
        if invalid:
            self.log.error("Retrieved version number is invalid!\n"
                           "Please contact the software authors.\n"
                           "Please include the generated data dump "
                           "in a bug report.")
            newver_dump=None
            # If invalid, dump into dump file
            try:
                newver_dump=tempfile.NamedTemporaryFile(prefix="newverdump",
                                                        delete=False,
                                                        mode="wt",
                                                        dir=os.getcwd())
                self.log.error("Writing invalid version into {0}"
                                   .format(newver_dump.name))
                newver_dump.write(newver)
            except Exception:
                self.log.exception("Unable to write data dump")
                raise
            finally:
                if newver_dump is not None:
                    newver_dump.close()

        if invalid:
            # Throw warning as error object after logging
            # If version is invalid, upgrade cannot succeed
            version_to_add="Old {0}|Server Invalid|Time {1}\n"\
                           .format(oldver,request_time)
            with open(self.version_check_log, "a") as log_file:
                log_file.write(version_to_add)
            raise CorruptedFileWarning

        # Will always return not new if new version is invalid
        has_new=(newver_obj>parse_version(oldver))
        # Add entry to the logfile and update version.txt
        if has_new:
            version_to_add="Old {0}|New {1}|Time {2}\n"\
                           .format(oldver,newver,request_time)
            with open(self.queue_update, 'w') as new_version:
                new_version.write(newver)
        else:
            version_to_add="Old {0}|Up to date|Time {1}\n"\
                           .format(oldver,request_time)
        with open(self.version_check_log, "a") as log_file:
            log_file.write(version_to_add)
        return has_new

    def _reset_update_files(self):
        """Resets the update directory to its default state.

           It also creates a new update directory if one doesn't exist.
        """
        self.log.debug("Resetting update directory")
        if os.path.isdir(self.updatedir):
            # Remove old contents
            shutil.rmtree(self.updatedir)
        # Make new empty directory
        # shutil.rmtree would have deleted the directory
        os.mkdir(self.updatedir)
        # Remove old archive
        if os.path.isfile(self.newfiles):
            os.remove(self.newfiles)

    def _get_new(self, allow_redirects=True, chunk_size=512):
        """Retrieves the new archive and extracts it to self.updatedir."""
        self.log.info("Retrieving new version")
        newurl = self.url+self.newfiles
        # Get new files
        http_get = requests.get(newurl, stream=True,
                                allow_redirects=allow_redirects)
        http_get.raise_for_status()
        with open(self.newfiles, 'wb') as filehandle:
            for chunk in http_get.iter_content(chunk_size=chunk_size):
                if chunk:
                    filehandle.write(chunk)
        # Unpack archive and remove it after extraction
        try:
            self.log.info("Unpacking downloaded archive")
            unpack_archive(self.newfiles, self.updatedir)
        except UnrecognizedFormat:
            self.log.error("Retrieved version archive is invalid!\n"
                           "Please contact the software authors.\n"
                           "Please include the invalid archive "
                           "in a bug report.")
            os.rename(self.newfiles,self.newfiles+".dump")
        else:
            # Remove archive only if unpack operation succeeded
            self.log.info("Removing archive after extraction")
            os.remove(self.newfiles)
            # Signal that update is ready
            self.log.debug("Creating downloaded file marker")
            open(self.queue_replace,"w").close()

    def _replace_files(self):
        """Replaces the existing files with the downloaded files.

           :return: Whether update succeeded
           :rtype: bool
        """
        # Only replace if update and replacement are queued
        if not (os.path.isfile(self.queue_update) and
                os.path.isfile(self.queue_replace)):
            return False
        # Attempt to acquire code lock here and exit if unable to
        # The finally block runs after the "return" statement
        # This can cause a double-release under some circumstances
        # Acquiring the lock here prevents this from happening
        else:
            self.log.debug("Acquiring code log to update files")
            has_lock=self.update.acquire(False)
            if not has_lock:
                self.log.warn("Could not acquire lock to update files")
                return False
        try:
            # else (os.path.isfile(self.queue_update) and
            # os.path.isfile(self.queue_replace))
            # TODO: Make this code safer and possibly leave diagnostics
            # if the update operation errors out in the middle
            self.log.debug("Writing new version into {0}"
                           .format(self.version_doc))
            os.rename(self.version_doc,self.version_doc+".bak")
            os.rename(self.queue_update,self.version_doc)
            os.remove(self.version_doc+".bak")
            self.log.debug("Removing downloaded file marker")
            os.remove(self.queue_replace)
            self.log.info("Replacing files")
            # Read in files from filelist and move to tempdir
            tempdir=tempfile.mkdtemp()
            self.log.debug("Created tempdir at {0}".format(tempdir))
            self.log.info("Backing up current filelist")
            filelist_backup=None
            try:
                filelist_backup=tempfile.NamedTemporaryFile(delete=False)
                with open(self.file_list, "r+b") as file_handle:
                    shutil.copyfileobj(file_handle,filelist_backup)
            except Exception:
                self.log.exception("Backup of current filelist failed!")
                raise
            finally:
                if filelist_backup is not None:
                    filelist_backup.close()
            self.log.info("Moving old files to tempdir")
            with open(self.file_list, "r") as file_handle:
                for line in file_handle:
                    file_rm=os.path.normpath(os.path.join(".",line))
                    file_rm=file_rm.rstrip("\n")
                    # Confirm that each file in filelist exists
                    if not os.path.isfile(file_rm):
                        self.log.error("{0} contains the invalid "
                                       "filepath {1}.\n"
                                       "Please check that {0} is not being "
                                       "used!\n"
                                       "Otherwise the {0} is corrupted.\n"
                                       "Updates will fail until this is "
                                       "restored."
                                       .format(self.file_list,file_rm))
                        warnings.warn("{0} is corrupted and contains the "
                                      "invalid path {1}!"
                                      .format(self.file_list,file_rm),
                                      CorruptedFileWarning,
                                      stacklevel=2)
                    else:
                        file_rm_temp=os.path.join(tempdir,file_rm)
                        file_rm_temp_dir=os.path.dirname(file_rm_temp)
                        if not os.path.isdir(file_rm_temp_dir):
                            # exist_ok does not exist in Python 2
                            os.makedirs(file_rm_temp_dir)
                        if file_rm.split(os.path.sep)[0] not in \
                                                [self.updatedir,
                                                 self.version_doc,
                                                 self.version_check_log]:
                            self.log.debug("Moving {0} to {1}".format(file_rm,
                                                                      tempdir))
                            shutil.move(file_rm,file_rm_temp)
                            file_rm_dir=os.path.dirname(file_rm)
                            if os.path.isdir(file_rm_dir):
                                if not os.listdir(file_rm_dir):
                                    os.rmdir(file_rm_dir)
                                    self.log.debug("Removing directory {0}"
                                                   .format(file_rm_dir))
            self.log.info("Removing old filelist")
            os.remove(self.file_list)
            self.log.info("Creating new filelist")
            filelist_new=list()
            relpath_start=os.path.join(self.updatedir)
            for dirpath, _, filenames in os.walk(self.updatedir):
                # _ is dirnames, but it is unused
                for filename in filenames:
                    filepath=os.path.normpath(os.path.join(dirpath,
                                                           filename))
                    filepath=os.path.relpath(filepath,start=relpath_start)
                    filepath+="\n"
                    filelist_new.append(filepath)
            self.log.debug("New filelist is:\n"+pprint.pformat(filelist_new))
            self.log.info("Writing new filelist to {0}".format(self.file_list))
            with open(self.file_list, "w") as file_handle:
                file_handle.writelines(filelist_new)
            self.log.info("Copying downloaded contents to current directory")
            copy_glob(os.path.join(self.updatedir,"*"),".")
            self.log.info("Removing backup filelist")
            os.remove(filelist_backup.name)
            self.log.info("Removing tempdir")
            shutil.rmtree(tempdir)
        finally:
            self.log.debug("Releasing lock after updating files")
            self.update.release()
        return has_lock

    def update_code(self):
        """Updates the code if necessary.
           :return: Whether update succeeded
           :rtype: bool
        """
        if self.check_new():
            # self.check_new will create a self.queue_update file
            self.log.info("Beginning update process")
            if not os.path.isfile(self.queue_replace):
                self._reset_update_files()
                self._get_new()
            update_successful=self._replace_files()
            if update_successful:
                self._reset_update_files()
                self.log.info("Update successful")
            else:
                self.log.info("Update failed")
        else:
            self.log.info("Already up to date")
            update_successful=False
        return update_successful
