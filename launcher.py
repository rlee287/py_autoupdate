import requests
import multiprocessing
import src.run
from exceptions import *

class Launcher:
    def __init__(self, url)
        self.url=url

    def run(self):
        p = multiprocessing.Process(target=src.run.run())
        p.start()
        p.join()

    def update(self):
        pass

