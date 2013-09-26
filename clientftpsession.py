from ftp_error import *
class Clientftpsession:
	def __init__(self,host='',port='',uname='',upass='',ssh_host_key='',acv_pcv=''):
		if host=='' or port=='' or uname=='' or upass=='' or acv_pcv =='':
			raise FTP_ERROR('Oops: Blank config parameters, Please dont leave any config parameter blank')
			
		self.host = host
		self.port = port
		self.uname = uname
		self.upass = upass
		self.ssh_host_key = ssh_host_key
		self.acv_pcv = acv_pcv
		
	def getFtpSession(self,type_ftp):
		ft = None
		if type_ftp == 'FTP':
			from ftpimpl import Ftpimpl
			ft = Ftpimpl()
		elif type_ftp == 'SFTP':
			from sftpimpl import Sftpimpl
			ft = Sftpimpl()
		elif type_ftp == 'SSH':
			from sshimpl import Sshimpl
			ft = Sshimpl()
		
		if ft != None:
			ft.connectFTP(self.host,self.port,self.uname,self.upass,self.ssh_host_key,self.acv_pcv)
		
		return ft