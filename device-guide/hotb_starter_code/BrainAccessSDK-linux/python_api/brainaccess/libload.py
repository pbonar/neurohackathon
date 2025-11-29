import platform
import ctypes
import pathlib

from ctypes.util import find_library
from os import getcwd
from os.path import join
from shutil import which

from brainaccess.utils.exceptions import BrainAccessException

_lib_directory = pathlib.Path(__file__).parent / "lib"


def get_lib_name(name: str) -> str:
    platform_name = platform.uname()[0]
    if platform_name == "Windows":
        return name + ".dll"
    elif platform_name == "Linux":
        return "lib" + name + ".so"
    else:
        raise BrainAccessException(f'Unsupported platform "{platform_name}"')


def load_library(name: str) -> ctypes.CDLL:
    dll_name = get_lib_name(name)
    try:
        onlyfiles = [file.name for file in pathlib.Path(getcwd()).glob("*")]
        if dll_name in onlyfiles:
            return ctypes.CDLL(join(getcwd(), dll_name))
        onlyfiles = [file.name for file in _lib_directory.glob("*")]
        if dll_name in onlyfiles:
            return ctypes.CDLL(join(_lib_directory, dll_name))
        _lib = find_library(dll_name)
        if _lib:
            return ctypes.CDLL(_lib)
        lib = which(dll_name)
        if lib:
            return ctypes.CDLL(lib)
        raise BrainAccessException("Could not find " + dll_name)
    except OSError:
        raise BrainAccessException("Could not load " + dll_name)
    except Exception as e:
        raise BrainAccessException("Could not load " + dll_name + " " + str(e))
