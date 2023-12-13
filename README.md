# ML-API-Beta-Ver

This API handles user input of skincare product images and returns the predicted name of the skincare product. It checks if the uploaded file is an image (JPEG or PNG), processes the image, performs prediction using a model, and returns the predicted name of the skincare product. If an error occurs during this process, it returns an appropriate error message. This API is currently in development to also retrieve product details based on data stored in a database.

# ML-API-Beta-Ver

This API handles user input of skincare product images and returns predicted details about the skincare product. It checks the uploaded file's format, processes the image, predicts the skincare product using a trained machine learning model, and returns the product's details based on data stored in a database.

## Endpoint Description

### Image Prediction (`POST /predict_image`)
Predicts the skincare product name from the provided image and retrieves its details.

#### Request:
- **Endpoint:** `/predict_image`
- **Method:** `POST`
- **Request Body (Form Data):** 
  - `photo`: Image file (JPEG or PNG)

#### Responses:
- **Success (200):** Returns details about the predicted skincare product.
    ```json
    {
      "product_details": {
        "NoBPOM": "NA49200100042",
        "product_name": "Product A",
        "image_url": "https://example.com/images/ProductA.jpg",
        "ingredients": [
          {
            "idIngredient": 1,
            "nameIngredients": "Ingredient 1",
            "fungsi": "Function 1 for Ingredient 1"
          },
          {
            "idIngredient": 2,
            "nameIngredients": "Ingredient 2",
            "fungsi": "Function 1 for Ingredient 2"
          },
          {
            "idIngredient": 3,
            "nameIngredients": "Ingredient 3",
            "fungsi": "Function 1 for Ingredient 3"
          }
        ]
      }
    }
    ```
- **Error (400):** Invalid file format (Not an image).
- **Error (500):** Internal server error.

## Usage

1. **Health Check Endpoint:**
    - **Endpoint:** `/`
    - **Method:** `GET`
    - **Description:** Health check for API status. Returns "API WORKING" when the API is operational.

2. **Image Prediction:**
    - **Endpoint:** `/predict_image`
    - **Method:** `POST`
    - **Description:** Predicts the skincare product from the provided image.

