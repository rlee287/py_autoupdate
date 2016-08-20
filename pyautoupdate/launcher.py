from __future__ import absolute_import, print_function

from datetime import datetime
from logging import WARNING
import multiprocessing
import os
import pprint
import re
import shutil
import tempfile
import warnings

from pkg_resources import parse_version, SetuptoolsVersion, PEP440Warning
from setuptools.archive_util import unpack_archive

import requests

from ._move_glob import move_glob, copy_glob
from .exceptions import ProcessRunningException, CorruptedFileWarning

class Launcher(object):
    '''Creates a :class:`Launcher` object.

    :param str filepath: Path to file to execute
    :param str url: Base URL from which to download new versions
    :param str newfiles: Name of archive with new versions to download from
     site
    :param str updatedir: Directory in which new versions are downloaded into
    :param int log_level: Logging level for the built in logger
    :param list args: ``args`` passed to the launched code
    :param dict kwargs: ``kwargs`` passed to the launched code

    .. note::

       The archive can be a ``.zip``, ``.tar.gz``, or a ``.tar.bz2`` file.

    When the code is launched, certain variables are already defined as
    follows:

    +-------------+-------------------------------------------------+
    |Variable Name|Value Description                                |
    +=============+=================================================+
    |``filepath`` |Path to the file that was initially launched     |
    +-------------+-------------------------------------------------+
    |``url``      |Base url to check and download new versions      |
    +-------------+-------------------------------------------------+
    |``newfiles`` |Name of the archive containing the new files     |
    +-------------+-------------------------------------------------+
    |``updatedir``|Directory into which the new archive is extracted|
    +-------------+-------------------------------------------------+
    |``update``   |:class:`multiprocessing.Event` that can be set to|
    |             |signal an update event                           |
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

       Please ensure that all ``args`` and ``kwargs`` can be pickled.'''

    def __init__(self, filepath, url,
                 newfiles='project.zip',
                 updatedir='downloads',
                 log_level=WARNING,
                 *args,**kwargs):
        self.log=multiprocessing.get_logger()
        #Create handle to self.log only if necessary
        self.log.setLevel(log_level)
        if len(self.log.handlers)==0:
            # Create handler to sys.stderr
            multiprocessing.log_to_stderr()
        self.log.info("Initializing launcher")
        # Check that version.txt is valid and create it if it does not exist
        open(self.version_doc, 'a').close() # "Touch" self.version_doc
        if not self.version_doc_validator():
            self.log.warning("{0} does not have a valid version number!\n"
                             "Please check that {0} is not being used!\n"
                             "It will be overwritten by this program!\n"
                             "If the {0} is corrupted,"
                             "Please use the logfile at {1} to restore it."
                             .format(self.version_doc,self.version_log))
            warnings.warn("{0} is corrupted!".format(self.version_doc),
                          CorruptedFileWarning,
                          stacklevel=2)
        # Check that version_history.log is valid
        open(self.version_log, 'a').close() # "Touch" self.version_log
        if not self.version_log_validator():
            self.log.warning("Log file at {0} is corrupted!\n"
                             "Please check that {0} is "
                             "not being used!\n"
                             "It will be overwritten "
                             "by this program!".format(self.version_log))
            warnings.warn("{0} is corrupted!"
                          .format(self.version_log),
                          CorruptedFileWarning,
                          stacklevel=2)

        if len(filepath) != 0:
            self.filepath = filepath
        else:
            raise ValueError("Filepath must not be empty")
        # Check that URL is specified
        if len(url) == 0:
            raise ValueError("URL must not be empty")
        # Append slash to end of URL if it is not present
        if url.endswith("/"):
            self.url = url
        else:
            self.url = url + "/"
        # Check for valid updatedir
        if len(os.path.normpath(updatedir).split(os.path.sep))>1:
            raise ValueError("updatedir should be a single directory name")
        else:
            self.updatedir = updatedir
        # Check for valid newfiles
        if len(os.path.normpath(newfiles).split(os.path.sep))>1:
            raise ValueError("newfiles should be a single file name")
        else:
            self.newfiles = newfiles
        self.update = multiprocessing.Event()
        self.pid = os.getpid()
        self.args = args
        self.kwargs = kwargs
        self.__process = multiprocessing.Process(target=self._call_code,
                                                 args=self.args,
                                                 kwargs=self.kwargs)
        self.log.info("Launcher initialized")

