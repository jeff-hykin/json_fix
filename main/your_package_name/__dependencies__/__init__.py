from os import remove, getcwd, makedirs, listdir, rename, rmdir, system
from os.path import isabs, isfile, isdir, join, dirname, basename, exists, splitext, relpath, join, dirname
from pathlib import Path
import os
import shutil
import sys
import warnings # TODO: convert serveral prints to warnings
from hashlib import md5 

is_windows = os.name == 'nt'
# 
# helpers
# 
def consistent_hash(value):
    if isinstance(value, bytes):
        return md5(value).hexdigest()
    
    if isinstance(value, str):
        return md5(("@"+value).encode('utf-8')).hexdigest()
    
    if isinstance(value, (bool, int, float, type(None))):
        return md5(str(value).encode('utf-8')).hexdigest()
        
    else:
        return md5(pickle.dumps(value, protocol=4)).hexdigest()

def make_absolute_path(to, coming_from=None):
    # if coming from cwd, its easy
    if coming_from is None:
        return os.path.abspath(to)
    
    # source needs to be absolute
    coming_from_absolute = os.path.abspath(coming_from)
    # if other path is  absolute, make it relative to coming_from
    relative_path = to
    if os.path.isabs(to):
        relative_path = os.path.relpath(to, coming_from_absolute)
    return os.path.join(coming_from_absolute, relative_path)

def make_relative_path(*, to, coming_from=None):
    if coming_from is None:
        coming_from = get_cwd()
    return os.path.relpath(to, coming_from)

def path_pieces(path):
    """
    example:
        *folders, file_name, file_extension = path_pieces("/this/is/a/filepath.txt")
    """
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break
    folders.reverse()
    *folders, file = folders
    filename, file_extension = os.path.splitext(file)
    return [ *folders, filename, file_extension ]

def remove(path):
    if not Path(path).is_symlink() and os.path.isdir(path):
        shutil.rmtree(path)
    else:
        try:
            os.remove(path)
        except:
            pass

def final_target_of(path):
    # resolve symlinks
    if os.path.islink(path):
        have_seen = set()
        while os.path.islink(path):
            path = os.readlink(path)
            if path in have_seen:
                return None # circular broken link
            have_seen.add(path)
    return path
    
# 
# globals
# 
this_file = make_absolute_path(__file__)
this_folder = dirname(this_file)
settings_path = join(this_folder, '..', 'settings.json')

# 
# find closest import path
#
*folders_to_this, _, _ = path_pieces(this_file)
best_match_amount = 0
best_import_zone_match = None
import sys
for each_import_path in sys.path:
    each_import_path = make_absolute_path(each_import_path)
    if not isdir(each_import_path):
        continue
    *folders_of_import_path, name, extension = path_pieces(each_import_path)
    folders_of_import_path = [ *folders_of_import_path, name+extension]
    matches = 0
    for folder_to_this, folder_to_some_import_zone in zip(folders_to_this, folders_of_import_path):
        if folder_to_this != folder_to_some_import_zone:
            break
        else:
            matches += 1
    
    if matches > best_match_amount:
        best_import_zone_match = each_import_path
        best_match_amount = matches

# shouldn't ever happen
if best_import_zone_match is None:
    raise Exception(f"""Couldn't find a path to {this_file} from any of {sys.path}""")

# 
# import json mapping
# 
import json
from os.path import join
# ensure it exists
if not isfile(settings_path):
    with open(settings_path, 'w') as the_file:
        the_file.write(str("{}"))
with open(settings_path, 'r') as in_file:
    settings = json.load(in_file)
    if not isinstance(settings, dict):
        raise Exception(f"""\n\n\nThis file is corrupt (it should be a JSON object):{settings_path}""")

# ensure that pure_python_packages exists
if not isinstance(settings.get("pure_python_packages", None), dict):
    settings["pure_python_packages"] = {}
dependency_mapping = settings["pure_python_packages"]

# 
# calculate paths
# 
from random import random
counter = 0
import_strings = []
for dependency_name, dependency_info in dependency_mapping.items():
    counter += 1
    if dependency_name.startswith("__"):
        raise Exception(f"""dependency names cannot start with "__", but this one does: {dependency_name}. This source of that name is in: {settings_path}""")
    if not dependency_name.isidentifier():
        raise Exception(f"""dependency names must be an identifier ("blah".isidentifier() in python), but this one is not: {dependency_name}. This source of that name is in: {settings_path}""")
    
    target_path = join(this_folder, dependency_info["path"])
    relative_target_path = make_relative_path(to=target_path, coming_from=best_import_zone_match)
    # ensure the parent folder
    *path_parts, _, _ = path_pieces(join(relative_target_path, "_"))
    unique_name = f"{dependency_name}_{random()}_{counter}".replace(".","")
    target_folder_for_import = join(this_folder, dependency_name)
    
    target_path_obj = Path(target_folder_for_import)
    if is_windows:
        if not target_path_obj.exists():
            # windows has to copy the files because it can't symlink
            if os.path.isdir(target_path):
                shutil.copytree(target_path, target_folder_for_import)
            else:
                shutil.copy(target_path, target_folder_for_import)
    elif not target_path_obj.is_symlink() or final_target_of(target_folder_for_import) != dependency_info["path"]:
        # clear the way (encase something was in the way)
        remove(target_folder_for_import)
        target_path_obj.symlink_to(dependency_info["path"])
        
# import the paths
__all__ = []
for dependency_name, dependency_info in dependency_mapping.items():
    # this will register it with python and convert it to a proper module with a unique path (important for pickling things)
    try:
        exec(f"""from .{dependency_name} import __file__ as _""")
        __all__.append(dependency_name)
    except ImportError as error:
        if f"{error}" == "cannot import name '__file__'":
            # this means top level folder isn't a module or doesnt have a __init__.py
            # some modules simply are like this
            pass
        else:
            raise error