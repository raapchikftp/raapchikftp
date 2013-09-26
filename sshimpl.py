import paramiko,os
from ftp_error import *
from processlogger import *
class Sshimpl():
	def __init__(self):
		self.log = ProcessLogger()
		
	def connectFTP(self,host='',port=22,uname='',upass='',ssh_host_key='',acv_pcv=''):
		if host=='' or port=='' or uname=='' or upass=='' or acv_pcv=='':
			raise FTP_ERROR('Blank config parameters, Please dont leave any config parameter blank')
		
		hostkeytype=None
		self.hostkey=None
		
		try:
			hostkeys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		except IOError:
			try:
				hostkeys = paramiko.util.load_host_keys(os.path.expanduser(r'~\ssh\known_hosts'))
			except IOError:
				hostkeys = {}
		if hostkeys.has_key(host):
			hostkeytype = hostkeys[host].keys()[0]
			self.hostkey = hostkeys[host][hostkeytype]
			
		self.host = host
		log_id = self.log.processlog(logid=0,f1=False,f2=False,hostnm=host,up_dw='login',typ='new',status='Pending',result='trying to connect...')
		try:
			trans = paramiko.Transport((host, int(port)))
			trans.connect(username=uname, password=upass, hostkey=self.hostkey)
			self.ftp = paramiko.SFTPClient.from_transport(trans)
			self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=host,up_dw='login',typ='edit',status='Done',result='connected successfully...')
		except Exception as e:
			self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=host,up_dw='login',typ='edit',status='Failed',result=str(e))
			raise FTP_ERROR('Connection error: Reasons \n\n(Internet connection) \n(Remote server down)\n (Config settings) \n Response: (%s)'%str(e))
		
	def uploadFileFTP(self,lFile='',rFile='',callbk=None):
		if lFile=='' or rFile=='':
			raise FTP_ERROR('SSH UPLOAD ERROR, Required parameters are missing...[CODE:1000]')
		log_id = self.log.processlog(logid=0,f1=lFile,f2=rFile,hostnm=self.host,up_dw='upload',typ='new',status='Pending',result='trying to upload...')
		upl = self.ftp.put(lFile,rFile)
		self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='upload',typ='edit',status='Done',result='uploaded successfully...')
		return upl
		# try:
			# upl = self.ftp.put(lFile,rFile)
			# self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='upload',typ='edit',status='Done',result='uploaded successfully...')
			# return upl
		# except Exception as e:
			# self.log.processlog(logid=log_id,f1=lFile,f2=lFile,hostnm=self.host,up_dw='upload',typ='edit',status='Failed',result=str(e))
			# raise FTP_ERROR('SSH UPLOAD ERROR, Please check internet connection... \n Response: (%s)'%str(e))
	
	def downloadFileFTP(self,rFile='',lFile='',callbk=None):
		if lFile=='' or rFile=='':
			raise FTP_ERROR('SSH DOWNLOAD ERROR, Required parameters are missing...[CODE:1001]')
		# self.ftp.get(rFile,lFile)
		log_id = self.log.processlog(logid=0,f1=lFile,f2=rFile,hostnm=self.host,up_dw='download',typ='new',status='Pending',result='trying to download...')
		self.ftp.get(rFile,lFile)
		self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='download',typ='edit',status='Done',result='uploaded successfully...')
		# try:
			# self.ftp.get(rFile,lFile)
			# self.log.processlog(logid=log_id,f1=lFile,f2=rFile,hostnm=self.host,up_dw='download',typ='edit',status='Done',result='uploaded successfully...')
		# except Exception as e:
			# self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=self.host,up_dw='download',typ='edit',status='Failed',result=str(e))
			# raise FTP_ERROR('SSH DOWNLOAD ERROR, Please check internet connection... \n Response: (%s)'%str(e))
		
	def chmodFileFTP(self,rFile='',cmod='',callbk=None):
		if rFile=='' or cmod=='':
			raise FTP_ERROR('SSH CHMOD ERROR, Required parameters are missing...[CODE:1002]')
		try:
			self.ftp.chmod(rFile,cmod)
		except:
			raise FTP_ERROR('SSH CHMOD ERROR, You dont have permission to change...')
		
	def deleteFileFTP(self,rFile='',callbk=None):
		if rFile=='':
			raise FTP_ERROR('SSH DELETE ERROR, Required parameters are missing...[CODE:1003]')
		try:
			self.ftp.remove(rFile)
		except:
			raise FTP_ERROR('SSH DELETE ERROR, Please check internet connection and permission to delete')
		
	def makeDirFTP(self,rPath,callbk=None):
		if rPath=='':
			raise FTP_ERROR('SSH MKDIR ERROR, Required parameters are missing...[CODE:1004]')
		log_id = self.log.processlog(logid=0,f1=rPath,f2=False,hostnm=self.host,up_dw='mkdir',typ='new',status='Pending',result='creating directory...')
		try:
			self.ftp.mkdir(rPath)
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='mkdir',typ='edit',status='Done',result='dir created successfully')
		except Exception as e:
			# print 'printing in ,djbdjs '+str(e)
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='mkdir',typ='edit',status='Failed',result=str(e))
			if str(e) == 'Failure':
				pass
			else:
				raise FTP_ERROR('SSH MKDIR ERROR, Please check internet connection and permission to mkdir, \n Response: (%s)'%str(e))
			
	def listDirFTP(self,rPath,callbk=None):
		if rPath=='':
			raise FTP_ERROR('SSH LIST DIR ERROR, Required parameters are missing...[CODE:1005]')
		log_id = self.log.processlog(logid=0,f1=rPath,f2=False,hostnm=self.host,up_dw='ls',typ='new',status='Pending',result='listing directory...')
		try:
			files_list = self.ftp.listdir(rPath)
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='ls',typ='edit',status='Done',result='list directory successfully...')
			return files_list
		except Exception as e:
			self.log.processlog(logid=log_id,f1=rPath,f2=False,hostnm=self.host,up_dw='ls',typ='edit',status='Failed',result=str(e))
			# raise FTP_ERROR('Config parameters error, Please cross check remote dir path...')
	
	def closeFTP(self):
		log_id = self.log.processlog(logid=0,f1=False,f2=False,hostnm=self.host,up_dw='login',typ='new',status='Pending',result='trying to disconnect...')
		self.ftp.close()
		self.log.processlog(logid=log_id,f1=False,f2=False,hostnm=self.host,up_dw='login',typ='edit',status='Done',result='disconnected successfully...')