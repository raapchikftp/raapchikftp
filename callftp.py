from clientftpsession import Clientftpsession
import os,sys
from notify import *
# from multiprocessing import Process, set_executable
from conn_zdb import CONN_ZDB
from ftp_error import *
from dbpaths import *
class Callftp:
	def __init__(self,files_detail):
		self.files_detail = files_detail[:-2]
		self.file_status = {}
		self.file_status['file_status'] = []
		self.file_status['new'] = []
		fresh_db = CONN_ZDB(DBPATH)
		fresh_dbroot = fresh_db.dbroot
		self.config = fresh_dbroot[files_detail[-2].replace("\\",'/')]
		self.action_type = files_detail[-1]
		fresh_db.close()

	def getFtpSession(self):
		try:
			clientsess = Clientftpsession(host=self.config['FTP_HOST'],port=self.config['FTP_PORT'],uname=self.config['FTP_USER'],upass=self.config['FTP_PASSW'],acv_pcv=self.config['FTP_ACV_PCV'])
			self.ftp_session = clientsess.getFtpSession(self.config['FTP_CON_TYPE'])
			for file_dtl in self.files_detail:
				if self.action_type == 'upld':
					file_status = self.try_upload_action(file_dtl[0][0],file_dtl[0][1])
				elif self.action_type == 'dwnld':
					file_status = self.try_download_action(file_dtl[0][0],file_dtl[0][1])
				else:
					sys.exit(1)
				self.file_status['file_status'].append((file_dtl[1],file_status))
			self.ftp_session.closeFTP()
			if self.action_type == 'dwnld':
				msg = 'Files downloaded successfully'
			else:
				msg = 'Files uploaded successfully'

			msg_sound = 'chick$'+str(self.config['FTP_PLAY_SOUND'])
			# p = Process(target=runftprocess, args=(msg,)).start()
			runftprocess((msg,))
			if str(self.config['FTP_PLAY_SOUND']) == '1':
				play_sound((msg_sound,))
				# p2 = Process(target=play_sound, args=(msg_sound,)).start()
			
			sys.exit(1)
		except FTP_ERROR as e:
			if str(self.config['FTP_PLAY_SOUND']) == '1':
				e.show_error('laugh$'+str(self.config['FTP_PLAY_SOUND']))
			sys.exit(1)
		
		
	def path_leaf(self,fpath):
		return os.path.split(fpath)
		
	def try_upload_action(self,lfile,rfile):
		import ftplib
		try:
			print lfile,rfile
			sts = self.ftp_session.uploadFileFTP(lFile=lfile,rFile=rfile)
			return True
		except (IOError, ftplib.error_perm):
			rDir = self.path_leaf(rfile[len(self.config['FTP_WWW_REMOTE']):])[0].split('/')#self.config['FTP_WWW_SEP'])
			dp = self.config['FTP_WWW_REMOTE']
			for d in rDir:
				try:
					dp = '/'.join([dp,d]).replace('//','/')
					self.ftp_session.makeDirFTP(dp)
					self.file_status['new'].append(dp)
				except (IOError, ftplib.error_perm):
					raise FTP_ERROR('FTP ERROR: Reasons\n\n (You dont have mkdir permission) \n\n (Files not found on server) \n(Internet connection) \n(Remote server down)\n (Config settings)')
				except ftplib.all_errors as e:
					pass
				except Exception as e:
					raise
					
			return self.try_upload_action(lfile,rfile)
		except:
			raise FTP_ERROR('FTP ERROR: Reasons\n\n (Files not found on server) \n(Internet connection) \n(Remote server down)\n (Config settings)')
			
	def try_download_action(self,rfile,lfile):
		try:
			sts = self.ftp_session.downloadFileFTP(rFile=rfile,lFile=lfile)
			return True
		except:
			raise FTP_ERROR('FTP ERROR: Reasons\n\n (Files not found on server) \n(Internet connection) \n(Remote server down)\n (Config settings)')
	
def runftprocess(args):
	import subprocess
	args = ["notify.exe", args]
	subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
