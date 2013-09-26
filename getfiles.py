import os
class GetFiles:
	def __init__(self,dir_name,config_params):
		self.dir_name = dir_name
		self.config = config_params
		self.matches = []
		self.current_path = dir_name#os.getcwd()
		self.filemanip = FileManip(self.config)
	
	def get_all_files(self):
		if(self.filemanip.check_dir_in_local_path(self.current_path) == 0):
			for(dirname,dirshere,fileshere) in os.walk(self.current_path):
				pathname = dirname
				manip_file_path = self.filemanip.trim_ftp_path(pathname)
				local_ftp_path = self.filemanip.convert_filepath_ftp_path(pathname,manip_file_path)
				self.matches.append(local_ftp_path)
				for filename in fileshere:
					pathname = os.path.join(dirname,filename)
					manip_file_path = self.filemanip.trim_ftp_path(pathname)
					local_ftp_path = self.filemanip.convert_filepath_ftp_path(pathname,manip_file_path)
					self.matches.append(local_ftp_path)
		# print self.matches
		return self.matches

class FileManip:
	def __init__(self,config_params):
		self.config = config_params
		
	def check_dir_in_local_path(self,dirpth):
		return dirpth.find(self.config['FTP_WWW_LOCAL'].replace('/','\\'))
	
	def trim_ftp_path(self,filen):
		ftp_path_len = len(self.config['FTP_WWW_LOCAL'].replace('/','\\'))
		return filen[ftp_path_len:]
		
	def convert_filepath_ftp_path(self,acc_file_path,manip_file_path):
		locl_type = os.path.splitdrive(acc_file_path)[0]
		www_type = os.path.splitdrive(self.config['FTP_WWW_REMOTE'])[0]
		
		if(os.path.splitdrive(acc_file_path)[0] == ''):
			if www_type != '':
				manip_file_path = manip_file_path.replace('/','\\')
		else:
			if www_type == '':
				manip_file_path = manip_file_path.replace('\\','/')
				
		ftp_p = self.config['FTP_WWW_REMOTE']+manip_file_path
		ftp_p = ftp_p.replace('//','/')
		
		return (acc_file_path,ftp_p)
