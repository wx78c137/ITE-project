import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from uuid import getnode as get_mac
from gtts import gTTS
from gpiozero import Button, LED
from signal import pause
from time import sleep
from datetime import datetime

tmpNum = ''
current_link = ''
t1 = 0
t2 = 0
button1 = Button(21)
button2 = Button(20)
buzzer = LED(16)
def set_t1():
    print('set t1')
    global t1
    t1 = datetime.now()
    print(t1)

def set_t2():
    buzzerOn()
    print('set t2')
    global t2
    t2 = datetime.now()
    print(t2)
    countDelta()


def countDelta():
    global t1, t2
    mac_address = get_mac()
    delta = t2 - t1
    print(delta)
    delsec = delta.total_seconds()
    if delsec < 1:
        getNewResult(mac_address)
    else:
        getOldResult()
    t1=0
    t2=0


def userChoice():
    print('program start')
    sleep(5)
    mac_address = get_mac()
    while 1:
        button1.when_pressed = set_t1
        button1.when_released = set_t2





def getNewResult(mac_address):
    global tmpNum
    global current_link
    print('making request to server')
    postRequest = requests.post('http://45.117.169.186:5000/api_1_0/first_data', data = {'mac_address':mac_address})
    print('end server request')
    return_data = postRequest.json().get('return_data')
    num = return_data.get('num')
    link = return_data.get('link')
    if num == 0:
        os.system("mpg321 /home/pi/myProjects/ITE-project/noAns.mp3")
    elif link:
        os.system("mpg321 http://45.117.169.186:5000" + link)
        current_link = link
        tmpNum = str(num)


def getOldResult():
    if tmpNum == '':
        os.system("mpg321 /home/pi/myProjects/ITE-project/noAns.mp3")
    else:
        os.system("mpg321 http://45.117.169.186:5000" + current_link)


def buzzerOn():
    buzzer.on()
    sleep(0.5)
    buzzer.off()

if __name__ == '__main__':
    try:
        buzzerOn()
        userChoice()
    except Exception as e:
        print(e)
