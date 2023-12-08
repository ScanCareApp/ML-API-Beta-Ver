import os
import uvicorn
import traceback
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image

from pydantic import BaseModel
from urllib.request import Request
from fastapi import FastAPI, Response, UploadFile, File
from PIL import Image

model = tf.keras.models.load_model('./model_skincare.h5')
app = FastAPI()

# Image processing
def process_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    image = image.resize((350, 350))  # Resize the image as per the model requirements
    image = np.array(image) / 255.0  # Normalize pixel values
    return image

# Health check
@app.get("/")
def index():
    return "API WORKING"


@app.post("/predict_image")
async def predict_skincare(photo: UploadFile = File(...)):
    try:
        response = {"predict_result": None}
        # Check wether the file is an image
        if photo.content_type not in ["image/jpeg", "image/png"]:
            response['predict_result'] = "File is Not an Image"
            return response
        contents = await photo.read()
        processed_image = process_image(contents)
        processed_image = np.expand_dims(processed_image, axis=0)  # Add batch dimension

        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction)
        class_names = ['Age Miracle Serum', 'Age Miracle Whip Cream', 'Men Acne Solution Facial Foam']
        predicted_class_name = class_names[predicted_class]
        response['predict_result'] = predicted_class_name
        return response
    except Exception as e:
        traceback.print_exc()
        return {"predict_result": "Internal Server Error"}


port = os.environ.get("PORT", 8080)
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(app, host='0.0.0.0', port=port)
