import pyscreeze 
from datetime import datetime
import time
import pysftp
sftp = pysftp.Connection(host= '',username='',password='')

while True:
    timestand = datetime.now().strftime('%Y%m%d-%H%M%S')
    im1 = pyscreeze.screenshot()
    im2 = pyscreeze.screenshot('screenshot'+timestand+'.png')
    with sftp.cd('ftp'):
       sftp.put('screenshot'+timestand+'.png',preserve_mtime=True) 
    time.sleep(30)