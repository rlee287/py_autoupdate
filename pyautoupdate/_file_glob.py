import glob
import shutil
import os

if os.name == "nt": # pragma: no branch
    from .ntcommonpath import commonpath
else:
    from .posixcommonpath import commonpath

# def move_glob(src,dst):
#     """Moves files from src to dest.

#     src may be any glob to recognize files. dst must be a folder.
#     """
#     for obj in glob.iglob(src):
#         shutil.move(obj,dst)

def copy_glob(src,dst):
    """Copies files from src to dest.

    src may be any glob to recognize files. dst must be a folder.
    """
    for obj in glob.iglob(src):
        if os.path.isdir(obj):
            start_part=commonpath([src,obj])
            end_part=os.path.relpath(obj,start_part)
            ctree_dst=os.path.join(dst,end_part)
            if not os.path.isdir(ctree_dst):
                shutil.copytree(obj,ctree_dst)
            else:
                copy_glob(os.path.join(obj,"*"),ctree_dst)
        else:
            shutil.copy2(obj,dst)
