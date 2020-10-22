import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from uuid import getnode as get_mac
from gtts import gTTS
from gpiozero import Button
from signal import pause

tmpNum = ''

button1 = Button(21)
button2 = Button(20)

def userChoice():
    print('program start')
    mac_address = get_mac()
    while 1:
        if button1.is_pressed == True:
            b1Pressed(mac_address)
        elif button2.is_pressed == True:
            b2Pressed()

def playViLanguage(text):
    print('making request to gTTS')
    tts = gTTS(text=text, lang='vi')
    print('end gTTS')
    tts.save("tmp.mp3")
    os.system("mpg321 tmp.mp3")


def b1Pressed(mac_address):
    global tmpNum
    print('making request to server')
    postRequest = requests.post('http://45.117.169.186:8000/api_1_0/first_data', data = {'mac_address':mac_address})
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


def b2Pressed():
    if tmpNum == '':
        playViLanguage('Chưa có câu trả lời mới')
    else:
        os.system("mpg321 tmp.mp3")

if __name__ == '__main__':
    try:
        userChoice()
    except Exception as e:
        print(e)
