from __future__ import absolute_import

import requests
import multiprocessing
from .src import start
from .exceptions import *

class Launcher:
    def __init__(self, url):
        self.url=url
        self.updateEvent=multiprocessing.Event()

    def run(self):
        p = multiprocessing.Process(target=start.run,
                                    args=(self.updateEvent,))
        p.start()
        p.join()

    def update(self):
        pass

