from os.path import join, dirname
import imutils
from flask import Blueprint, render_template, Response, request, url_for
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import face_recognition as fr

global capture, rec_frame
capture = 0


def detect_caffe(frame, rec):
    protoPath = join(dirname(__file__), "deploy.prototxt.txt")
    modelPath = join(dirname(__file__), "res10_300x300_ssd_iter_140000.caffemodel")
    net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:
        return frame

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
        face_img = frame[startY:endY, startX:endX]  # извлекаем лицо
    except Exception as e:
        pass

    return frame


class Capture:

    def gen_frames(self):  # генератор кадров
        camera = cv2.VideoCapture(-1)
        camera.set(3, 640)  # set Width
        camera.set(4, 480)  # set Height
        global out, capture, rec_frame

        while True:
            success, frame = camera.read()
            if success:
                frame = imutils.resize(frame, width=600)
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                gray = detect_caffe(frame, 0)

                try:
                    # вывод данных
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(gray, 1))
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass

            else:
                pass
        camera.release()
        cv2.destroyAllWindows()
