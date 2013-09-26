import sys,os
from multiprocessing import freeze_support
if __name__ == '__main__':
    freeze_support()
    if len(sys.argv) == 4:
        if sys.argv[1] == 'fldr':
            if os.path.isdir(sys.argv[3]) == True:
                import subprocess
                args = ["smftp.exe", sys.argv[2],sys.argv[3]]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
        elif sys.argv[1] == 'fle':
            if os.path.isdir(sys.argv[3]) == False:
                import subprocess
                args = ["smftpF.exe", sys.argv[3],sys.argv[2]]
                subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
        else:
            pass