import requests
import multiprocessing
from .src import start
from .exceptions import *

class Launcher:
    def __init__(self, url):
        self.url=url

    def run(self):
        p = multiprocessing.Process(target=start.run())
        p.start()
        p.join()

    def update(self):
        pass

