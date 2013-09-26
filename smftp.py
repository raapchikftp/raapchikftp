import sys, os
from getfiles import GetFiles
from getrmtfiles import GetRmtFiles
from callftp import Callftp
from Tkinter import *
from multiprocessing import Process, freeze_support
import uuid
from conn_zdb import CONN_ZDB
from config import *
from dbpaths import *
import sys
import subprocess,tkFont
	
class Smftp():
	def __init__(self,parent=None,files=None,C_KEY=None,action_type=None):
		self.root = Tk()
		self.root.wm_resizable(0,0)
		self.root.wm_title(":::: RaapCHIK :::")
		# Frame.__init__(self,parent)
		self.files = files
		self.files_checked = []
		self.fstatus = []
		self.C_KEY = C_KEY
		self.action_type = action_type
		self.fbolder = tkFont.Font(weight='bold',size=9,slant='italic')
		self.fitalic = tkFont.Font(slant='italic',size=8)
		self.selallbox = IntVar()
		
		hdr_frame1 = Frame(self.root)
		if self.action_type == 'upld':
			u_d = 'Upload'
		else:
			u_d = 'Download'
		butt = Button(hdr_frame1,text=u_d,command=lambda : self.process_files(True),font=self.fbolder,background='thistle',height=2)
		
		butt.pack(fill="both",expand=True)
		hdr_frame1.pack(side="bottom",fill='both')
		
		hdr_frame = Frame(self.root,background='thistle')
		chkb = Checkbutton(hdr_frame,text='#',font=self.fbolder, anchor=W,width=10,background='thistle',height=2,padx=10,command=self.set_all_chke,variable=self.selallbox)
		labl = Label(hdr_frame,text='Files',font=self.fbolder, anchor=CENTER,width=77,background='thistle',height=2)
		stlb = Label(hdr_frame,text='Status',font=self.fbolder, anchor=E,background='thistle',height=2)
		chkb.grid(row=0,column=0)
		labl.grid(row=0,column=1)
		stlb.grid(row=0,column=2)
		hdr_frame.pack(side="top",fill="both")
		
		self.canvas = Canvas(self.root,width=800,height=450)
		self.frame = Frame(self.canvas)
		self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
		self.frame.bind("<Configure>", self.OnFrameConfigure)
		
		self.make_ftp_form()
		self.root.bind('<Return>',self.process_files)
		self.root.mainloop()
		
	def make_ftp_form(self):
		if self.files != None:
			row = 1
			for (lpath,fpath) in self.files:
				# folder_disb = 'disabled' if os.path.splitext(lpath)[1] == '' else 'normal'
				var = IntVar()
				status_var = StringVar()
				status_var.set('Pending...')
				if self.action_type == 'upld':
					isf_isd = os.path.isfile(lpath)
				else:
					isf_isd = False if os.path.splitext(fpath)[1] == '' else True
				
				if isf_isd == False and self.action_type == 'dwnld':
					self.files_checked.append(var)
					self.fstatus.append(status_var)
					row += 1
					continue
				
				if isf_isd:
					chkb = Checkbutton(self.frame,variable=var,width=5)
				else:
					chkb = Label(self.frame,text=' ',width=0)
				
				if isf_isd:
					labl = Label(self.frame,text=lpath,width=80,wraplength=350)
				else:
					labl = Label(self.frame,text=lpath,width=80,wraplength=350,background='AntiqueWhite4',font=self.fbolder,fg="white")
				
				if isf_isd:
					stlb = Label(self.frame,width=15,textvariable=status_var,font=self.fitalic)
				else:
					stlb = Label(self.frame,width=0,text=' ')
					
				self.files_checked.append(var)
				self.fstatus.append(status_var)
				chkb.grid(row=row,column=0)
				labl.grid(row=row,column=1)
				stlb.grid(row=row,column=2)
				row += 1
				
	def get_all_files_2_process(self):
		return self.files_checked
	
	def OnFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		
	def process_files(self,eve):
		counter = 0
		process_fls = []
		if self.files_checked != None:
			for x in self.files_checked:
				if x.get() == 1:
					if self.action_type == 'upld':
						isf_isd = os.path.isfile(self.files[counter][0])
					else:
						isf_isd = False if os.path.splitext(self.files[counter][1])[1] == '' else True
						
					if isf_isd:
						process_fls.append((self.files[counter],counter))
						self.fstatus[counter].set('Please wait........')
				counter += 1
			
			if len(process_fls) > 0:
				process_fls.append(self.C_KEY)
				process_fls.append(self.action_type)
				
				self.root.withdraw()
				# print process_fls
				call_ftp = Callftp(process_fls)
				call_ftp.getFtpSession()
			sys.exit(1)
	
	def set_all_chke(self):
		for x in self.files_checked:
			if self.selallbox.get() == 1:
				x.set(1)
			else:
				x.set(0)

if __name__ == '__main__':
	freeze_support()
	upld_or_dwnl = sys.argv[1]
	fld_path = r''+os.getcwd()
	if len(sys.argv) == 3:
		fld_path = r''+sys.argv[2]
	
	config = Config(fld_path)
	config_params = config.get_config_params()
	if len(config_params) <= 0:
		# config.create_frame()
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
				
			newint = askinteger('Select FTP [default=1]', msg,initialvalue=1,parent=root,minvalue=1,maxvalue=len(config_params))
			root.destroy()
			if newint == None:
				config_index = 0
			else:
				config_index = newint-1
		
		if upld_or_dwnl == "dwnld":
			f = GetRmtFiles(fld_path,config_params[config_index])
		elif upld_or_dwnl == "upld":
			f = GetFiles(fld_path,config_params[config_index])
		else:
			sys.exit(1) ##FUTURE REF handle unwanted
		
		allfls = f.get_all_files()	
		smftp = Smftp(files=allfls,C_KEY=config_params[config_index]['FTP_KEY'],action_type=upld_or_dwnl)
		# mainloop()