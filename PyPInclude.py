from setuptools import setup as __setup__
from setuptools import find_packages
from os import listdir as __ls__
from os.path import join as __join_path__
from os.path import isdir as __is_dir__
from os.path import isfile as __is_file__

def __return_name_if_is_exist_in__(f, target, where):
    ret = __join_path__(where, target)
    return (ret if f(ret) else None) if target in where else None

def __core__(package_paths, **kargv):
    ret = {}
    for package_path in package_paths:
        PyPInclude = __return_name_if_is_exist_in__(__is_dir__, "__PyPInclude__", package_path)
        if PyPInclude:
            if "package_data" in ret: ret["package_data"][package_path] = ["__PyPInclude__/*"]
            else: ret["package_data"] = { package_path : ["__PyPInclude__/*"] }
            if __return_name_if_is_exist_in__(__is_file__, "__main__.py", PyPInclude):
                if 
    return ret

def setup(*, package_paths, **kargv):
    return __setup__(**kargv, **__core__(package_paths, **kargv))