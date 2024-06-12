from flask_restful import Resource
from flask import request, jsonify
import requests
import face_recognition
from PIL import Image
from io import BytesIO
import numpy as np
import json

from . import db
from .models import Staff

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


class AddStaff(Resource):
    def post(self):
        data = request.json
        image_url = data.get('image_url')

        if not image_url:
            return jsonify({'error': 'Image URL is missing', 'success': False}), 400

        response = requests.get(image_url)

        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve image', 'success': False}), 400

        img = Image.open(BytesIO(response.content))
        img_array = np.array(img)
        unknown_encodings = face_recognition.face_encodings(img_array)

        if not unknown_encodings:
            return jsonify({'error': 'No face found in the image', 'success': False}), 400

        encodings_json = json.dumps(unknown_encodings[0].tolist())

        new_staff = Staff(
            staff_id=data.get('staff_id'),
            business_id=data.get('business_id'),
            image_url=image_url,
            staff_phone=data.get('staff_phone'),
            encodings=encodings_json
        )

        db.session.add(new_staff)
        db.session.commit()

        return {'message': 'Staff added successfully', 'success': True}



class VerifyStaff(Resource):
    def post(self):
        data = request.json
        phone = data.get('phone')
        image_url = data.get('url')

        if not phone or not image_url:
            return jsonify({'error': 'Phone or image URL is missing', 'success': False}), 400

        staff = Staff.query.filter_by(staff_phone=phone).first()

        if not staff:
            return jsonify({'error': 'Staff not found', 'success': False}), 404

        response = requests.get(image_url)

        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve image', 'success': False}), 400

        img = Image.open(BytesIO(response.content))

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img_array = np.array(img)

        face_locations = face_recognition.face_locations(img_array)
        
        if not face_locations:
            return jsonify({'error': 'No face found in the image', 'success': False}), 400

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = img.crop((left, top, right, bottom))  # Crop the face region
            face_image = face_image.convert("RGB")  # Convert to RGB format
            face_array = np.array(face_image)  # Convert to numpy array
            unknown_encoding = face_recognition.face_encodings(face_array)

            if not unknown_encoding:
                continue

            matches = face_recognition.compare_faces([json.loads(staff.encodings)], unknown_encoding[0])

            if matches[0]:
                return jsonify({'message': 'Verification successful', 'success': True, 'businessId': staff.business_id})
        
        return jsonify({'message': 'Verification failed', 'success': False})
