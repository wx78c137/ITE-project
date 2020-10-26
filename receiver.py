import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from subprocess import Popen,PIPE
from gtts import gTTS
from gpiozero import Button, LED
from time import sleep
from datetime import datetime

tmpNum = ''
current_link = ''
t1 = 0
t2 = 0
button1 = Button(21)
button2 = Button(20)
buzzer = LED(16)
serverUrl = 'http://45.117.169.186:5000'

def getName():
    f = open('/home/pi/name.txt', 'r')
    data = f.read().replace('\n', '')
    return data


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
    mac_address = getName()
    delta = t2 - t1
    print(delta)
    delsec = delta.total_seconds()
    if delsec < 1:
        getNewResult(mac_address)
    else:
        getOldResult()
    t1=0
    t2=0


def main():
    print('program start')
    sleep(5)
    buzzerOn()
    while 1:
        button1.when_pressed = set_t1
        button1.when_released = set_t2


def playMp3(url):
    p = Popen(['play','-t', 'mp3', url, 'tempo 0.8'], stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        print("sox play failed %d %s %s" % (p.returncode, output, error))
        pass


def getNewResult(mac_address):
    global tmpNum
    global current_link
    try:
        print('making request to server')
        firstDataUrl = serverUrl + '/api_1_0/first_data'
        postRequest = requests.post(firstDataUrl, data = {'mac_address':mac_address})
        print('end server request')
        return_data = postRequest.json().get('return_data')
        num = return_data.get('num')
        link = return_data.get('link')
        if num == 0:
            noAnsUrl = '/home/pi/myProjects/ITE-project/noAns.mp3'
            playMp3(noAnsUrl)
        elif link:
            mp3Url = serverUrl + link
            playMp3(mp3Url)
            current_link = link
            tmpNum = str(num)
    except Exception as e:
        print(e)
        pass


def getOldResult():
    if tmpNum == '':
        noAnsUrl = '/home/pi/myProjects/ITE-project/noAns.mp3'
        playMp3(noAnsUrl)
    else:
        playMp3(current_link)


def buzzerOn():
    buzzer.on()
    sleep(0.5)
    buzzer.off()

if __name__ == '__main__':
    main()
