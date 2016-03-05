import requests
import multiprocessing
from .src import start
from .exceptions import *

class Launcher:
    def __init__(self, url, **kwargs):
        self.url=url
        self.updateEvent=multiprocessing.Event()
        self.extraArgs=kwargs

    def run(self):
        p = multiprocessing.Process(target=start.run,
                                    args=(self.updateEvent,),
                                    kwargs=self.extraArgs)
        p.start()
        p.join()

    def update(self):
        pass

