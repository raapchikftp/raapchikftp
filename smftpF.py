# from smftp import runftprocess
import sys
import uuid
from multiprocessing import Process, freeze_support
from getfiles import FileManip
from conn_zdb import CONN_ZDB
from dbpaths import *
from config import *
from Tkinter import *
from callftp import Callftp
def process_files(fls,config_params,action_type):
	process_fls = []
	fm = FileManip(config_params)
	manip_file_path = fm.trim_ftp_path(fls)
	if action_type == 'upld':
		local_ftp_path = fm.convert_filepath_ftp_path(fls,manip_file_path)
	elif action_type == 'dwnld':
		local_ftp_path = fm.convert_filepath_ftp_path(fls,manip_file_path)
		local_ftp_path = (local_ftp_path[1],local_ftp_path[0])
	else:
		sys.exit(1)
		
	process_fls.append((local_ftp_path,0))	
	rd_uuid = str(uuid.uuid4())
	process_fls.append(config_params['FTP_KEY'])
	process_fls.append(action_type)
	
	call_ftp = Callftp(process_fls)
	call_ftp.getFtpSession()
	sys.exit(1)
	

if __name__ == '__main__':
	freeze_support()
	upld_or_dwnl = sys.argv[2]
	config = Config(r''+sys.argv[1])
	config_params = config.get_config_params()
	# print config_params
	if len(config_params) <= 0:
		from config_design import CONFIG_DESIGN
		root = Tk()
		root.withdraw()
		cd = CONFIG_DESIGN(ky='',eparams='')
	else:
		config_index = 0
		if len(config_params) > 1:
			from tkSimpleDialog import askinteger
			root = Tk()
			root.withdraw()
			msg = 'Select FTP Server \n\n'
			x = 1
			for host_name in config_params:
				msg += str(x) + ' : HOST >> [ ' + host_name['FTP_HOST'] + ' ]\n'
				x = x + 1
				
			newint = askinteger('Select FTP', msg,initialvalue=1,parent=root,minvalue=1,maxvalue=len(config_params))
			root.destroy()
			if newint == None:
				config_index = 0
			else:
				config_index = newint-1
		# print config_params[config_index]['FTP_WWW_LOCAL']
		process_files(r''+sys.argv[1],config_params[config_index],sys.argv[2])