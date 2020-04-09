import os
import sys
import csv

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil
from PIL import Image


# Declare a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model.h5'

# Load trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
print('Model loaded. Serving at http://127.0.0.1:5000/')


def model_predict(img, model):
    img = img.resize((32, 32), Image.ANTIALIAS)

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    
    #Make a prediction
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)
        
        # Make prediction
        preds = model_predict(img, model)
        print("Preds: ", list(preds))
        
        # Get classes
        with open('../stone-classifier-webapp/static/classes.csv', 'r') as read:
            reader = csv.reader(read)
            classes = list(reader)

        # Return result
        return jsonify(result=str(*classes[preds.argmax()]).capitalize())

    return None


if __name__ == '__main__':

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
