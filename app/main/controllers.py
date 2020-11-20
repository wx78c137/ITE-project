from flask import Flask, jsonify, abort, request, json, render_template, redirect, url_for, Blueprint
import os, random, string
from mongoengine.queryset.visitor import Q
from app import db, socketio
from app.models import Result

basedir = os.path.abspath(os.path.dirname(__file__))
main = Blueprint('main', __name__)


def fakeDb():
    dropDatabase()
    words = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','None']
    for i in range(80):
        letters = string.ascii_lowercase
        result_str = random.choice(words)
        seq = Result.objects.count()
        seq = seq + 1
        result =Result(result= result_str, seq= seq)
        result.save()


def dropDatabase():
    Result.drop_collection()


# Handle data array
def data_handle(data):
    if data == '1':
        cleaned_data = 'A'
    elif data == '2':
        cleaned_data = 'B'
    elif data == '3':
        cleaned_data = 'C'
    elif data == '4':
        cleaned_data = 'D'
    elif data == '5':
        cleaned_data = 'E'
    elif data == '6':
        cleaned_data = 'F'
    elif data == '7':
        cleaned_data = 'G'
    elif data == '8':
        cleaned_data = 'H'
    elif data == '9':
        cleaned_data = 'I'
    elif data == '10':
        cleaned_data = 'J'
    elif data == '11':
        cleaned_data = 'K'
    elif data == '12':
        cleaned_data = 'L'
    elif data == '13':
        cleaned_data = 'M'
    elif data == '14':
        cleaned_data = 'N'
    elif data == '15':
        cleaned_data = 'O'
    else:
        cleaned_data = 'None'
    return cleaned_data


# xoa toan bo database
@main.route('/clear-data')
def clear_data():
    try:
        dropDatabase()
    except Exception as e:
        print(e)
    return redirect(url_for('main.index'))

#hàm xử lý khi máy phát gửi dữ liệu
@main.route('/api_1_0/data', methods=['POST'])
def data_access():
    if not request.data:  # neu khong co data
        raw_data = 'No Data'
    else:
        raw_data = request.get_data(as_text=True)
    try:
        cleaned_data = data_handle(raw_data)
        seq = Result.objects.count()
        seq = seq + 1
        result = Result(result=cleaned_data, seq = seq)
        result.save()
        socketio.emit('newData')
        return_data = 'Post successfully'
    except Exception as e:
        print(e)
        return_data = str(e)
    return jsonify({'return_data': return_data})


@main.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    result = Result.objects.get(id=id)
    print(result.result)
    if request.method == 'POST':
        result.result = request.form['result']
        result.save()
        socketio.emit('newData')
    return redirect(url_for('main.resultEdit'))


@main.route('/', methods = ['GET','POST'])
def index():
    answers = Result.objects.all()
    return render_template('index.html', answers=answers)


@main.route('/edit')
def resultEdit():
    answers = Result.objects.all()
    return render_template('resultEdit.html', answers=answers)


#handle socketio
@socketio.on('onConnect')
def handle_message(json):
    print('received message: ' + str(json))
