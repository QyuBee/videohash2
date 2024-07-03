import os
import sys
import importlib.util
import shutil
import tempfile
from pathlib import Path

currentDir = os.path.dirname(sys.executable)
modDir = currentDir + "\Tools\scripts\win_add2path.py"
spec = importlib.util.spec_from_file_location("add2path", modDir)
add2path = importlib.util.module_from_spec(spec)
sys.modules["add2path"] = add2path
spec.loader.exec_module(add2path)

add2path.main()

import requests
from pyunpack import Archive

cwd = os.getcwd()

temp_folder = os.path.join(tempfile.mkdtemp(), ("temp_storage_dir%s" % os.path.sep))
Path(temp_folder).mkdir(parents=True, exist_ok=True)

ffmpeg_7z_path = os.path.join(temp_folder, "ffmpeg_full.7z")
with open(ffmpeg_7z_path, "wb") as fd:
    fd.write(
        requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z").content
    )
Archive(ffmpeg_7z_path).extractall(temp_folder)
for file in os.listdir(temp_folder):
    if "build" and "ffmpeg" in file:
        shutil.copyfile(
            os.path.join(
                os.path.join(temp_folder, (file + os.path.sep)), "bin", "ffmpeg.exe"
            ),
            os.path.join(cwd, "ffmpeg.exe"),
        )
        shutil.copyfile(
            os.path.join(
                os.path.join(temp_folder, (file + os.path.sep)), "bin", "ffprobe.exe"
            ),
            os.path.join(cwd, "ffprobe.exe"),
        )
        break

shutil.rmtree(temp_folder, ignore_errors=True, onerror=None)
