# from flask import Flask, render_template, Response, request
# import numpy as np
# import cv2

# app = Flask(__name__)

# # Store the video frame and screen frame
# video_frame = None
# screen_frame = None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video', methods=['POST'])
# def receive_video():
#     global video_frame
#     frame = np.frombuffer(request.data, np.uint8)
#     video_frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
#     return 'OK'

# @app.route('/screen', methods=['POST'])
# def receive_screen():
#     global screen_frame
#     frame = np.frombuffer(request.data, np.uint8)
#     screen_frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
#     return 'OK'

# def generate_video():
#     global video_frame
#     while True:
#         if video_frame is None:
#             continue
#         ret, encoded_frame = cv2.imencode('.jpg', video_frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n\r\n')

# def generate_screen():
#     global screen_frame
#     while True:
#         if screen_frame is None:
#             continue
#         ret, encoded_frame = cv2.imencode('.jpg', screen_frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_video(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/screen_feed')
# def screen_feed():
#     return Response(generate_screen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host="192.168.24.242",debug=True)


from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Store the video frame and screen frame
video_frame = None
screen_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def receive_video(data):
    global video_frame
    frame = base64.b64decode(data)
    nparr = np.frombuffer(frame, np.uint8)
    video_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    emit('video_frame', data, broadcast=True)

@socketio.on('screen_frame')
def receive_screen(data):
    global screen_frame
    frame = base64.b64decode(data)
    nparr = np.frombuffer(frame, np.uint8)
    screen_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    emit('screen_frame', data, broadcast=True)

def video_stream_thread():
    global video_frame
    while True:
        if video_frame is not None:
            _, encoded_frame = cv2.imencode('.jpg', video_frame)
            base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
            socketio.emit('video_frame', base64_frame)
        socketio.sleep(0.01)

def screen_stream_thread():
    global screen_frame
    while True:
        if screen_frame is not None:
            _, encoded_frame = cv2.imencode('.jpg', screen_frame)
            base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
            socketio.emit('screen_frame', base64_frame)
        socketio.sleep(0.01)

if __name__ == '__main__':
    video_thread = socketio.start_background_task(video_stream_thread)
    screen_thread = socketio.start_background_task(screen_stream_thread)
    socketio.run(app, host='192.168.24.242', port=5000)
