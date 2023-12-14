# Machine Learning Model API

This API handles user input of skincare product image and returns details about the predicted skincare product. It checks the uploaded file's format (JPEG or PNG), processes the image, predicts the skincare product using a machine learning model, and returns the product's details based on data stored in a database. If an error occurs during this process, it returns an appropriate error message.
   
## Endpoint Description

### Image Prediction (`POST /predict_image`)
Predicts the skincare product name from the provided image, retrieves its details from database, and returns it.

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
    - **Description:** Predicts the skincare product from the provided image. Returns details about the predicted skincare product.

## Preparation and Prerequisites

### Set Up Google Cloud

1. **Creating a Project on Google Cloud**
    - Open [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or use an existing one

2. **Creating a SQL Instance on Google Cloud**
    - Create a MySQL instance
    - Set a password for the root user
    - Store the password in Secret Manager

4. **Creating a Database on Google Cloud**
   - Upload `bpom.sql` to Cloud Storage
   - Import the database into the MySQL instance

### Authenticate to Secret Manager Locally
(If you want to run the application locally)

1. **Installing Google Cloud SDK**
    - Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

2. **Logging into Google Cloud**
    - Run the following command for authentication:
      ```bash
      gcloud auth application-default login
      ```

## Running the Application Locally

1. **Cloning the Repository**
    ```bash
    git clone <repository_url>
    cd <project_folder>
    ```

2. **Installing Requirements**
    ```bash
    pip install -r requirements.txt
    ```

3. **Running the FastAPI Application**
    - Update the run configuration in `main.py` or `app.py`:
        ```python
        if __name__ == "__main__":
            import uvicorn
            
            uvicorn.run(app, host='localhost', port=8000)  # Use any desired port number
        ```

4. **Starting the Local Server**
    ```bash
    uvicorn main:app --reload
    ```

5. **Accessing the API**
    - Utilize the provided API endpoints as documented earlier.

## Deployment
