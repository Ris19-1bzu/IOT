import cv2
import numpy as np
import asyncio
import face_recognition as fr
import time
import string
import random
from pathlib import Path
import json


def accessGranted(name=None):

	print('открыто')
	if name:
		print('привет',name)


def accessDenied(name=None):

	print('закрыто')
	pass


async def videoProcessing(identifier, imshow=False):
	vstream = cv2.VideoCapture(0)
	vstream.set(3, 640)  # ширина
	vstream.set(4, 480)  # высота
	print('старт')
	await asyncio.sleep(0.1)

	while True:
		# ожидание внешнего сигнала для перывания цикла
		await asyncio.sleep(0.1)

		print('цикл распознавания')
		_, frame = vstream.read()
		ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
		frame = buffer.tobytes()

		scaled = cv2.resize(frame, None, fx=0.5, fy=0.5)
		face_locations = fr.face_locations(scaled)

		for top, right, bottom, left in face_locations:
			# очерчиваем лицо
			cv2.rectangle(scaled, (left, top), (right, bottom), (255, 0, 0), 3)

			top *= 2
			bottom *= 2
			right *= 2
			left *= 2

			face_img = frame[top:bottom, left:right]  # извлекаем лицо

			try:
				await asyncio.sleep(0.1)
				face_encoding = fr.face_encodings(face_img)[0]

			except Exception as e:
				# если не распознается - просто продолжаем цикл
				continue
                
                
            person = identifier.getIDFromEncoding(face_encoding)

			if person is None:
				# Новое лицо,
				# генерируем новый id, и сохраняем
				print('Добавляется новое лицо')
				identifier.addNew(face_img, face_encoding)
				continue

			if identifier.hasAccess(person):
				accessGranted()
			else:
				accessDenied()  

            ret, v = cv2.imencode('.jpg', scaled)
            identifier.setView(v)            