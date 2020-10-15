import requests
from uuid import getnode as get_mac
def userChoice():
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
            print(postRequest.text)
        if choice == '2':
            postRequest = requests.post('http://127.0.0.1:5000/api_1_0/last_data', data = {'mac_address':mac_address})
            print(postRequest.text)

if __name__ == '__main__':
    userChoice()
