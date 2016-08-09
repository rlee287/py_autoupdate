from __future__ import absolute_import, print_function

from datetime import datetime
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import multiprocessing
import os
import shutil
import tempfile
import pprint
import warnings
import re

from pkg_resources import parse_version, SetuptoolsVersion, PEP440Warning
from setuptools.archive_util import unpack_archive
from ._move_glob import move_glob, copy_glob
from .exceptions import ProcessRunningException, CorruptedFileWarning

import requests

class Launcher:
    '''Creates a :class:`Launcher` object.

    :param str filepath: Path to file to execute
    :param str url: Base URL from which to download new versions
    :param str newfiles: Name of archive with new versions to download from
     site
    :param str updatedir: Directory in which new versions are downloaded into
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
    |``updatedir``|Directory into which the new archive is extracted|
    +-------------+-------------------------------------------------+
    |``newfiles`` |Name of the archive containing the new files     |
    +-------------+-------------------------------------------------+
    |``update``   |:class:`multiprocessing.Event` that can be set to|
    |             |signal an update event                           |
    +-------------+-------------------------------------------------+
    |``pid``      |PID of parent process that spawns the code       |
    +-------------+-------------------------------------------------+
    |``args``     |``args`` for the spawned code                    |
    +-------------+-------------------------------------------------+
    |``kwargs``   |``kwargs`` for the spawned code                  |
    +-------------+-------------------------------------------------+

    .. warning::

       The :class:`Launcher` uses :class:`multiprocessing.Process`
       to run the code.

       Please ensure that all ``args`` and ``kwargs`` can be pickled.'''

    def __init__(self, filepath, url, newfiles='project.zip',
                 updatedir='downloads',
                 log_level=INFO,
                 *args, **kwargs):
        self.log=multiprocessing.log_to_stderr()
        self.log.info("Initializing launcher")
        # Check that version.txt
        with warnings.catch_warnings():
            invalid_log=False
            warnings.simplefilter("error",category=PEP440Warning)
            if os.path.isfile(self.version_doc):
                try:
                    with open(self.version_doc,"r") as version_check:
                        vers=version_check.read()
                        if len(vers)>0:
                            vers_obj=parse_version(vers)
                            if not isinstance(vers_obj,SetuptoolsVersion):
                                raise PEP440Warning
                except PEP440Warning:
                    invalid_log=True
            if invalid_log:
                self.log.warning("{0} does not have a valid version number!"
                                 .format(self.version_doc))
                self.log.warning("Please check that {0} is not being used!"
                                 .format(self.version_doc))
                self.log.warning("It will be overwritten by this program!")
                self.log.warning("Otherwise the {0} is corrupted."
                                 .format(self.version_doc))
                self.log.warning("Please use the logfile at {0} to restore it."
                                 .format(self.version_doc))
                warnings.warn("{0} is corrupted!".format(self.version_doc),
                                                         CorruptedFileWarning,
                                                         stacklevel=2)
        if os.path.isfile(self.version_log):
            with open(self.version_log,"r") as log_file:
                log_syntax=re.compile(
                              r"Old .+?\|(New .+?|Up to date)\|Time .+?")
                version=log_file.read()
                if version!="\n" and len(version)>0:
                    has_match=re.match(log_syntax,version)
                    if has_match is None:
                        self.log.warning("Log file at {0} is corrupted!"
                                         .format(self.version_log))
                        self.log.warning("Please check that {0} is "
                                         "not being used!"
                                         .format(self.version_log))
                        self.log.warning("It will be overwritten "
                                         "by this program!")
                        warnings.warn("{0} is corrupted!"
                                      .format(self.version_log),
                                      CorruptedFileWarning,
                                      stacklevel=2)

        if len(filepath) != 0:
            self.filepath = filepath
        else:
            raise ValueError("Filepath must not be empty")
        if len(url) == 0:
            raise ValueError("URL must not be empty")
        if url.endswith("/"):
            self.url = url
        else:
            self.url = url + "/"
        self.updatedir = updatedir
        self.newfiles = newfiles
        self.update = multiprocessing.Event()
        self.pid = os.getpid()
        self.args = args
        self.kwargs = kwargs
        self.oldcwd=os.getcwd()
        self.cwd=os.path.abspath(os.path.join(".",self.filepath))
        self.__process = multiprocessing.Process(target=self._call_code,
                                                 args=self.args,
                                                 kwargs=self.kwargs)

    @property
    def version_doc(self):
        return "version.txt"

    @property
    def version_log(self):
        return "version_history.log"

    @property
    def file_list(self):
        return "filelist.txt"

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
        self.__process.join(timeout)

    def process_terminate(self):
        self.__process.terminate()

