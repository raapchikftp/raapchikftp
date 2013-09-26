from conn_zdb import CONN_ZDB
from dbpaths import *
from Tkinter import *
import sys
import tkMessageBox
import logging
import tkFont
class edit_config():
	def __init__(self,parent=None):
		logging.basicConfig()
		self.root = Tk()
		self.root.wm_resizable(0,0)
		self.root.wm_title(":::: RaapCHIK :::")
		# self.root.wm_iconbitmap(bitmap='favicon.gif')
		self.root.protocol('WM_DELETE_WINDOW', self.closesmftp)
		self.fbolder = tkFont.Font(weight='bold',size=9,slant='italic')
		self.fitalic = tkFont.Font(slant='italic',size=9)
		addbtn = Button(self.root,text='Add New', font=self.fbolder, command=self.addnewftp,background='thistle',height=2)
		addbtn.pack(side="bottom",fill="both")
		
		# addbtn = Button(self.root,text='Status', font=self.fbolder, command=self.show_status,background='thistle',height=2)
		# addbtn.pack(side="bottom",fill="both")
		
		hdr_frame = Frame(self.root,background='thistle')
		ebtn = Label(hdr_frame,text='Host',font=self.fbolder, anchor=W,width=42,background='thistle',height=2,padx=10)
		dbtn = Label(hdr_frame,text='Edit',font=self.fbolder, anchor=CENTER,width=14,background='thistle',height=2)
		labl = Label(hdr_frame,text='Delete',font=self.fbolder, anchor=E,background='thistle',height=2)
		ebtn.grid(row=0,column=0)
		dbtn.grid(row=0,column=1)
		labl.grid(row=0,column=2)
		
		hdr_frame.pack(side="top",fill="both")
		
		if True:
			self.canvas = Canvas(self.root,width=500,height=200)
			self.frame = Frame(self.canvas)
			self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
			self.canvas.configure(yscrollcommand=self.vsb.set)
			self.vsb.pack(side="right", fill="y")
			self.canvas.pack(side="left", fill="both", expand=True)
			self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
			self.frame.bind("<Configure>", self.OnFrameConfigure)
			
			self.make_ftp_form()
			self.canvas.focus()
			self.canvas.pack()
		else:
			self.root.withdraw()
			tkMessageBox.showerror(':::Config:::',"Zero FTP setting found",parent=self.root)
			self.root.destroy()
			sys.exit(1)
		self.root.mainloop()
		
	def closesmftp(self):
		sys.exit(1)
		
	def OnFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		
	def make_ftp_form(self):
		if True:
			fresh_db = CONN_ZDB(DBPATH)
			row = 1
			for key in fresh_db.dbroot.keys():
				lbl_text = '%s [%s]' % (fresh_db.dbroot[key]['FTP_CONN_NAME'], fresh_db.dbroot[key]['FTP_HOST'])
				labl = Label(self.frame,text=lbl_text,anchor=NW,width=45,wraplength=350)
				ebtn = Button(self.frame,text='Edit',font=self.fitalic, command=lambda key=key: self.edit_frame(key),anchor=N,width=10)
				dbtn = Button(self.frame,text='Delete',font=self.fitalic, width=10)
				labl.grid(row=row,column=0)
				ebtn.grid(row=row,column=1)
				dbtn.grid(row=row,column=2)
				dbtn.config(command=lambda labl=labl,ebtn=ebtn,dbtn=dbtn,key=key: self.del_frame(labl,ebtn,dbtn,key))
				row += 1
			fresh_db.close()
				
	def edit_frame(self,ky):
		from config_design import CONFIG_DESIGN
		fresh_db = CONN_ZDB(DBPATH)
		fresh_dbroot = fresh_db.dbroot
		eparams=fresh_dbroot[ky]
		fresh_db.close()
		root = Tk()
		root.withdraw()
		cd = CONFIG_DESIGN(ky=ky,eparams=eparams,e_sec=1)
	
	def del_frame(self,i1,i2,i3,ky):
		result = tkMessageBox.askquestion("Delete", "Are You Sure?", icon='warning')
		if result == 'yes':
			i1.grid_remove()
			i2.grid_remove()
			i3.grid_remove()
			fresh_db = CONN_ZDB(DBPATH)
			fresh_dbroot = fresh_db.dbroot
			fresh_db.deleterec(fresh_dbroot[ky])
			# del fresh_dbroot[ky]
			fresh_db.close()
			# print 'del : %s'%(ky,)
			
	def addnewftp(self):
		from config_design import CONFIG_DESIGN
		root = Tk()
		root.withdraw()
		cd = CONFIG_DESIGN(e_sec=1)
		
# def show_status():
	# import status
	# status.Status()
if __name__ == '__main__':
	conf = edit_config()