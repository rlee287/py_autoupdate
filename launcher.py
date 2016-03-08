from __future__ import absolute_import, print_function

import requests
import multiprocessing
import sys

class Launcher:
    def __init__(self, filepath, url, **kwargs):
        self.url=url
        self.filepath=filepath
        self.update=multiprocessing.Event()
        self.extraArgs=kwargs

    def call_code(self):
        try:
            with open(self.filepath, mode='r') as file:
                code=file.read()
                exec(code,globals(),
                     {'updateEvent':self.update,'kwargs':self.extraArgs})
        except IOError:
            print('Unable to open file to run code', file=sys.stderr)
    
    def run(self):
        p = multiprocessing.Process(target=self.call_code)
        p.start()
        p.join()

    def update(self):
        pass

