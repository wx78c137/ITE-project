import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from uuid import getnode as get_mac
from gtts import gTTS
from gpiozero import Button, LED
from signal import pause
from time import sleep
from datetime import datetime

tmpNum = ''
t1 = 0
t2 = 0
button1 = Button(21)
button2 = Button(20)
buzzer = LED(16)
def set_t1():
    global t1
    t1 = datetime.now()

def set_t2():
    global t2
    t2 = datetime.now()

def countDelta():
    global t1, t2
    mac_address = get_mac()
    delta = t2 - t1
    delsec = delta.total_second()
    if 0.2 < delsec < 2:
        getNewResult(mac_address)
    else:
        getOldResult()
    t1=0
    t2=0


def userChoice():
    print('program start')
    mac_address = get_mac()
    while 1:
        button1.when_pressed = set_t1
        button1.when_released = set_t2


def playViLanguage(text):
    print('making request to gTTS')
    tts = gTTS(text=text, lang='vi')
    print('end gTTS')
    tts.save("tmp.mp3")
    os.system("mpg321 tmp.mp3")


def getNewResult(mac_address):
    buzzerOn()
    global tmpNum
    print('making request to server')
    postRequest = requests.post('http://45.117.169.186:5000/api_1_0/first_data', data = {'mac_address':mac_address})
    print('end server request')
    return_data = postRequest.json().get('return_data')
    num = return_data.get('num')
    if num == 0:
        playViLanguage('Chưa có câu trả lời mới')
    else:
        result = return_data.get('result')
        text = 'Câu ' + str(num) + ': ' + result
        playViLanguage(text)
        tmpNum = text


def getOldResult():
    buzzerOn()
    if tmpNum == '':
        playViLanguage('Chưa có câu trả lời mới')
    else:
        os.system("mpg321 tmp.mp3")


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
