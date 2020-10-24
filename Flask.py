from flask import Flask, jsonify, abort, request, json, render_template, redirect, url_for
from flask_mongoengine import MongoEngine
import os, random, string
from mongoengine.queryset.visitor import Q

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#app.config['MONGODB_SETTINGS'] = {
#    'host': 'mongodb+srv://vuhoang17891:Vu1781991@cluster0.bknlw.mongodb.net/iteprojects?retryWrites=true&w=majority',
#}
app.config['MONGODB_SETTINGS'] = {
    'db': 'iteprojects',
    'host': '127.0.0.1',
    'port': 27017
}


db = MongoEngine(app)

class Result(db.Document):
    seq = db.IntField()
    result = db.StringField()
    received = db.ListField()


def fakeDb():
    dropDatabase()
    words = ["Stack", "Overflow", "rocks", 'print', 'Generation, Thế hệ', 'Home, ngôi nhà', 'horse, con ngựa', 'dog, con chó', 'Anh', 'Bê Bò', 'Chó','Dê','Em', 'F', 'Gà', 'Door, cánh cửa', 'pillow, cái gối', 'coffee, cà phê', 'pencil, cây bút chì','mobile phone, điện thoại di động']
    for i in range(40):
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
        cleaned_data = 'Anh'
    elif data == '2':
        cleaned_data = 'Bò'
    elif data == '3':
        cleaned_data = 'Chó'
    elif data == '4':
        cleaned_data = 'Dê'
    elif data == '5':
        cleaned_data = 'Em'
    elif data == '6':
        cleaned_data = 'F'
    elif data == '7':
        cleaned_data = 'Gà'
    elif data == '8':
        cleaned_data = 'Heo'
    elif data == '9':
        cleaned_data = 'I ngắn'
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
@app.route('/clear-data')
def clear_data():
    try:
        dropDatabase()
    except Exception as e:
        print(e)
    return redirect(url_for('index'))

#hàm xử lý khi máy phát gửi dữ liệu
@app.route('/api_1_0/data', methods=['POST'])
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
        return_data = 'Post successfully'
    except Exception as e:
        print(e)
        return_data = str(e)
    return jsonify({'return_data': return_data})


@app.route('/api_1_0/first_data', methods = ['POST'])
def get_first_data():
    if not request.values:  # neu khong co data
        pass
    else:
        mac_address = request.values.get('mac_address')
    result = Result.objects(Q(received__ne = mac_address) & Q(result__ne = 'None')).first()
    if result:
        result.update(add_to_set__received = mac_address)
        return jsonify({'return_data': {'num':result.seq, 'result': result.result}})
    else:
        return jsonify({'return_data': {'num':0, 'result': 'None'}})



@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    result = Result.objects.get(id=id)
    print(result.result)
    if request.method == 'POST':
        result.result = request.form['result']
        result.save()
    return redirect(url_for('index'))

@app.route('/')
def index():
    answers = Result.objects.all()
    return render_template('index.html', answers=answers)


if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get('HOST'), port=5000)
