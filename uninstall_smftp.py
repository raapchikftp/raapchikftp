import sys
import os, os.path
import win32api
import win32con
import ctypes
import time

""" Abbreviations for readability """
OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
memcpy = ctypes.cdll.msvcrt.memcpy

""" Windows Registry utilities """
def OpenRegistryKey(hiveKey, key):
    keyHandle = None
    try:
        curKey = ""
        keyItems = key.split('\\')
        for keyItem in keyItems:
            if curKey:
                curKey = curKey + "\\" + keyItem
            else:
                curKey = keyItem
            keyHandle = win32api.RegCreateKey(hiveKey, curKey)
    except Exception, e:
        keyHandle = None
        show_messg("OpenRegistryKey failed, Please this run program as Administrator")
        sys.exit(1)
        # print "OpenRegistryKey failed:", e
    return keyHandle

def ReadRegistryValue(hiveKey, key, name):
    """ Simple api to read one value from Windows registry. 
    If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        hKey = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_ALL_ACCESS)
        data, typeId = win32api.RegQueryValueEx(hKey, name)
        win32api.RegCloseKey(hKey)
    except Exception, e:
        if e[2] == "Access is denied.":
            # print "throw error admin right"
            show_messg("Admin Rights, Please this run program as Administrator")
            sys.exit(1)
        # show_messg("ReadRegistryValue failed, Please this run program as Administrator")
        # print "ReadRegistryValue failed:", e
    return data, typeId

def DelRegistryValue(hiveKey, key):
    """ Simple api to delete one value to Windows registry. 
    If 'name' is empty string, writes to default value."""
    try:
        keyHandle = OpenRegistryKey(hiveKey, key)
        win32api.RegDeleteKey(hiveKey, key)
        # win32api.RegSetValueEx(keyHandle, name, 0, typeId, data)
        win32api.RegCloseKey(keyHandle)
    except Exception, e:
        show_messg("Deletion Registry key failed, Please this run program as Administrator "+str(e))
        sys.exit(1)
        # print "WriteRegistry failed:", e
 
#########################################################
def UnInstallSMFTP():
	if ReadRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FolderUpload\Command", "") != (None,None):
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FolderUpload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FolderUpload")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FolderUpload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FolderUpload")

		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FolderDownload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FolderDownload")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FolderDownload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FolderDownload")

		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FileUpload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FileUpload")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FileUpload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FileUpload")

		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FileDownload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\FileDownload")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FileDownload\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\FileDownload")
		
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\Ftp Settings\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\Ftp Settings")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\Ftp Settings\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\Ftp Settings")
		
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\Ftp log\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\Ftp log")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\Ftp log\Command")
		DelRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\Ftp log")
	else:
		# show_messg("Installation failed: Already installed")
		sys.exit(1);
    # WriteLastTime()
#########################################################

def show_messg(msg):
	import tkMessageBox,Tkinter
	root = Tkinter.Tk()
	root.withdraw()
	tkMessageBox.showinfo(':::RaapCHIK:::',msg,parent=root)
	root.destroy()
	
if __name__ == "__main__":
	UnInstallSMFTP()
	show_messg(':::RaapCHIK::: uninstalled successfully')
		
