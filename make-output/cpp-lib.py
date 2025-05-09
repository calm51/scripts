import os, sys, re
import shutil
import time

cwd = os.path.dirname(os.path.abspath(__file__))


def _copytree_h_file(dir, files):
    l = []
    for file in files:
        _abs_path = os.path.join(dir, file)
        if os.path.isfile(_abs_path):
            if not file.endswith('.h'):
                l.append(file)
    return l


# usage: script.py linux64 folder_name project_name project_path build_path


print(sys.argv)
print(os.getcwd())
print(os.name)
_platform = sys.argv[1]
_folder_name = sys.argv[2]  # gh-project
_project_name = sys.argv[3]  # project
_project_path = sys.argv[4]  # /gh/project
_build_path = sys.argv[5]  # /gh/project/build

if __name__ == "__main__":
    if _platform not in (
            "linux32", "linux64",
            "win32msvc", "win32mingw", "win64msvc", "win64mingw",
            "darwin",
            "android",
    ): raise ValueError(str(_platform))

    if (not os.path.isfile(os.path.join(_project_path, "CMakeLists.txt")) or
            not os.path.isdir(os.path.join(_project_path, "src"))):
        raise ValueError(_project_path)

    _project_path = os.path.abspath(_project_path)
    _src_path = os.path.abspath(os.path.join(_project_path, "src"))
    _output_path = os.path.abspath(os.path.join(_project_path, "output"))
    _bin_path = os.path.abspath(os.path.join(_output_path, "bin"))
    _include_path = os.path.abspath(os.path.join(_output_path, "include"))
    _lib_path = os.path.abspath(os.path.join(_output_path, "lib", ))
    if os.path.exists(_include_path): shutil.rmtree(_include_path)

    _include_path = os.path.join(_include_path, _project_name)
    if _platform in ("linux32",):
        _lib_path = os.path.join(_lib_path, "linux32")
    elif _platform in ("linux64",):
        _lib_path = os.path.join(_lib_path, "linux64")
    elif _platform in ("win32msvc",):
        _lib_path = os.path.join(_lib_path, "win32msvc")
    elif _platform in ("win32mingw",):
        _lib_path = os.path.join(_lib_path, "win32mingw")
    elif _platform in ("win64msvc",):
        _lib_path = os.path.join(_lib_path, "win64msvc")
    elif _platform in ("win64mingw",):
        _lib_path = os.path.join(_lib_path, "win64mingw")
    elif _platform in ("darwin",):
        _lib_path = os.path.join(_lib_path, "macos")
    elif _platform in ("android",):
        _lib_path = os.path.join(_lib_path, "android")
    _lib_path = os.path.join(_lib_path, _project_name)

    time.sleep(0.5)
    os.makedirs(_lib_path, exist_ok=True)
    os.makedirs(_include_path)
    shutil.copytree(_src_path, _include_path, dirs_exist_ok=True, ignore=_copytree_h_file)

    _build_output = []
    if _platform in ("linux64",):
        _build_output.append(os.path.join(_build_path, f"lib{_project_name}.so"))
    elif _platform in ("win32msvc", "win32mingw",):
        if _platform in ("win32msvc",):
            _build_output.append(os.path.join(_build_path, f"{_project_name}.dll"))
            _build_output.append(os.path.join(_build_path, f"{_project_name}.lib"))
        elif _platform in ("win32mingw",):
            _build_output.append(os.path.join(_build_path, f"lib{_project_name}.dll"))
            # _build_output.append(os.path.join(_build_path, f"lib{_project_name}.dll.a"))
    elif _platform in ("android",):
        _path = os.path.join(_build_path, "android-build", "libs", "armeabi-v7a", f"lib{_project_name}_armeabi-v7a.so")
        if not os.path.isfile(_path):
            _path = os.path.join(_build_path, f"lib{_project_name}.so")
        _build_output.append(_path)
    else:
        raise ValueError(str(_platform))
    for i in _build_output:
        shutil.copy(i, _lib_path)
