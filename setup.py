# from distutils.core import setup
# import py2exe, sys, os

# setup(
    # windows = ['smftp.py','smftpF.py','edit_config.py','callftp.py'],
    # zipfile = None,
	# options={"py2exe":{"includes": ["pkg_resources"]}}
# )

# import sys
# from cx_Freeze import setup, Executable

# executables = [
        # Executable("callftp.py"),
        # Executable("notify.py")
# ]

# buildOptions = dict(
        # compressed = True,
        # includes = ["callftp", "notify"],
        # path = sys.path + ["modules"])

# base = None
# if sys.platform == "win32":
    # base = "Win32GUI"

# setup(  name = "guifoo",
        # version = "0.1",
        # description = "My GUI application!",
        # options = {"build_exe": build_exe_options},
		# options = dict(build_exe = buildOptions),
        # executables = [Executable("smftp.py", base=base)])
		
# from distutils.core import setup
# setup(name='smftp',version='1.0',py_modules=['smftp'])
from distutils.core import setup
import py2exe

setup(windows=['smftp.py','notify.py','play_sound.py','smftpF.py','edit_config.py','entry_point.py','install_smftp.py','status.py','uninstall_smftp.py'])