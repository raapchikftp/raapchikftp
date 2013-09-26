import sys, os
from conn_zdb import CONN_ZDB
from tkFileDialog import askdirectory
from ftp_error import *
from dbpaths import *
class Config:
	def __init__(self,path):
		self.config_params = []
		self.local_ftp_path = path
		self.check_config_exits(path)
			
	def check_config_exits(self,path):
		if not os.path.exists(CONFIG_BASE):
			os.makedirs(CONFIG_BASE)
		
		connection = CONN_ZDB(DBPATH)
		root = connection.getalldbroot()
		config_keys = connection.getallkeys()
		path = r''+path
		path = path.replace("\\",'/')
		if config_keys:
			for config_name in config_keys:
				if path.find(config_name[:-1]) == 0:
					self.config_params.append(root[config_name])
		connection.close()
	
	def get_config_params(self):
		return self.config_params
		
	def create_frame(self):
		from config_design import CONFIG_DESIGN
		cd = CONFIG_DESIGN()