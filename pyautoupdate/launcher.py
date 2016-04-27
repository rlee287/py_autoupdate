from __future__ import absolute_import, print_function

from pkg_resources import parse_version
import multiprocessing
import os
import sys
import shutil

import requests

class Launcher:
    def __init__(self, filepath, url,
                 updatedir='downloads', vdoc='version.txt',
                 *args, **kwargs):
        self.url = url
        self.filepath = filepath
        self.updatedir = updatedir
        self.vdoc = vdoc
        self.update = multiprocessing.Event()
        self.pid = os.getpid()
        self.args = args
        self.kwargs = kwargs

    def _call_code(self):
        '''Method that executes the wrapped code.
           Internally used as target of multiprocessing.Process instance'''
        #open code file
        try:
            code_file = open(self.filepath, mode='r')
            code = code_file.read()
        except IOError:
            print('Unable to open file to run code', file=sys.stderr)
        finally:
            #Local variable for called file=class fields
            exec(code,globals(),vars(self))
    
    def run(self):
        '''Method used to run code
           Returns the exit code of the executed code'''
        #Call code through wrapper
        run_code = multiprocessing.Process(target=self._call_code)
        run_code.start()
        run_code.join()
        #Exit code can be used by program that calls the launcher
        return run_code.exitcode

    def _reset_update_dir(self):
        '''Resets the update directory to its default state
           Also creates a new update directory if it doesn't exist'''
        if not os.path.isdir(self.updatedir):
            os.makedirs(self.updatedir)
        else:
            #Remove old contents
            shutil.rmtree(self.updatedir)

    def _get_new(self):
        local_filename = self.url.split('/')[-1]
        file_location = self.updatedir+local_filename
        #get new files
        http_get = requests.get(self.url, stream=True, allow_redirects=True)
        with open(file_location, 'wb') as f:
            for chunk in http_get.iter_content(chunk_size=1024*50):
                if chunk:
                    f.write(chunk)
        http_get.raise_for_status()
        return local_filename
    
    def check_new(self):
        '''Retrieves the latest version number from the remote host
           Internally uses setuptool's parse_version to compare versions'''
        oldpath=self.vdoc+'.old'
        newpath=self.vdoc
        os.rename(newpath,oldpath)
        versionurl=self.url+self.vdoc
        #get new files
        r=requests.get(versionurl, allow_redirects=True)
        with open(newpath, 'w') as new_version:
            new_version.write(r.text)
        r.raise_for_status()
        with open(oldpath, 'r') as f:
            oldver=f.read()
        with open(newpath) as new_version:
            newver=new_version.read()
        os.remove(oldpath)
        return parse_version(newver)>parse_version(oldver)

    def update_code(self):
        if self.check_new():
            #self._get_new()
            self._reset_update_dir()
        else:
            print("Already up to date")

