from __future__ import absolute_import, print_function

import requests
import multiprocessing
import sys

class Launcher:
    def __init__(self, filepath, url, **kwargs):
        self.url=url
        self.filepath=filepath
        self.updateEvent=multiprocessing.Event()
        self.extraArgs=kwargs

    def call_code(self):
        try:
            with open(self.filepath, mode='r') as file:
                code=file.read()
                def code_func(): pass
                code_func.__code__=compile(code,self.filepath,mode='exec')
                #code_func(self.updateEvent,**self.extraArgs)
                code_func()
        except IOError:
            print('Unable to open file to run code', file=sys.stderr)
    
    def run(self):
        p = multiprocessing.Process(target=self.call_code)
        p.start()
        p.join()

    def update(self):
        pass

