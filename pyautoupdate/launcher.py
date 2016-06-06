from __future__ import absolute_import, print_function

from pkg_resources import parse_version
import multiprocessing
import os
import sys
import shutil

from setuptools.archive_util import unpack_archive
import requests

class Launcher:
    '''Creates a :class:`Launcher` object.

    :param str filepath: Path to file to execute
    :param str url: Base URL from which to download new versions
    :param str newfiles: Name of archive with new versions to download from
     site
    :param str updatedir: Directory in which new versions are downloaded into
    :param str vdoc: Name of document containing version number
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
    |``update``   |:py:class:`multiprocessing.Event` that can be    |
    |             |set to signal an update event                    |
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
                 vdoc='version.txt',
                 *args, **kwargs):
        self.url = url
        self.filepath = filepath
        self.updatedir = updatedir
        self.vdoc = vdoc
        self.newfiles = newfiles
        self.update = multiprocessing.Event()
        self.pid = os.getpid()
        self.arguments = (args, kwargs)

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

    def run(self):
        '''Method used to run code.

           :return: the exit code of the executed code
           :rtype: int'''
        #Call code through wrapper
        run_code = multiprocessing.Process(target=self._call_code)
        run_code.start()
        run_code.join()
        #Exit code can be used by program that calls the launcher
        return run_code.exitcode

    def _reset_update_dir(self):
        '''Resets the update directory to its default state.

           Also creates a new update directory if it doesn't exist.'''
        if os.path.isdir(self.updatedir):
            #Remove old contents
            shutil.rmtree(self.updatedir)
        #Make new directory (one shouldn't exist)
        os.makedirs(self.updatedir)

    def _get_new(self):
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
        if os.path.isfile(self.newfiles):
            os.remove(self.newfiles)

    def check_new(self):
        '''Retrieves the latest version number from the remote host.

           :return: Whether a newer version is available
           :rtype: bool

           .. note::
              This function internally uses setuptool's ``parse_version``
              to compare versions.

              Any versioning scheme described in :pep:`440` can be used.'''
        oldpath=self.vdoc+'.old'
        newpath=self.vdoc
        versionurl=self.url+self.vdoc
        #get new files
        get_new=requests.get(versionurl, allow_redirects=True)
        get_new.raise_for_status()
        #move to new file only when connection succeeds
        if os.path.isfile(oldpath):
            os.remove(oldpath)
        os.rename(newpath,oldpath)
        with open(newpath, 'w') as new_version:
            new_version.write(get_new.text)
        with open(oldpath, 'r') as old_version:
            oldver=old_version.read()
        newver=get_new.text
        return parse_version(newver)>parse_version(oldver)

    def update_code(self):
        if self.check_new():
            self._reset_update_dir()
            self._get_new()
        else:
            print("Already up to date")
