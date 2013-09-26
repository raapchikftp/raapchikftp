from ftplib import FTP
from ftp_error import *
from processlogger import *
class Ftpimpl():
	def __init__(self):
		self.log = ProcessLogger()
		
	def connectFTP(self,host='',port=21,uname='',upass='',ssh_host_key='',acv_pcv=''):
		if host=='' or port=='' or uname=='' or upass=='':
			raise FTP_ERROR('Oops: Blank config parameters, Please dont leave any config parameter blank')
		hostStr = 'ftp.%s:%s' %(host,port)
		usrHostStr = '%s' %uname
		self.host = host
		log_id = self.log.processlog(logid=0,f1=False,f2=False,hostnm=host,up_dw='login',typ='new',status='Pending',result='trying to connect...')
		try:
			self.ftp = FTP('ftp.'+host)
			if acv_pcv == 'Active':
				self.ftp.set_pasv(False)
			elif acv_pcv == 'Passive':
				self.ftp.set_pasv(True)
			self.ftp.login(usrHostStr,upass)
			return_msg = self.ftp.getwelcome()
			self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=host,up_dw='login',typ='edit',status='Done',result=return_msg)
		except Exception as e:
			self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=host,up_dw='login',typ='edit',status='Failed',result=str(e))
			raise FTP_ERROR('Connection error: Reasons \n\n(Internet connection) \n(Remote server down)\n (Config settings) \n Response: (%s)'%str(e))
		
	def uploadFileFTP(self,lFile='',rFile='',callbk=None):
		if lFile=='' or rFile=='':
			raise FTP_ERROR('FTP UPLOAD ERROR, Required parameters are missing...[CODE:2000]')
		# return (rFile,lFile)
		log_id = self.log.processlog(logid=0,f1=lFile,f2=rFile,hostnm=self.host,up_dw='upload',typ='new',status='Pending',result='trying to upload...')
		upl = self.ftp.storbinary('STOR '+rFile, open(lFile, 'rb'))
		self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='upload',typ='edit',status='Done',result='uploaded successfully...')
		return upl
		# try:
			# upl = self.ftp.storbinary('STOR '+rFile, open(lFile, 'rb'))
			# self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='upload',typ='edit',status='Done',result='uploaded successfully...')
			# return upl
		# except Exception as e:
			# self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=self.host,up_dw='upload',typ='edit',status='Failed',result=str(e))
			# raise FTP_ERROR('FTP UPLOAD ERROR, Please check internet connection... \n Response: (%s)'%str(e))
			
	def downloadFileFTP(self,rFile='',lFile='',callbk=None):
		if lFile=='' or rFile=='':
			raise FTP_ERROR('FTP DOWNLOAD ERROR, Required parameters are missing...[CODE:2001]')
		# print 'iam inside'
		log_id = self.log.processlog(logid=0,f1=lFile,f2=rFile,hostnm=self.host,up_dw='download',typ='new',status='Pending',result='trying to download...')
		self.ftp.retrbinary('RETR '+rFile, open(lFile, 'wb').write)
		self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='download',typ='edit',status='Done',result='downloaded successfully...')
		# try:
			# self.ftp.retrbinary('RETR '+rFile, open(lFile, 'wb').write)
			# self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='download',typ='edit',status='Done',result='downloaded successfully...')
		# except Exception as e:
			# self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=self.host,up_dw='download',typ='edit',status='Failed',result=str(e))
			# raise FTP_ERROR('FTP DOWNLOAD ERROR, Please check internet connection... \n Response: (%s)'%str(e))
		
	def chmodFileFTP(self,rFile='',cmod='',callbk=None):
		if rFile=='' or cmod=='':
			raise FTP_ERROR('FTP CHMOD ERROR, Required parameters are missing...[CODE:2002]')
		try:
			self.ftp.sendcmd('chmod % %'%(rFile,cmod))
		except:
			raise FTP_ERROR('FTP CHMOD ERROR, You dont have permission to change...')
		
	def deleteFileFTP(self,rFile='',callbk=None):
		if rFile=='':
			raise FTP_ERROR('FTP DELETE ERROR, Required parameters are missing...[CODE:2003]')
		try:
			self.ftp.delete(rFile)
		except:
			raise FTP_ERROR('FTP DELETE ERROR, Please check internet connection and permission to delete')
		
	def makeDirFTP(self,rPath,callbk=None):
		if rPath=='':
			raise FTP_ERROR('FTP MKDIR ERROR, Required parameters are missing...[CODE:2004]')
		log_id = self.log.processlog(logid=0,f1=rPath,f2=False,hostnm=self.host,up_dw='mkdir',typ='new',status='Pending',result='creating directory...')
		try:
			self.ftp.mkd(rPath)
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='mkdir',typ='edit',status='Done',result='dir created successfully')
		except Exception as e:
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='mkdir',typ='edit',status='Failed',result=str(e))
			cod = str(e).split(' ')
			# print cod
			# if cod[0] == '550':
			if '550' in cod[0]:
				pass
			else:
				raise FTP_ERROR('FTP MKDIR ERROR, Please check internet connection and permission to mkdir \n Response: (%s)'%str(e))
		
	def listDirFTP(self,rPath,callbk=None):
		if rPath=='':
			raise FTP_ERROR('SSH LIST DIR ERROR, Required parameters are missing...[CODE:2005]')
		log_id = self.log.processlog(logid=0,f1=rPath,f2=False,hostnm=self.host,up_dw='ls',typ='new',status='Pending',result='listing directory...')
		try:
			files_list = self.ftp.nlst(rPath)
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='ls',typ='edit',status='Done',result='list directory successfully...')
			return files_list
		except Exception as e:
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='ls',typ='edit',status='Failed',result='Listing dir exception')
			raise FTP_ERROR('FTP LISTING ERROR, Please check internet connection and also check connection type in config...')
		# if len(files_list) <= 0:
			# raise FTP_ERROR('Config parameters error, Please cross check remote dir path...')
		
	
	def closeFTP(self):
		log_id = self.log.processlog(logid=0,f1=False,f2=False,hostnm=self.host,up_dw='login',typ='new',status='Pending',result='trying to disconnect...')
		self.ftp.close()
		self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=self.host,up_dw='login',typ='edit',status='Done',result='disconnected successfully...')
	