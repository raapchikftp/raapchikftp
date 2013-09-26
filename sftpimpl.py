from ftpimpl import Ftpimpl
from ftplib import FTP_TLS
from processlogger import *
class Sftpimpl(Ftpimpl):
	def __init__(self):
		self.log = ProcessLogger()
	def connectFTP(self,host='',port='',uname='',upass='',ssh_host_key='',acv_pcv=''):
		if host=='' or port=='' or uname=='' or upass=='':
			raise FTP_ERROR('Oops: Blank config parameters, Please dont leave any config parameter blank')
		self.host = host
		log_id = self.log.processlog(logid=0,f1=False,f2=False,hostnm=host,up_dw='login',typ='new',status='Pending',result='trying to connect...')
		hostStr = '%s:%s' %(host,port)
		usrHostStr = '%s@%s' %(uname,hostStr)
		try:
			self.ftp = FTP_TLS(hostStr)
			if acv_pcv == 'Active':
				self.ftp.set_pasv(False)
			elif acv_pcv == 'Passive':
				self.ftp.set_pasv(True)
				
			self.ftp.login(uname,upass)
			self.ftp.prot_p()
			return_msg = self.ftp.getwelcome()
			self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=host,up_dw='login',typ='edit',status='Done',result=return_msg)
		except Exception as e:
			self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=host,up_dw='login',typ='edit',status='Failed',result=str(e))
			raise FTP_ERROR('Connection error: Reasons \n\n(Internet connection)\n(Remote server down)\n(Config settings) ')
		