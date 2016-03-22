from __future__ import absolute_import, print_function

from pkg_resources import parse_version
import requests
import multiprocessing
import os
import sys
import shutil

class Launcher:
    def __init__(self, filepath, url,
                 updatedir='downloads', vdoc='version.txt',
                 *args, **kwargs):
        self.url=url
        self.filepath=filepath
        self.updatedir=updatedir
        self.vdoc=vdoc
        self.update=multiprocessing.Event()
        self.pid=os.getpid()
        self.args=args
        self.kwargs=kwargs

    def _call_code(self):
        #open code file
        try:
            with open(self.filepath, mode='r') as file:
                code=file.read()
                #Local variable for called file=class fields
                exec(code,globals(),vars(self))
        except IOError:
            print('Unable to open file to run code', file=sys.stderr)
    
    def run(self):
        #Call code through wrapper
        p = multiprocessing.Process(target=self._call_code)
        p.start()
        p.join()
        #Exit code can be used by program that calls the launcher
        return p.exitcode

    def _reset_update_dir(self):
        if not os.path.isdir(self.updatedir):
            os.makedirs(self.updatedir)
        else:
            #Remove old contents
            try:
                shutil.rmtree(self.updatedir)
            except:
                print(e, file=sys.stderr)

    def _get_new(self):
        local_filename=self.url.split('/')[-1]
        file_location=self.updatedir+local_filename
        #get new files
        r=requests.get(self.url, stream=True, allow_redirects=True)
        with open(file_location, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*50):
                if chunk:
                    f.write(chunk)
        return local_filename
    
    def _check_new(self):
        oldpath=self.vdoc+'.old'
        newpath=self.vdoc
        os.rename(newpath,oldpath)
        versionurl=self.url+self.vdoc
        #get new files
        r=requests.get(versionurl, stream=True, allow_redirects=True)
        with open(newpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                if chunk:
                    f.write(chunk)
        with open(oldpath, 'r') as f:
            oldver=f.read()
        with open(newpath) as f:
            newver=f.read()
        os.remove(oldpath)
        return parse_version(newver)>parse_version(oldver)

    def update(self):
        self._reset_update_dir()

