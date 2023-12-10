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
from connect import create_connection_pool
from sqlalchemy import text

model = tf.keras.models.load_model('./model_skincare.h5')
app = FastAPI()

# Initialize the connection pool
pool = create_connection_pool()

# Image processing
def process_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    image = image.resize((350, 350))  # Resize the image as per the model requirements
    image = np.array(image) / 255.0  # Normalize pixel values
    return image

# Function to fetch product details
def fetch_product_details(product_name):
    with pool.connect() as conn:
        sql_statement = text("SELECT NoBPOM, `Nama Produk`, gambar FROM produk WHERE `Nama Produk` = :product_name;")
        sql_statement = sql_statement.bindparams(product_name=product_name)
        result = conn.execute(sql_statement)
        query_results = result.fetchall()
    formatted_results = [{'NoBPOM': row[0], 'product_name': row[1], 'image_url': row[2]} for row in query_results]
    return formatted_results

# Health check
@app.get("/")
def index():
    return "API WORKING"

# Endpoint for image prediction
@app.post("/predict_image")
async def predict_image(photo: UploadFile = File(...)):
    try:
        response = {"product_details": None}
        if photo.content_type not in ["image/jpeg", "image/png"]:
            response['error_message'] = "File is Not an Image"
            return response
        
        contents = await photo.read()
        processed_image = process_image(contents)
        processed_image = np.expand_dims(processed_image, axis=0)

        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction)
        class_names = ['Age Miracle Serum', 'Age Miracle Whip Cream', 'Men Acne Solution Facial Foam']
        predicted_class_name = class_names[predicted_class]
        
        product_details = fetch_product_details(predicted_class_name)
        if not product_details:
            return {"error_message": "Product details not found"}

        response['product_details'] = product_details

        return response
    
    except Exception as e:
        traceback.print_exc()
        return {"error_message": str(e)}

port = os.environ.get("PORT", 8080)
print(f"Listening to http://localhost:{port}")
uvicorn.run(app, host='localhost', port=port)
