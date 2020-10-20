import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from uuid import getnode as get_mac
from gtts import gTTS

tmpNum = ''

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def userChoice():
    global tmpNum
    mac_address = get_mac()
    while 1:
        if GPIO.input(23) == False:
            if GPIO.input(23) == True:
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
        if GPIO.input(18) == False:
            if GPIO.input(23) == True:
                if tmpNum == '':
                    playViLanguage('Chưa có câu trả lời mới')
                else:
                    playViLanguage(tmpNum)

def playViLanguage(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("tmp.mp3")
    os.system("mpg321 tmp.mp3")



if __name__ == '__main__':
    userChoice()
