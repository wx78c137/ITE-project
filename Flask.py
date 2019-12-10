from flask import Flask, jsonify, abort, request, json, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(80))



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
    else:
        cleaned_data = 'None'
    return cleaned_data

#xoa toan bo database
@app.route('/clear-data')
def clear_data():
    try:
        db.drop_all()
        db.create_all() # tao database moi
    except Exception as e:
        print(e)
    return redirect(url_for('index'))


@app.route('/api_1_0/data', methods=['POST'])
def data_access():
    if not request.data:  # neu khong co data
        raw_data = 'No Data'
    else:
        raw_data = request.get_data(as_text=True)
    try:
        cleaned_data = data_handle(raw_data)
        answer = Answer(answer=cleaned_data)
        db.session.add(answer)
        db.session.commit()
        return_data = 'Post successfully'
    except Exception as e:
        print(e)
        return_data = str(e)
    return jsonify({'return_data': return_data})


@app.route('/')
def index():
    answers = Answer.query.all()
    return render_template('index.html', answers=answers)


if __name__ == '__main__':
    app.run(debug=True)