########################### Code execution methods ###########################

    def _call_code(self):
        '''Method that executes the wrapped code.

           Internally used as target of :py:class:`multiprocessing.Process`
           instance

           .. warning::

              End users should never call this directly.
              Please use the :meth:`run` method instead.'''
        #Open code file
        with open(self.filepath, mode='r') as code_file:
            code = code_file.read()
        #Only attempt to run when file has been opened
        localvar = vars(self).copy()
        localvar["check_new"] = self.check_new
        del localvar["_Launcher__process"]
        exec(code, dict(), localvar)

    def run(self, background=False):
        '''Method used to run code.

           If background is ``True``, returns a handle to the Process object.

           Otherwise, it returns the Process's exitcode.

           :param bool background: Whether to run code in background

           :return: the exit code of the executed code or the Process
           :rtype: :class:`int` or :class:`multiprocessing.Process`'''
        #Find the right error to raise depending on python version
        try:
            error_to_raise=FileNotFoundError
        except NameError:
            error_to_raise=IOError
        if not os.path.isfile(self.filepath):
            raise error_to_raise("No file at {0}".format(self.filepath))
        if self.process_pid is None:
            # Process has not run yet
            self.__process.start()
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
        versionurl=self.url+self.version_doc
        #get new files
        get_new=requests.get(versionurl, allow_redirects=True)
        get_new.raise_for_status()
        newver=get_new.text
        newver=newver.rstrip("\n")
        #move to new file only when connection succeeds
        with open(self.version_doc, 'r') as old_version:
            oldver=old_version.read()
            oldver=oldver.rstrip("\n")
        has_new=(parse_version(newver)>parse_version(oldver))
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

           Also creates a new update directory if it doesn't exist.'''
        if os.path.isdir(self.updatedir):
            #Remove old contents
            shutil.rmtree(self.updatedir)
        #Make new directory (one shouldn't exist)
        os.makedirs(self.updatedir)

    def _get_new(self):
        '''Retrieves the new archive and extracts it to the downloads
           directory.'''
        if os.path.isfile(self.newfiles):
            os.remove(self.newfiles)
        newurl = self.url+self.newfiles
        #get new files
        http_get = requests.get(newurl, stream=True, allow_redirects=True)
        http_get.raise_for_status()
        with open(self.newfiles, 'wb') as filehandle:
            for chunk in http_get.iter_content(chunk_size=1024*50):
                if chunk:
                    filehandle.write(chunk)
        unpack_archive(self.newfiles, self.updatedir)
        os.remove(self.newfiles)

    def _replace_files(self):
        """Replaces the existing files with the downloaded files."""
        with open(self.file_list, "r") as file_handle:
            for line in file_handle:
                file_rm=os.path.normpath(os.path.join(".",line))
                if not os.path.isfile(file_rm):
                    self.log.error("{0} contains the invalid filepath {1}."
                                   .format(self.file_list,file_rm))
                    self.log.error("Please check that {0} is not being used!"
                                   .format(self.file_list))
                    self.log.error("Otherwise the {0} is corrupted."
                                   .format(self.file_list))
                    self.log.error("Updates will fail until this is restored.")
                    warnings.warn("{0} is corrupted!"
                                  .format(self.version_log),
                                  CorruptedFileWarning,
                                  stacklevel=2)
                if file_rm.split(os.path.sep)[0]!="downloads":
                    self.log.debug("Removing {0}",file_rm)
                    os.remove(file_rm)
                    file_rm_dir=os.path.dirname(file_rm)
                    if os.path.isdir(file_rm_dir):
                        try:
                            os.rmdir(file_rm_dir)
                            self.log.debug("Removing directory {0}",
                                           file_rm_dir)
                        except OSError:
                            pass #Directory is not empty yet
        tempdir=tempfile.mkdtemp()
        self.log.debug("Moving downloads to {0}", tempdir)
        move_glob(os.path.join(self.updatedir,"*"), tempdir)
        filelist_backup=tempfile.NamedTemporaryFile(delete=False)
        with open(self.file_list, "r+b") as file_handle:
            shutil.copyfileobj(file_handle,filelist_backup)
        filelist_backup.close()
        os.remove(self.file_list)
        filelist_new=list()
        for dirpath, dirnames, filenames in os.walk(tempdir):
            for filename in filenames:
                filepath=os.path.normpath(os.path.join(dirpath,
                                          filename))
                relpath_start=os.path.join(tempdir)
                filepath=os.path.relpath(filepath,start=relpath_start)
                filepath+="\n"
                filelist_new.append(filepath)
        self.log.debug("new filelist")
        self.log.debug(pprint.pformat(filelist_new))
        self.log.info("Writing new filelist to filelist.txt")
        with open(self.file_list, "w") as file_handle:
            file_handle.writelines(filelist_new)
        self.log.info("Copy tempdir contents to current directory")
        copy_glob(os.path.join(tempdir,"*"),".")
        self.log.info("Remove backup filelist")
        os.remove(filelist_backup.name)
        self.log.info("Removing tempdir")
        shutil.rmtree(tempdir)

    def update_code(self):
        """Updates the code if necessary"""
        if self.check_new():
            self._reset_update_dir()
            self._get_new()
            self._replace_files()
            self._reset_update_dir()
        else:
            self.log.info("Already up to date")
