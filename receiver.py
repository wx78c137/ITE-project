import requests, os
from uuid import getnode as get_mac
from gtts import gTTS
tmpNum = 0
def userChoice():
    global tmpNum
    mac_address = get_mac()
    print(mac_address)
    while 1:
        print('Chọn lệnh:')
        print('1. Lấy đáp án kế tiếp')
        print('2. Lấy lại đáp án cũ')
        print('Nhấn Ctrl + D để thoát')
        choice = input('Lựa chọn: ')
        if choice == '1':
            postRequest = requests.post('http://127.0.0.1:5000/api_1_0/first_data', data = {'mac_address':mac_address})
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
        if choice == '2':
            if tmpNum == 0:
                playResult('No answer yet')
            else:
                playResultNum(tmpNum)
                os.system("mpg321 tmp.mp3")


def playResultNum(num):
    path = 'mpg321' + ' /home/vuhoang/voiceGTTS/Câu\ ' + str(num) + '.mp3'
    os.system(path)


def playResult(result):
    tts = gTTS(text=result, lang='en')
    tts.save("tmp.mp3")
    os.system("mpg321 tmp.mp3")


if __name__ == '__main__':
    userChoice()
