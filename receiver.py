import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from uuid import getnode as get_mac
from gtts import gTTS
from gpiozero import Button

tmpNum = ''

B23 = Button(23)
B18 = Button(18)

def userChoice():
    global tmpNum
    mac_address = get_mac()
    B23.when_pressed = b23Pressed
    B18.when_pressed = b18Pressed

def playViLanguage(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("tmp.mp3")
    os.system("mpg321 tmp.mp3")


def b23Pressed():
    postRequest = requests.post('http://45.117.169.186:8000/api_1_0/first_data', data = {'mac_address':mac_address})
    return_data = postRequest.json().get('return_data')
    num = return_data.get('num')
    if num == 0:
        playResult('No answer yet')
    else:
        result = return_data.get('result')
        text = 'Câu ' + str(num) + ': ' + result
        playViLanguage(text)
        tmpNum = text


def b18Pressed():
    if tmpNum == '':
        playViLanguage('Chưa có câu trả lời mới')
    else:
        os.system("mpg321 tmp.mp3")

if __name__ == '__main__':
    userChoice()
