from flask import Flask, jsonify, abort, request, json, render_template, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO



app = Flask(__name__)
# Configurations
app.config.from_object('config')

#Khai báo module
db = MongoEngine(app)
socketio = SocketIO(app, cors_allowed_origins="*",engineio_logger=False)



#Khai báo blueprint
from app.main.controllers import main as main_module
app.register_blueprint(main_module)
