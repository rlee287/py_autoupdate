from __future__ import absolute_import, print_function

import requests
import multiprocessing
import os
import sys

class Launcher:
    def __init__(self, filepath, url, *args, **kwargs):
        self.url=url
        self.filepath=filepath
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

    def update(self):
        pass

