from __future__ import absolute_import, print_function

import requests
import multiprocessing
import os
import sys
import shutil

class Launcher:
    def __init__(self, filepath, url, updatedir='downloads', *args, **kwargs):
        self.url=url
        self.filepath=filepath
        self.updatedir=updatedir
        self.update=multiprocessing.Event()
        self.pid=os.getpid()
        self.args=args
        self.kwargs=kwargs

    def call_code(self):
        try:
            with open(self.filepath, mode='r') as file:
                code=file.read()
                exec(code,globals(),vars(self))
        except IOError:
            print('Unable to open file to run code', file=sys.stderr)
    
    def run(self):
        p = multiprocessing.Process(target=self.call_code)
        p.start()
        p.join()

    def get_new(self):
        local_filename = self.url.split('/')[-1]
        file_location=self.updatedir+local_filename
        #Make update directory if it doesn't exist
        if not os.path.isdir(self.updatedir):
            os.makedirs(self.updatedir)
        else:
            #Remove old contents
            for files in os.listdir(self.updatedir):
                file_path = os.path.join(self.updatedir, files)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print (e)
        #get new files
        r = requests.get(self.url, stream=True, allow_redirects=True)
        with open(file_location, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*50):
                if chunk:
                    f.write(chunk)
        return local_filename

    def update(self):
        pass

