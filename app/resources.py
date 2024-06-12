from flask_restful import Resource
from flask import request, jsonify
import requests
import face_recognition
from PIL import Image
from io import BytesIO
import numpy as np

from . import db
from .models import Staff

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


class AddStaff(Resource):
    def post(self):
        data = request.json
        image = data.get('image_url')

        if not image:
            return jsonify({'error': 'image url is missing', 'success': False}), 400

        response = requests.get(image)

        img = Image.open(BytesIO(response.content))
        img_array = np.array(img)
        unknown_encodings = face_recognition.face_encodings(img_array)

        # Save staff data to the database
        new_staff = Staff(
            staff_id=data.get('staff_id'),
            business_id=data.get('business_id'),
            image_url=image,
            staff_phone=data.get('staff_phone'),
            encodings=unknown_encodings 
        )

        db.session.add(new_staff)
        db.session.commit()

        return {'message': 'Staff added successfully', 'success': True}