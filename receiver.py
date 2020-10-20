import requests, os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from uuid import getnode as get_mac
from gtts import gTTS

tmpNum = 0

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def userChoice():
    global tmpNum
    mac_address = get_mac()
    while 1:
        if GPIO.input(5) == GPIO.HIGH:
            postRequest = requests.post('http://45.117.169.186:8000/api_1_0/first_data', data = {'mac_address':mac_address})
            return_data = postRequest.json().get('return_data')
            num = return_data.get('num')
            print(num)
            if num == 0:
                playResult('No answer yet')
            else:
                result = return_data.get('result')
                playResultNum(num)
                playResult(result)
                tmpNum = num
        if GPIO.input(6) == GPIO.HIGH:
            if tmpNum == 0:
                playResult('No answer yet')
            else:
                playResultNum(tmpNum)
                os.system("mpg321 tmp.mp3")


def playResultNum(num):
    path = 'mpg321' + 'voiceGTTS/Câu\ ' + str(num) + '.mp3'
    os.system(path)


def playResult(result):
    tts = gTTS(text=result, lang='en')
    tts.save("tmp.mp3")
    os.system("mpg321 tmp.mp3")


if __name__ == '__main__':
    userChoice()
