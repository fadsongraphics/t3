# import cv2
import numpy as np
# import requests
import pyautogui
# import time

# # Function to capture video stream
# def capture_video():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         # Resize frame if needed
#         # frame = cv2.resize(frame, (640, 480))
#         # Convert frame to JPEG
#         _, encoded_frame = cv2.imencode('.jpg', frame)
#         # Send frame to server
#         requests.post('http://192.168.24.242:5000/video', data=encoded_frame.tobytes())
#         cv2.imshow('Video Stream', frame)
#         if cv2.waitKey(1) == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# # Function to record screen
# def record_screen():
#     screen_size = (1920, 1080)  # Set your screen size
#     fourcc = cv2.VideoWriter_fourcc(*"XVID")
#     out = cv2.VideoWriter('output.avi', fourcc, 20.0, screen_size)
#     while True:
#         img = pyautogui.screenshot()
#         frame = np.array(img)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         out.write(frame)
#         # Send frame to server
#         _, encoded_frame = cv2.imencode('.jpg', frame)
#         requests.post('http://192.168.24.242:5000/screen', data=encoded_frame.tobytes())
#         cv2.imshow('Screen Record', frame)
#         if cv2.waitKey(1) == ord('q'):
#             break
#     out.release()
#     cv2.destroyAllWindows()

# # Start capturing video stream and screen record in separate threads
# import threading
# video_thread = threading.Thread(target=capture_video)
# screen_thread = threading.Thread(target=record_screen)

# video_thread.start()
# screen_thread.start()


import cv2
import base64
import time
from socketIO_client import SocketIO

# Function to capture video stream
def capture_video():
    cap = cv2.VideoCapture(0)
    socketIO = SocketIO('192.168.24.242', 5000)

    while True:
        ret, frame = cap.read()
        _, encoded_frame = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
        socketIO.emit('video_frame', base64_frame)
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    socketIO.disconnect()

# Function to record screen
def record_screen():
    screen_size = (1920, 1080)  # Set your screen size
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, screen_size)
    socketIO = SocketIO('192.168.24.242', 5000)

    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, encoded_frame = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
        socketIO.emit('screen_frame', base64_frame)
        out.write(frame)
        cv2.imshow('Screen Record', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()
    socketIO.disconnect()

# Start capturing video stream and screen record in separate threads
import threading
video_thread = threading.Thread(target=capture_video)
screen_thread = threading.Thread(target=record_screen)

video_thread.start()
screen_thread.start()
