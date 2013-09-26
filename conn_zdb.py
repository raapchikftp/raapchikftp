import sqlite3
class CONN_ZDB(object):
	def __init__(self, path):
		self.db = sqlite3.connect(path)
		self.check_config_tb_created()
		self.dbroot = self.getalldbroot()

	def close(self):
		self.db.close()
		
	def commit(self,params):
		if 'FTP_ID' in params.keys():
			strn = '''UPDATE config_tbl SET
					FTP_CONN_NAME = '%s',
					FTP_HOST = '%s',
					FTP_PORT = %i,
					FTP_CON_TYPE = '%s',
					FTP_USER = '%s',
					FTP_PASSW = '%s',
					FTP_WWW_LOCAL = '%s',
					FTP_WWW_REMOTE = '%s',
					FTP_PLAY_SOUND = '%s', 
					FTP_ACV_PCV = '%s' 
					WHERE ID = %i ''' %(params['FTP_CONN_NAME'],params['FTP_HOST'],params['FTP_PORT'],params['FTP_CON_TYPE'],params['FTP_USER'],params['FTP_PASSW'],params['FTP_WWW_LOCAL'],params['FTP_WWW_REMOTE'],params['FTP_PLAY_SOUND'],params['FTP_ACV_PCV'],params['FTP_ID'])
		else:
			last_id = self.db.execute("SELECT ID FROM config_tbl ORDER BY ID DESC LIMIT 1")
			last_id = last_id.fetchone()
			if last_id == None:
				last_id = 1
			else:
				last_id = last_id[0]+1
			
			strn = '''INSERT INTO config_tbl
						(FTP_KEY,FTP_CONN_NAME,FTP_HOST,FTP_PORT,FTP_CON_TYPE,FTP_USER,FTP_PASSW,FTP_WWW_LOCAL,FTP_WWW_REMOTE,FTP_PLAY_SOUND,FTP_ACV_PCV) 
						VALUES 
						('%s','%s','%s',%i,'%s','%s','%s','%s','%s','%s','%s');''' %(params['FTP_WWW_LOCAL']+str(last_id),params['FTP_CONN_NAME'],params['FTP_HOST'],params['FTP_PORT'],params['FTP_CON_TYPE'],params['FTP_USER'],params['FTP_PASSW'],params['FTP_WWW_LOCAL'],params['FTP_WWW_REMOTE'],params['FTP_PLAY_SOUND'],params['FTP_ACV_PCV'])
		
		self.db.execute(strn)
		self.db.commit()
		
	def check_config_tb_created(self):
		tbl_exits = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config_tbl'")
		tbl_exits = tbl_exits.fetchone()
		if tbl_exits == None:
			self.db.execute('''CREATE TABLE config_tbl
				(ID INTEGER PRIMARY KEY NOT NULL,
				FTP_KEY TEXT NOT NULL,
				FTP_CONN_NAME TEXT NOT NULL,
				FTP_HOST TEXT NOT NULL,
				FTP_PORT INT NOT NULL,
				FTP_CON_TYPE TEXT NOT NULL,
				FTP_USER TEXT NOT NULL,
				FTP_PASSW TEXT NOT NULL,
				FTP_WWW_LOCAL TEXT NOT NULL,
				FTP_WWW_REMOTE TEXT NOT NULL,
				FTP_PLAY_SOUND TEXT NOT NULL,
				FTP_ACV_PCV TEXT NOT NULL);''')
			return True
		else:
			return True
	
	def getalldbroot(self):
		cursor = self.db.execute("SELECT * from config_tbl")
		data = {}
		if cursor == None:
			return data
		else:
			for row in cursor:
				nerw = {}
				nerw['FTP_ID'] = row[0]
				nerw['FTP_KEY'] = row[1]
				nerw['FTP_CONN_NAME'] = row[2]
				nerw['FTP_HOST'] = row[3]
				nerw['FTP_PORT'] = row[4]
				nerw['FTP_CON_TYPE'] = row[5]
				nerw['FTP_USER'] = row[6]
				nerw['FTP_PASSW'] = row[7]
				nerw['FTP_WWW_LOCAL'] = row[8]
				nerw['FTP_WWW_REMOTE'] = row[9]
				nerw['FTP_PLAY_SOUND'] = row[10]
				nerw['FTP_ACV_PCV'] = row[11]
				data.update({r''+row[1]:nerw})
			return data
	
	def getallkeys(self):
		cursor = self.db.execute("SELECT * from config_tbl")
		data = []
		if cursor == None:
			return data
		else:
			for row in cursor:
				data.append(r''+row[1])
			return data
			
	def deleterec(self,prms):
		self.db.execute('DELETE FROM config_tbl WHERE ID = '+str(prms['FTP_ID']))
		self.db.commit()