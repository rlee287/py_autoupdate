import requests
import multiprocessing
import sys
#from .src import start
#from .exceptions import *

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
                def code_func(updateEvent,**kwargs): pass
                code_func.__code__=code
                code_func(self.updateEvent,**self.extraArgs)
        except IOError:
            print('Unable to open file to run code', file=sys.stderr)
    
    def run(self):
        p = multiprocessing.Process(target=self.call_code)
        p.start()
        p.join()

    def update(self):
        pass

