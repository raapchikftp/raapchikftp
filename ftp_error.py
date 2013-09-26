# from multiprocessing import Process
import os
import tkMessageBox,Tkinter
from play_sound import *
class FTP_ERROR(Exception):
	def __init__(self, msg):
		self.msg = msg
	def show_error(self,soundparams):
		root = Tkinter.Tk()
		root.withdraw()
		# p = Process(target=play_sound, args=(soundparams,)).start()	
		play_sound((soundparams,))
		tkMessageBox.showerror('FTP ERROR',self.msg,parent=root)
		root.destroy()

def play_sound(args):
	import subprocess
	args = ["play_sound.exe", args]
	subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)