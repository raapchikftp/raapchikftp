from clientftpsession import Clientftpsession
from getfiles import FileManip
from ftp_error import *
import sys
import os
class GetRmtFiles:
	def __init__(self,dir_name,config_params):
		self.dir_name = dir_name
		self.config = config_params
		self.matches = []
		self.current_path = dir_name#os.getcwd()
		self.filemanip = FileManip(self.config)
	
	def get_all_files(self):
		manip_file_path = self.filemanip.trim_ftp_path(self.current_path)
		rmt_dir = self.filemanip.convert_filepath_ftp_path(self.current_path,manip_file_path)
		# print rmt_dir
		try:
			clientsess = Clientftpsession(host=self.config['FTP_HOST'],port=self.config['FTP_PORT'],uname=self.config['FTP_USER'],upass=self.config['FTP_PASSW'],acv_pcv=self.config['FTP_ACV_PCV'])
			self.ftp_session = clientsess.getFtpSession(self.config['FTP_CON_TYPE'])
			rmt_files = self.ftp_session.listDirFTP(rmt_dir[1])
			# print rmt_files
			self.ftp_session.closeFTP()
			path_sepr = '/' if os.path.splitdrive(manip_file_path)[0] == '' else '\\'
			self.current_path = self.current_path.replace('/','\\');
			local_path_sepr = '\\' if os.path.splitdrive(self.current_path)[0] != '' else '/'
			rmt_files = [self.filemanip.convert_filepath_ftp_path(self.current_path + local_path_sepr + (x[len(rmt_dir[1])+1:] if x[0:len(rmt_dir[1])] == rmt_dir[1] else x) , manip_file_path + path_sepr + (x[len(rmt_dir[1])+1:] if x[0:len(rmt_dir[1])] == rmt_dir[1] else x)) for x in rmt_files]
			rmt_files = [(x[1],x[0]) for x in rmt_files]
			return rmt_files
		except FTP_ERROR as e:
			if str(self.config['FTP_PLAY_SOUND']) == '1':
				e.show_error('laugh$'+str(self.config['FTP_PLAY_SOUND']))
			sys.exit(1)