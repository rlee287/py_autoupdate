from __future__ import absolute_import, print_function

import multiprocessing
import os
import sys
import shutil
import tempfile

from pkg_resources import parse_version
from setuptools.archive_util import unpack_archive
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
                 *args, **kwargs):
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

########################### Code execution methods ###########################

    def _call_code(self):
        '''Method that executes the wrapped code.

           Internally used as target of :py:class:`multiprocessing.Process`
           instance

           .. warning::

              End users should never call this directly.
              Please use the :meth:`run` method instead.'''
        #Open code file
        try:
            code_file = open(self.filepath, mode='r')
            code = code_file.read()
        except (FileNotFoundError, IOError):
            print('Unable to open file {} to run code'.format(self.filepath)
                  , file=sys.stderr)
            print('The full traceback is below:', file=sys.stderr)
            raise
        else:
            #Only attempt to run when file has been opened
            localvar = vars(self).copy()
            localvar["check_new"] = self.check_new
            exec(code, globals(), localvar)

    def run(self, background=False):
        '''Method used to run code.

           If background is ``True``, returns a handle to the Process object.

           Otherwise, it returns the Process's exitcode.

           :param bool background: Whether to run code in background

           :return: the exit code of the executed code or the Process
           :rtype: :class:`int` or :class:`multiprocessing.Process`'''
        #Call code through wrapper
        run_code = multiprocessing.Process(target=self._call_code)
        run_code.start()
        if not background:
            run_code.join()
            #Exit code can be used by program that calls the launcher
            return run_code.exitcode
        else:
            return run_code

######################### New code retrieval methods #########################

    def check_new(self):
        '''Retrieves the latest version number from the remote host.

           :return: Whether a newer version is available
           :rtype: bool

           .. note::
              This function internally uses setuptool's ``parse_version``
              to compare versions.

              Any versioning scheme described in :pep:`440` can be used.'''
        versionurl=self.url+"version.txt"
        #get new files
        get_new=requests.get(versionurl, allow_redirects=True)
        get_new.raise_for_status()
        #move to new file only when connection succeeds
        if os.path.isfile("version.txt.old"):
            os.remove("version.txt.old")
        os.rename("version.txt","version.txt.old")
        with open("version.txt", 'w') as new_version:
            new_version.write(get_new.text)
        with open("version.txt.old", 'r') as old_version:
            oldver=old_version.read()
        newver=get_new.text
        return parse_version(newver)>parse_version(oldver)


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
        filelist=list()
        with open("filelist.txt", "r") as file_handle:
            for line in file_handle:
                filelist.append(os.path.join(".",line))
        for file_rm in filelist:
            if file_rm.split(os.path.sep)[0]!="downloads":
                os.remove(file_rm)
        shutil.move(downloads, ".")

    def update_code(self):
        if self.check_new():
            self._reset_update_dir()
            self._get_new()
            self._replace_files()
        else:
            print("Already up to date")