####################### Filename getters and validators ######################

    @property
    def version_doc(self):
        return "version.txt"

    @property
    def version_log(self):
        return "version_history.log"

    @property
    def file_list(self):
        return "filelist.txt"

    def version_doc_validator(self):
        """Validates the file containing the current version number.

        :return: Whether the version_doc is a proper version
        :rtype: bool
        """
        version_valid=True
        with warnings.catch_warnings():
            warnings.simplefilter("error",category=PEP440Warning)
            try:
                with open(self.version_doc,"r") as version_check:
                    vers=version_check.read()
                    if len(vers)>0:
                        vers_obj=parse_version(vers)
                        if not isinstance(vers_obj,SetuptoolsVersion):
                            raise PEP440Warning
            except PEP440Warning:
                version_valid=False
        return version_valid

    def version_log_validator(self):
        """Validates the file containing the version history.

        :return: Whether the version_log is formatted properly
        :rtype: bool
        """
        valid_log=True
        with open(self.version_log,"r") as log_file:
            log_syntax=re.compile(
                r"Old .+?\|(New .+?|Up to date)\|Time .+?")
            version=log_file.read()
            if version!="\n" and len(version)>0:
                has_match=re.match(log_syntax,version)
                valid_log=bool(has_match)
        return bool(valid_log)

######################### Process attribute getters  #########################

    @property
    def process_is_alive(self):
        return self.__process.is_alive()

    @property
    def process_pid(self):
        return self.__process.pid

    @property
    def process_exitcode(self):
        return self.__process.exitcode

    def process_join(self,timeout=None):
        self.log.info("Joining process")
        self.__process.join(timeout)

    def process_terminate(self):
        self.log.warning("Terminating Process")
        self.__process.terminate()

########################### Code execution methods ###########################

    def _call_code(self, *args, **kwargs):
        '''Method that executes the wrapped code.

           This is internally used as target of a
           :py:class:`multiprocessing.Process` instance.

           :param tuple args: ``*args`` tuple from self.args
           :param dict kwargs: ``**kwargs`` dict from self.kwargs

           .. warning::

              End users should never call this directly.
              Please use the :meth:`run` method instead.'''
        # Open code file
        with open(self.filepath, mode='r') as code_file:
            code = code_file.read()
        localvar = vars(self).copy()
        # Manipulate __dict__ attribute to add handle to check_new
        localvar["check_new"] = self.check_new
        # Remove handle to process
        del localvar["_Launcher__process"]
        # Pass in args, kwargs, and logger
        localvar["args"]=args
        localvar["kwargs"]=kwargs
        # multiprocessing.get_logger again since this is not pickleable
        localvar["log"]=multiprocessing.get_logger()
        localvar["log"].debug("Starting process with"
                              " the following local variables:\n"+\
                              pprint.pformat(localvar))
        # Execute code in file
        exec(code, dict(), localvar)

    def run(self, background=False):
        '''Method used to run code.

           If background is ``False``, returns the Process's exitcode.

           :param bool background: Whether to run code in background

           :return: the exit code if background is ``False``
           :rtype: :class:`int` or :class:`None`'''
        # Find the right error to raise depending on python version
        self.log.info("Starting code")
        try:
            error_to_raise=FileNotFoundError
        except NameError:
            error_to_raise=IOError
        if not os.path.isfile(self.filepath):
            raise error_to_raise("No file at {0}".format(self.filepath))
        if self.process_pid is None:
            # Process has not run yet
            _backup_log=self.log
            del self.log
            self.__process.start()
            self.log=_backup_log
            self.log.info("Process started")
            if not background:
                self.process_join()
                #Exit code can be used by program that calls the launcher
                return self.process_exitcode
        else:
            # Process has started
            if self.process_exitcode is not None:
                # Process has already terminated
                # Reinitialize the process instance
                self.__process = None
                self.__process = multiprocessing.Process(target=
                                                         self._call_code,
                                                         args=self.args,
                                                         kwargs=self.kwargs)
                # Recursion, since this will reset @property properties
                self.run(background)
            else:
                raise ProcessRunningException

