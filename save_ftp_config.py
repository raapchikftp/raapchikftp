from conn_zdb import CONN_ZDB
from dbpaths import *
from ftp_error import *
import subprocess
import sys
class save_ftp_config():
	def __init__(self,params,ky=''):
		try:
			if params['FTP_CONN_NAME'] == '' or params['FTP_HOST'] == '' or params['FTP_PORT'] == '' or params['FTP_CON_TYPE'] == '' or params['FTP_USER'] == '' or params['FTP_PASSW'] == '' or params['FTP_WWW_REMOTE'] == '' or params['FTP_WWW_LOCAL'] == '' or params['FTP_ACV_PCV'] == '':
				raise FTP_ERROR('Oops: Please dont leave any config parameter blank')
				
			import os,ntpath
			if os.path.splitext(ntpath.basename(params['FTP_WWW_REMOTE']))[-1] != '':
				raise FTP_ERROR('Please enter valid remote path')
				
			from clientftpsession import Clientftpsession
			clientsess = Clientftpsession(host=params['FTP_HOST'],port=params['FTP_PORT'],uname=params['FTP_USER'],upass=params['FTP_PASSW'],acv_pcv=params['FTP_ACV_PCV'])
			self.ftp_session = clientsess.getFtpSession(params['FTP_CON_TYPE'])
			# print "Dir listing RM"
			self.ftp_session.listDirFTP(params['FTP_WWW_REMOTE'])
			self.ftp_session.closeFTP()

			self.db = CONN_ZDB(DBPATH)
			self.dbroot = self.db.dbroot
			if ky != '':
				local_ftp_key = r''+ky
				edit_ky = self.dbroot[local_ftp_key]
			# else:
				# local_ftp_key = r''+params['FTP_KEY']
			edit_ky = params

			# self.dbroot[local_ftp_key] = edit_ky
			self.db.commit(edit_ky)
			self.db.close()
			if ky == '':
				args = ["notify.exe", ('FTP config added successfully',)]
			else:
				args = ["notify.exe", ('FTP config updated successfully',)]
			
			subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
			args = ["play_sound.exe", ('chick$'+str(params['FTP_PLAY_SOUND']),)]
			if str(params['FTP_PLAY_SOUND']) == '1':
				subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)

			sys.exit(1)
		except FTP_ERROR as e:
			args = ["play_sound.exe", ('laugh$'+str(params['FTP_PLAY_SOUND']),)]
			root = Tkinter.Tk()
			root.withdraw()
			if str(params['FTP_PLAY_SOUND']) == '1':
				subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
			tkMessageBox.showerror('FTP ERROR',e.msg,parent=root)
			root.destroy()
			
			# e.show_error('laugh$'+str(params['FTP_PLAY_SOUND']))
