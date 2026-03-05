from setuptools import setup as __setup__
from setuptools.command.install import install as __install__
from setuptools.command.develop import develop as __develop__
from setuptools import find_packages
from os import listdir as __ls__
from os.path import join as __join_path__
from os.path import isdir as __is_dir__
from os.path import isfile as __is_file__
from os.path import sep as __path_sep__
from os.path import basename as __base_name__
from subprocess import run as __shell__

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
                if "cmdclass" in ret: ret["cmclass"].append(__base_name__(package_path))
                else: ret["cmclass"] = [__base_name__(package_path)]
    if "cmclass" in ret:
        cmclass = ret["cmclass"]
        class install(__install__):
            def run(self):
                __install__.run(self)
                installed_dir = self.install_lib
                for init_script in map(lambda x : __join_path__(installed_dir, x, "__PyPInclude__", "main.py"), filter(cmclass.__contains__, self.distribution.packages)): __shell__(["python", "-m", init_script])
        class develop(__develop__):
            def run(self):
                __develop__.run(self)
                installed_dir = self.egg_path
                for init_script in map(lambda x : __join_path__(installed_dir, x, "__PyPInclude__", "main.py"), filter(cmclass.__contains__, self.distribution.packages)): __shell__(["python", "-m", init_script])
        ret["cmclass"] = {"install" : install, "develop" : develop}
    return ret

def setup(*, package_paths, **kargv):
    return __setup__(**kargv, **__core__(package_paths, **kargv))