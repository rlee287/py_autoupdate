import glob
import shutil
import os

def move_glob(src,dst):
    """Moves files from src to dest.

    src may be any glob to recognize files. dst must be a folder."""
    for obj in glob.iglob(src):
        shutil.move(obj,dst)
