import sqlite3
from dbpaths import *
class ProcessLogger():
	def __init__(self):
		self.db = sqlite3.connect(LOGPATH)
		self.chk_prcloggr_exits()
		
	def processlog(self,logid=0,f1=False,f2=False,hostnm=False,up_dw=False,typ='new',status='Pending',result=False):
		if typ == 'new':
			# sql_str = "INSERT INTO prcloggr (log_id,crtd_ti,f1,f2,hnm,tp,sts,result) VALUES (null,datetime('now', 'localtime'),'%s','%s','%s','%s','%s','%s')"%(f1,f2,hostnm,up_dw,status,result)
			cur = self.db.cursor()
			cur.execute("INSERT INTO prcloggr (log_id,crtd_ti,f1,f2,hnm,tp,sts,result) VALUES (null,datetime('now', 'localtime'),?,?,?,?,?,?)",(f1,f2,hostnm,up_dw,status,result))
			self.db.commit()
			lst_id = cur.lastrowid
			return lst_id
		else:
			if logid != 0:
				# sql_str = "UPDATE prcloggr set sts = ?, result=? WHERE log_id = ?", (status,result,logid)
				# print sql_str
				cur = self.db.cursor()
				cur.execute("UPDATE prcloggr set sts = ?, result=? WHERE log_id = ?", (status,result,logid))
				self.db.commit()
				return True
			return False
	
	def get_process_Q(self,dt):
		sql_str = "SELECT * FROM prcloggr WHERE date(crtd_ti) = %s"%dt
		# sql_str = "SELECT * FROM prcloggr WHERE crtd_ti = date('now', 'localtime')"
		cur = self.db.cursor()
		cur.execute(sql_str)
		rows = cur.fetchall()
		return rows
		
	def chk_prcloggr_exits(self):
		sql_str = "SELECT name FROM sqlite_master WHERE type='table' AND name='prcloggr'"
		cur = self.db.execute(sql_str)
		row = cur.fetchone()
		if row == None:
			sql_str = '''CREATE TABLE prcloggr (
						log_id INTEGER PRIMARY KEY,
						crtd_ti DATETIME NULL,
						f1 VARCHAR(250) NULL,
						f2 VARCHAR(250) NULL,
						hnm VARCHAR(250) NULL,
						tp VARCHAR(10) NULL,
						sts VARCHAR(10) NULL,
						result TEXT NULL
						)'''
			self.db.execute(sql_str)
		
	def close_db(self):
		self.db.close()

if __name__ == '__main__':
	log = ProcessLogger()
	recd = log.get_process_Q("DATE('now','localtime')")
	# print recd
	log.close_db()