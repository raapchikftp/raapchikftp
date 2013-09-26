from Tkinter import *
import os,sys,tkFont
from save_ftp_config import save_ftp_config
from tkFileDialog import askdirectory

class CONFIG_DESIGN(Toplevel):
	def __init__(self,ky='',eparams='',e_sec=0):
		self.ky = ky
		self.eparams = eparams
		self.e_sec = e_sec
		Toplevel.__init__(self)
		self.conn_name = StringVar()
		self.host = StringVar()
		self.port = IntVar();
		self.conn_type = StringVar()
		self.usrnm = StringVar()
		self.passwd = StringVar()
		self.lcl_path = StringVar()
		self.rmt_path = StringVar()
		self.sound_play = IntVar()
		self.acv_pcv = StringVar()
		self.create_frame()
		
	def create_frame(self):
		tk = self
		tk.focus()
		self.frame = Frame(tk)
		tk.wm_resizable(0,0)
		tk.wm_title(":::: RaapCHIK :::")
		tk.protocol('WM_DELETE_WINDOW', self.cancel_ftp_config)
		MODES = ['FTP','FTPS','SSH']
		ACV_MODES = ['Default','Active','Passive']
		self.fbolder = tkFont.Font(weight='bold',size=9,slant='italic')
		self.fitalic = tkFont.Font(slant='italic',size=9)

		hedr = Label(tk,text='Settings',background='thistle',height=2,font=self.fbolder)
		hedr.pack(side="top",fill="both")
		
		if self.ky != '':
			self.conn_name.set(self.eparams['FTP_CONN_NAME'])
			self.host.set(self.eparams['FTP_HOST'])
			self.port.set(self.eparams['FTP_PORT'])
			self.conn_type.set(self.eparams['FTP_CON_TYPE'])
			self.usrnm.set(self.eparams['FTP_USER'])
			self.passwd.set(self.eparams['FTP_PASSW'])
			self.lcl_path.set(self.eparams['FTP_WWW_LOCAL'])
			self.rmt_path.set(self.eparams['FTP_WWW_REMOTE'])
			self.sound_play.set(self.eparams['FTP_PLAY_SOUND'])
			self.acv_pcv.set(self.eparams['FTP_ACV_PCV'])
			
			
		connection_name = Label(self.frame,text='Connection Name')
		connection_entry = Entry(self.frame,textvariable=self.conn_name)
		connection_name.grid(row=0,column=0, sticky=W,padx=10)
		connection_entry.grid(row=0,column=1,padx=10, pady=10)
		
		conn_type_name = Label(self.frame,text='FTP Type')
		conn_type_name.grid(row=1,column=0, sticky=W,padx=10)
		x=1
		for txt in MODES:
			b = Radiobutton(self.frame,text=txt,font=self.fitalic,variable=self.conn_type,value=txt,indicatoron=0,command=lambda txt=txt: self.set_port_number(txt),width=15)
			b.grid(row=x,column=1, sticky=W,padx=10)
			x = x + 1
		
		host_name = Label(self.frame,text='FTP HOST')
		host_entry = Entry(self.frame,textvariable=self.host)
		host_name.grid(row=x,column=0, sticky=W,padx=10)
		host_entry.grid(row=x,column=1,padx=10, pady=10)
		
		host_port_name = Label(self.frame,text='FTP PORT')
		host_port_entry = Entry(self.frame,textvariable=self.port)
		host_port_name.grid(row=x+1,column=0, sticky=W,padx=10)
		host_port_entry.grid(row=x+1,column=1,padx=10, pady=10)
		
		user_name = Label(self.frame,text='FTP UserName')
		user_name_entry = Entry(self.frame,textvariable=self.usrnm)
		user_name.grid(row=x+2,column=0, sticky=W,padx=10)
		user_name_entry.grid(row=x+2,column=1,padx=10, pady=10)
		
		password = Label(self.frame,text='FTP Password')
		password_entry = Entry(self.frame,textvariable=self.passwd)
		password.grid(row=x+3,column=0, sticky=W,padx=10)
		password_entry.grid(row=x+3,column=1,padx=10, pady=10)
		
		local_path = Label(self.frame,text='Local WWW Path')
		if self.ky != '':
			local_path_entry = Button(self.frame,text='Browse',command=self.ask_dirc,width=15,font=self.fitalic)#Label(self.frame,text=self.eparams['FTP_WWW_LOCAL'][-30:], width=15)
		else:
			local_path_entry = Button(self.frame,text='Browse',command=self.ask_dirc,width=15,font=self.fitalic)
		
		local_path.grid(row=x+4,column=0, sticky=W,padx=10)
		local_path_entry.grid(row=x+4,column=1,padx=10, pady=10)
		
		remote_path = Label(self.frame,text='Remote WWW path')
		remote_path_entry = Entry(self.frame,textvariable=self.rmt_path)
		remote_path.grid(row=x+5,column=0, sticky=W,padx=10)
		remote_path_entry.grid(row=x+5,column=1,padx=10, pady=10)
		
		sound_play = Label(self.frame,text='Play Sound')
		sound_play_entry = Checkbutton(self.frame,variable=self.sound_play)
		sound_play.grid(row=x+6,column=0, sticky=W,padx=10)
		sound_play_entry.grid(row=x+6,column=1,padx=10, pady=10)
		
		conn_type_acv_pcv = Label(self.frame,text='Connection Type')
		conn_type_acv_pcv.grid(row=x+7,column=0, sticky=W,padx=10)
		
		x=x+7
		for txt in ACV_MODES:
			b1 = Radiobutton(self.frame,text=txt,font=self.fitalic,variable=self.acv_pcv,value=txt,indicatoron=0,width=15)
			b1.grid(row=x,column=1,sticky=W,padx=10)
			x = x + 1
			
		lst_frm = Frame(tk,background='thistle')
		submit_butt = Button(lst_frm,text='Submit',font=self.fbolder,height=2,width=20,background='plum3',command=lambda : self.set_ftp_config(save_ftp_config))
		cancel_butt = Button(lst_frm,text='Cancel',font=self.fbolder,height=2, width=10,background='plum3',command=self.cancel_ftp_config)
		submit_butt.grid(row=0,column=0,sticky=W,padx=10)
		cancel_butt.grid(row=0,column=1,padx=10, pady=10)
		lst_frm.pack(side='bottom',fill=BOTH, expand=0)
		
		self.frame.pack(fill=BOTH, expand=0)
		# self.frame.focus()
		mainloop()
			
	def get_all_config_params(self):
		config = {}
		config['FTP_CONN_NAME'] = self.conn_name.get()
		config['FTP_HOST'] = self.host.get()
		config['FTP_PORT'] = self.port.get()
		config['FTP_CON_TYPE'] = self.conn_type.get()
		config['FTP_USER'] = self.usrnm.get()
		config['FTP_PASSW'] = self.passwd.get()
		config['FTP_WWW_REMOTE'] = self.rmt_path.get()
		config['FTP_WWW_LOCAL'] = self.lcl_path.get()
		config['FTP_PLAY_SOUND'] = self.sound_play.get()
		config['FTP_ACV_PCV'] = self.acv_pcv.get()
		if self.ky != '':
			config['FTP_ID'] = self.eparams['FTP_ID']
			config['FTP_WWW_LOCAL'] = self.eparams['FTP_WWW_LOCAL']
		return config
		
	def set_port_number(self,md):
		if md == 'SSH':
			self.port.set(22)
		else:
			self.port.set(21)
	
	def ask_dirc(self):
		options = {}
		options['initialdir'] = r''+self.ky
		options['title'] = 'Select Local WWW path'
		if self.ky != '':
			options['initialdir'] = r''+self.eparams['FTP_WWW_LOCAL']
			options['title'] = '[Readable] Local WWW path'
			
		options['mustexist'] = True
		options['parent'] = self.frame
		path = askdirectory(**options)
		path = r''+path
		self.lcl_path.set(path)
		
	def set_ftp_config(self,func):
		params = self.get_all_config_params()
		func(params,ky=self.ky)
		
	def cancel_ftp_config(self):
		if self.e_sec == 1:
			# self.destroy()
			self.destroy()
			self.quit()
			# sys.exit(1)
		else:
			sys.exit(1)
	