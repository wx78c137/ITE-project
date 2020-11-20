from app import app, socketio
if __name__ == '__main__':
    socketio.run(app, host='45.117.169.186', port='5000')
