#code stinks.

from martialaw.martialaw import martialaw as _clsr

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

"""
DEPRECATED when 0.0.2

it's indev ver. see repo's markdown. the range of age of indev ver is writed and also it will update over commit over commits

@lambda f : f()
def lib():
    data = {}
    class PyPInstallLibType:
        '''
        this class's data is not in this object. this class's data is in function which return this class's object.
        '''
        def __call__(self, libname, pw):
            if libname in data: assert data[libname][0] == hash(pw), "permission denied"
            else: data[libname] = (hash(pw), {})
            def addvar(var, value):
                data[libname][1][var] = value
                return value
            
            class PyPInstallLibExporter:
                '''
                this class's data is not in this object. this class's data is in function which return this class's object.
                '''
                def __getitem__(self, name):
                    def deco(value):
                        return addvar(name, value)
                    return deco
                
                def __neg__(self):
                    def deco(func):
                        return addvar(func.__name__, func)
                    return deco
            return PyPInstallLibExporter()
        
        def __getitem__(self, libname):
            class PyPInstallModuleType:
                '''
                this class's data is not in this object. this class's data is in function which return this class's object.
                '''
                def __getitems__(self, member):
                    return data[libname][1][member]
            return PyPInstallModuleType()
    return PyPInstallLibType()

cannot make private in python. function.__code__.co_varnames and function.__closure__ is can hake them.
"""

def __return_name_if_is_exist_in__(f, target, where):
    ret = __join_path__(where, target)
    return (ret if f(ret) else None) if target in where else None

def setup(*, package_paths, **kargv):
    ret = {}
    for package_path in package_paths:
        PyPInclude = __return_name_if_is_exist_in__(__is_dir__, "__PyPInclude__", package_path)
        
        # /* Step 1. Processing the PyPInclude */
        if PyPInclude: # if PyPInclude isn't Falsy Value such as None (= if PyPInclude is exist in package_path as directory)
            
            # /* Step 1.1. check which is it possible to acess ret["package_data"] then add package_path key as value which "__PyPInclude__/*" */
            if "package_data" in ret: ret["package_data"][package_path] = ["__PyPInclude__/*"]
            else: ret["package_data"] = { package_path : ["__PyPInclude__/*"] }
            
            # /* Step 1.2. add package name which __PyPIncluder__/ __main__.py is exist */            
            if __return_name_if_is_exist_in__(__is_file__, "__main__.py", PyPInclude):
                # /* see. it's same repartory as step 1 */
                if "cmdclass" in ret: ret["cmclass"].append(__base_name__(package_path))
                else: ret["cmclass"] = [__base_name__(package_path)]

    # /* Step 2. update cmclass as can use in setup function by defining cmclass which install class and develop class and use them */
    if "cmclass" in ret:
        cmclass = ret["cmclass"]

        is_in_cmclass = cmclass.__contains__
        get_confscript_path_getter = _clsr(lambda installed_dir_of_pkg, pkgname : __join_path__(installed_dir_of_pkg, pkgname, "__PyPInclude__", "__main__.py"))

        # /* Step 2.1. set pip install's Configuration Script */
        class install(__install__):
            # PEP 253, all class is based on MRO. including built-in types. we don't need to write __init__ function.
            def run(self):
                __install__.run(self)
                _ = map(
                    get_confscript_path_getter(
                        self.install_lib #install_dir_of_pkg(directory which package is install)
                    ), # path of install script
                    filter(
                        is_in_cmclass,
                        self.distribution.packages
                    ) # packages such that conf script is exist 
                ) # conf script paths
                for init_script in _: __shell__(["python", init_script]) # run each conf scripts

        # /* Step 2.2. set pip install -e's Configuration Script */
        class develop(__develop__):
            def run(self):
                __develop__.run(self)
                _ = map(
                    self.egg_path,
                    filter(
                        is_in_cmclass,
                        self.distribution.packages
                    )
                )
                for init_script in _: __shell__(["python", init_script])

        # /* Step 2. 3. update! */
        ret["cmclass"] = {"install" : install, "develop" : develop}

    # /* now cmclass and included directory is setted */
    return __setup__(**kargv, **ret)
