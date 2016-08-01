import glob
import shutil
import os

def move_glob(src,dst):
    """Moves files from src to dest.

    src may be any glob to recognize files. dst must be a folder."""
    for obj in glob.iglob(src):
        shutil.move(obj,dst)

def copy_glob(src,dst):
    """Copies files from src to dest.

    src may be any glob to recognize files. dst must be a folder."""
    for obj in glob.iglob(src):
        if os.path.isdir(obj):
#            start_part=os.path.commonpath([src,obj])
#            end_part=os.path.relpath(obj,start_part)
            shutil.copytree(obj,dst)
        else:
            shutil.copy2(obj,dst)


