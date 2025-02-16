#!/usr/bin/python3
import os
import sys
import shutil
import subprocess
import time
import glob

# usage: script.py linux64 folder_name project_name project_version project_path build_path


print(sys.argv)
print(os.getcwd())
print(os.name)
_platform = sys.argv[1]
_folder_name = sys.argv[2]  # gh-project
_project_name = sys.argv[3]  # project
_project_version = sys.argv[4]  # v1.0
_project_path = sys.argv[5]  # /gh/project
_build_path = sys.argv[6]  # /gh/project/build

_resource_path = os.path.join(_project_path, "resource")

if __name__ == "__main__":

    title = f"{_project_name} {_project_version}"
    script = os.path.abspath(__file__)
    scripts_project_path = os.path.split(os.path.split(script)[0])[0]
    tool_linuxdeployqt_project_path = os.path.join(os.path.split(scripts_project_path)[0], "tool-linuxdeployqt", )
    linuxdeployqt_path = os.path.join(tool_linuxdeployqt_project_path, "linuxdeployqt-continuous-x86_64.AppImage")
    if not os.path.isdir(os.path.join(scripts_project_path, "make-output")):
        sys.exit(0)

    package_dirpath = os.path.join(_project_path, "output", _project_name)
    if os.path.isdir(package_dirpath):
        shutil.rmtree(package_dirpath)
    time.sleep(2)
    try:
        os.makedirs(package_dirpath)
    except Exception as e:
        print(str(e))

    _build_output = []
    if _platform in ("linux64",):
        _build_output.append(os.path.join(_build_path, f"{_project_name}"))
    elif _platform in ("win32msvc", "win32mingw",):
        if _platform in ("win32msvc",):
            _build_output.append(os.path.join(_build_path, f"{_project_name}.exe"))
        elif _platform in ("win32mingw",):
            _build_output.append(os.path.join(_build_path, f"{_project_name}.exe"))
    else:
        raise ValueError(str(_platform))
    for i in _build_output:
        shutil.copy(i, package_dirpath)

    time.sleep(1)
    package_softpath = os.path.join(package_dirpath, os.path.split(_build_output[0])[1])
    os.chdir(package_dirpath)
    if os.name == "nt":
        os.system(r"set PATH=C:\Qt\5.15.2\msvc2019\bin;%PATH%")
        os.system(r"C:\Qt\5.15.2\msvc2019\bin\windeployqt.exe " + package_softpath)
    else:
        os.system(f"chmod +x {linuxdeployqt_path}")
        os.system(f"""export PATH=/home/m/Qt/5.15.2/gcc_64/bin:$PATH
export LD_LIBRARY_PATH=/home/m/Qt/5.15.2/gcc_64/lib:$LD_LIBRARY_PATH
export QT_PLUGIN_PATH=/home/m/Qt/5.15.2/gcc_64/plugins:$QT_PLUGIN_PATH
export QML2_IMPORT_PATH=/home/m/Qt/5.15.2/gcc_64/qml:$QML2_IMPORT_PATH
{linuxdeployqt_path} {package_softpath} -appimage -unsupported-allow-new-glibc -no-translations -no-copy-copyright-files""")
    if os.name == "nt":
        pass
    else:
        with open(os.path.join(tool_linuxdeployqt_project_path, "linux.desktop"), "r", encoding="utf8") as f1:
            with open(os.path.join(package_dirpath, f"{_project_name}.desktop"), "w", encoding="utf8") as f2:
                f2.write(f1.read().replace("application", _project_name))
        shutil.copy(os.path.join(_resource_path, "icon", "main.ico"),
                    os.path.join(package_dirpath, f"{_project_name}.ico"))
    _li = []
    if os.name == "nt":
        _li.append(os.path.join(package_dirpath, "translations"))
        _li.append(os.path.join(package_dirpath, "D3Dcompiler_47.dll"))
        _li.append(os.path.join(package_dirpath, "libEGL.dll"))
        _li.append(os.path.join(package_dirpath, "libGLESv2.dll"))
        _li.append(os.path.join(package_dirpath, "opengl32sw.dll"))
        _li.append(os.path.join(package_dirpath, "vc_redist.x86.exe"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qgif.dll"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qicns.dll"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qjpeg.dll"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qtga.dll"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qtiff.dll"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qwbmp.dll"))
        _li.append(os.path.join(package_dirpath, "imageformats", "qwebp.dll"))
    else:
        _li.append(os.path.join(package_dirpath, "AppRun"))
        _li.append(os.path.join(package_dirpath, "default.desktop"))
        _li.append(os.path.join(package_dirpath, "default.png"))
        _li.append(os.path.join(package_dirpath, "lib", "libgdk-3.so.0"))
        _li.append(os.path.join(package_dirpath, "lib", "libgtk-3.so.0"))
        _li.append(os.path.join(package_dirpath, "lib", "libQt5QmlModels.so.5"))
        _li.append(os.path.join(package_dirpath, "lib", "libQt5Quick.so.5"))
        _li.append(os.path.join(package_dirpath, "lib", "libQt5QuickTemplates2.so.5"))
        _li.append(os.path.join(package_dirpath, "lib", "libQt5VirtualKeyboard.so.5"))
    for i in _li:
        if os.path.isfile(i):
            os.remove(i)
        elif os.path.isdir(i):
            shutil.rmtree(i)
    with open(os.path.join(package_dirpath, "version.txt"), "w", encoding="utf8") as f:
        f.write(title)
    print("ok.")