######################### New code retrieval methods #########################

    def check_new(self):
        '''Retrieves the latest version number from the remote host.

           :return: Whether a newer version is available
           :rtype: bool

           .. note::
              This function internally uses setuptool's ``parse_version``
              to compare versions.

              Any versioning scheme described in :pep:`440` can be used.'''
        self.log.info("Checking for updates")
        versionurl=self.url+self.version_doc
        # Get new files
        get_new=requests.get(versionurl, allow_redirects=True)
        get_new.raise_for_status()
        newver=get_new.text
        newver=newver.rstrip("\n")
        # Read in old version and compare to new version
        with open(self.version_doc, 'r') as old_version:
            oldver=old_version.read()
            oldver=oldver.rstrip("\n")
        has_new=(parse_version(newver)>parse_version(oldver))
        # Add entry to the logfile and update version.txt
        if has_new:
            version_to_add="Old {0}|New {1}|Time {2}\n"\
                           .format(oldver,newver,datetime.utcnow())
        else:
            version_to_add="Old {0}|Up to date|Time {1}\n"\
                           .format(oldver,datetime.utcnow())
        with open(self.version_log, "a") as log_file:
            log_file.write(version_to_add)
        with open(self.version_doc, 'w') as new_version:
            new_version.write(newver)
        return has_new


    def _reset_update_dir(self):
        '''Resets the update directory to its default state.

           It also creates a new update directory if one doesn't exist.'''
        self.log.debug("Resetting update directory")
        if os.path.isdir(self.updatedir):
            # Remove old contents
            shutil.rmtree(self.updatedir)
        # Make new empty directory
        # shutil.rmtree would have deleted the directory
        os.mkdir(self.updatedir)

    def _get_new(self):
        '''Retrieves the new archive and extracts it to the downloads
           directory.'''
        self.log.info("Retrieving new version")
        # Remove old archive
        if os.path.isfile(self.newfiles):
            os.remove(self.newfiles)
        newurl = self.url+self.newfiles
        # Get new files
        http_get = requests.get(newurl, stream=True, allow_redirects=True)
        http_get.raise_for_status()
        with open(self.newfiles, 'wb') as filehandle:
            for chunk in http_get.iter_content(chunk_size=1024*50):
                if chunk:
                    filehandle.write(chunk)
        # Unpack archive and remove it after extraction
        unpack_archive(self.newfiles, self.updatedir)
        os.remove(self.newfiles)

    def _replace_files(self):
        """Replaces the existing files with the downloaded files."""
        self.log.info("Replacing files")
        # Read in files from filelist and move to tempdir
        tempdir=tempfile.mkdtemp()
        self.log.debug("Created tempdir at {0}".format(tempdir))
        self.log.info("Moving old files to tempdir")
        with open(self.file_list, "r") as file_handle:
            for line in file_handle:
                file_rm=os.path.normpath(os.path.join(".",line))
                file_rm=file_rm.rstrip("\n")
                # Confirm that each file in filelist exists
                if not os.path.isfile(file_rm):
                    self.log.error("{0} contains the invalid filepath {1}.\n"
                                   "Please check that {0} is not being used!\n"
                                   "Otherwise the {0} is corrupted.\n"
                                   "Updates will fail until this is restored."
                                   .format(self.file_list,file_rm))
                    warnings.warn("{0} is corrupted and contains the "
                                  "invalid path {1}!"
                                  .format(self.file_list,file_rm),
                                  CorruptedFileWarning,
                                  stacklevel=2)
                file_rm_temp=os.path.join(tempdir,file_rm)
                file_rm_temp_dir=os.path.dirname(file_rm_temp)
                if not os.path.isdir(file_rm_temp_dir):
                    # exist_ok does not exist in Python 2
                    os.makedirs(file_rm_temp_dir)
                if file_rm.split(os.path.sep)[0] not in \
                                        [self.updatedir, self.version_doc,
                                         self.version_log]:
                    self.log.debug("Moving {0} to {1}".format(file_rm,tempdir))
                    shutil.move(file_rm,file_rm_temp)
                    file_rm_dir=os.path.dirname(file_rm)
                    if os.path.isdir(file_rm_dir):
                        if not os.listdir(file_rm_dir):
                            os.rmdir(file_rm_dir)
                            self.log.debug("Removing directory {0}"
                                           .format(file_rm_dir))
        self.log.info("Backing up current filelist")
        filelist_backup=tempfile.NamedTemporaryFile(delete=False)
        try:
            with open(self.file_list, "r+b") as file_handle:
                shutil.copyfileobj(file_handle,filelist_backup)
        except Exception:
            self.log.exception("Backup of current filelist failed!")
            raise
        finally:
            filelist_backup.close()
        self.log.info("Removing old filelist")
        os.remove(self.file_list)
        self.log.info("Creating new filelist")
        filelist_new=list()
        for dirpath, dirnames, filenames in os.walk(self.updatedir):
            for filename in filenames:
                filepath=os.path.normpath(os.path.join(dirpath,
                                                       filename))
                relpath_start=os.path.join(self.updatedir)
                filepath=os.path.relpath(filepath,start=relpath_start)
                filepath=os.path.normpath(filepath)
                filepath+="\n"
                filelist_new.append(filepath)
        self.log.debug("New filelist is:\n"+pprint.pformat(filelist_new))
        self.log.info("Writing new filelist to {0}".format(self.file_list))
        with open(self.file_list, "w") as file_handle:
            file_handle.writelines(filelist_new)
        self.log.info("Copy downloaded contents to current directory")
        copy_glob(os.path.join(self.updatedir,"*"),".")
        self.log.info("Remove backup filelist")
        os.remove(filelist_backup.name)
        self.log.info("Removing tempdir")
        shutil.rmtree(tempdir)

    def update_code(self):
        """Updates the code if necessary"""
        if self.check_new():
            self.log.info("Beginning update process")
            self._reset_update_dir()
            self._get_new()
            self._replace_files()
            self._reset_update_dir()
            self.log.info("Update successful")
        else:
            self.log.info("Already up to date")
