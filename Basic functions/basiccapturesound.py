import sounddevice as sd 
from scipy.io.wavfile import write
import time
import pysftp
from datetime import datetime

sftp = pysftp.Connection(host= '',username='',password='')

fs = 44100 # Sample rate 
seconds = 30 # Duration of recording 


while True:
    timestand = datetime.now().strftime('%Y%m%d-%H%M%S')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait() # Wait until recording is finished 
    write('output'+timestand+'.wav', fs, myrecording)
    with sftp.cd('ftp'):
        sftp.put('output'+timestand+'.wav',preserve_mtime=True) 
    time.sleep(40)
   