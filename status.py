from conn_zdb import CONN_ZDB
from processlogger import ProcessLogger
from Tkinter import *
import tkFont,sys
from ttkcalendar import *
class Status(Calendar):
	def __init__(self,dt=""):
		self.log = ProcessLogger()
		self.data = self.log.get_process_Q(dt)
		self.create_design()
		self.log.close_db()
		
	def create_design(self):
		self.root = Tk()
		self.root.wm_resizable(0,0)
		self.root.wm_title(":::: RaapCHIK ::: ")
		self.fbolder = tkFont.Font(weight='bold',size=9,slant='italic')
		self.fitalic = tkFont.Font(slant='italic',size=9)
		
		top_frame = Frame(self.root,background='thistle')
		labl = Label(top_frame,text='Host',background='thistle',font=self.fbolder,width=21,height=2)
		lab2 = Label(top_frame,text='Type',background='thistle',font=self.fbolder,width=7,height=2)
		lab3 = Label(top_frame,text='Status',background='thistle',font=self.fbolder,width=7,height=2)
		lab4 = Label(top_frame,text='Message',background='thistle',font=self.fbolder,width=50,height=2)
		lab5 = Label(top_frame,text='File-1',background='thistle',font=self.fbolder,width=20,height=2)
		lab6 = Label(top_frame,text='File-2',background='thistle',font=self.fbolder,width=20,height=2)
		labl.grid(row=0,column=0)
		lab2.grid(row=0,column=1)
		lab3.grid(row=0,column=2)
		lab4.grid(row=0,column=3)
		lab5.grid(row=0,column=4)
		lab6.grid(row=0,column=5)
		top_frame.pack(side='top',fill='both',expand=True)
		
		
		bottom_2_frm = Frame(self.root,background='thistle',width=600,bd=1,relief=SUNKEN)
		labl = Label(bottom_2_frm,text='Status',font=self.fbolder,background='thistle',width=15)
		dbtn1 = Button(bottom_2_frm,text='Done',background='thistle',command=lambda : self.return_new_form('Done',6),font=self.fitalic, width=10)
		dbtn2 = Button(bottom_2_frm,text='Pending',background='thistle',command=lambda : self.return_new_form('Pending',6),font=self.fitalic, width=10)
		dbtn3 = Button(bottom_2_frm,text='Failed',background='thistle',command=lambda : self.return_new_form('Failed',6),font=self.fitalic, width=10)
		dbtn4 = Button(bottom_2_frm,text='All',background='thistle',command=lambda : self.return_new_form('all',6),font=self.fitalic, width=10)
		labl.grid(row=0,column=0)
		dbtn1.grid(row=0,column=1)
		dbtn2.grid(row=0,column=2)
		dbtn3.grid(row=0,column=3)
		dbtn4.grid(row=0,column=4)
		bottom_2_frm.pack(side='bottom',fill='both',expand=True)
		
		bottom_1_frm = Frame(self.root,background='thistle',width=600,bd=1,relief=SUNKEN)
		labl = Label(bottom_1_frm,text='Type',font=self.fbolder,background='thistle',width=15)
		dbtn1 = Button(bottom_1_frm,text='Login',background='thistle',font=self.fitalic, command=lambda : self.return_new_form('login',5),width=10)
		dbtn2 = Button(bottom_1_frm,text='Upload',background='thistle',font=self.fitalic, command=lambda : self.return_new_form('upload',5), width=10)
		dbtn3 = Button(bottom_1_frm,text='Download',background='thistle',font=self.fitalic, command=lambda : self.return_new_form('download',5), width=10)
		dbtn4 = Button(bottom_1_frm,text='List',background='thistle',font=self.fitalic, command=lambda : self.return_new_form('ls',5), width=10)
		dbtn5 = Button(bottom_1_frm,text='All',background='thistle',font=self.fitalic, command=lambda : self.return_new_form('all',5), width=10)
		labl.grid(row=0,column=0)
		dbtn1.grid(row=0,column=1)
		dbtn2.grid(row=0,column=2)
		dbtn3.grid(row=0,column=3)
		dbtn4.grid(row=0,column=4)
		dbtn5.grid(row=0,column=4)
		bottom_1_frm.pack(side='bottom',fill='both',expand=True)
		
		
		
		ttkcal = Calendar(firstweekday=calendar.SUNDAY,master=self.root)
		# self.ttkcal = Calendar.__init__(self, firstweekday=calendar.SUNDAY,master=self.root)
		ttkcal.pack(side='right',expand=1, fill='both')
		
		ttkcal.bind('<<date-selected>>', lambda x: self.cal_click_evnt_triggred(dtim = ttkcal.dtim))
		
		# super(Status, self).__init__(self, firstweekday=calendar.SUNDAY).pack(side='right',expand=1, fill='both')
		
		self.canvas = Canvas(self.root,width=900,height=450)
		self.frame = Frame(self.canvas)
		self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
		self.frame.bind("<Configure>", self.OnFrameConfigure)

		self.make_status_form(self.data)
		# self.root.bind('<Return>',self.return_new_form)
		self.root.mainloop()
	
	def make_status_form(self,data):
		row = 1
		self.st_frame = Frame(self.frame,width=890)
		if len(data)>0:
			for dt in data:
				# ifrm = Frame(self.frame,bd=1, relief=SUNKEN,width=890)
				labl = Label(self.st_frame,text=dt[4],width=20,anchor=NW,wraplength=350)
				lab2 = Label(self.st_frame,text=dt[5],width=7)
				lab3 = Label(self.st_frame,text=dt[6],width=7)
				lab4 = Label(self.st_frame,text=dt[7],width=50,wraplength=350)
				lab5 = Label(self.st_frame,text=dt[2],width=20,wraplength=120)
				lab6 = Label(self.st_frame,text=dt[3],width=20,wraplength=150)
				labl.grid(row=row,column=0)
				lab2.grid(row=row,column=1)
				lab3.grid(row=row,column=2)
				lab4.grid(row=row,column=3)
				lab5.grid(row=row,column=4)
				lab6.grid(row=row,column=5)
				
				# ifrm.grid(row=row,column=0)
				# ifrm.pack(fill="both",expand=0)
				row += 1
		
		self.st_frame.grid(row=0,column=0)
				
	def OnFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		
	def return_new_form(self,srch,fld):
		if srch == 'all':
			data = self.data
		else:
			data = [x for x in self.data if x[fld] == srch]
			
		self.canvas.yview('moveto','0')
		self.st_frame.grid_forget()
		self.make_status_form(data)
	
	def cal_click_evnt_triggred(self,dtim='now'):
		# dte = "DATE('%s','localtime')"%dtim
		dte = dtim
		import subprocess
		args = ["status.exe", dte,'test']
		subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
		sys.exit(1)
		# self.log = ProcessLogger()
		# self.data = self.log.get_process_Q(dte)
		# self.log.close_db()
		# self.return_new_form('all',5)

if __name__ == '__main__':
	# if len(sys.argv) > 2:
		# dte = "DATE('%s','localtime')"%sys.argv[1]
		# Status(dt=dte)
	# else:
		# Status(dt="DATE('now','localtime')")
	# with open('logme.txt', 'a') as the_file:
		# the_file.write(sys.argv[1]+'\n')
	dte = "DATE('%s','localtime')"%sys.argv[1]
	Status(dt=dte)