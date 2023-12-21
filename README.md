# Machine Learning Model API

This API handles user input of skincare product image and returns details about the predicted skincare product. It checks the uploaded file's format (JPEG or PNG), processes the image, predicts the skincare product using a machine learning model, and returns the product's details based on data stored in a database. If an error occurs during this process, it returns an appropriate error message. 

## Access Our Deployed API : 
[ML-API](https://scancare-ml-api-lxntso327q-et.a.run.app/)

## Table Of Contents
1. [Machine Learning Model API](#machine-learning-model-api)
   - [Image Prediction (`POST /predict_image`)](#image-prediction-post-predict_image)
   - [Health Check Endpoint (`GET /`)](#health-check-endpoint-get)
2. [Preparation and Prerequisites](#preparation-and-prerequisites)
   - [Set Up Google Cloud](#set-up-google-cloud)
   - [Authenticate to Secret Manager Locally](#authenticate-to-secret-manager-locally)
3. [Running the Application Locally](#running-the-application-locally)
4. [Deploying the Application to Cloud Run](#deploying-the-application-to-cloud-run)

## Endpoint Description

### Image Prediction (`POST /predict_image`)
Predicts the skincare product name from the provided image, retrieves its details from database, and returns it.

#### Request:
- **Endpoint:** `/predict_image`
- **Method:** `POST`
- **Request Body (Form Data):** 
  - `photo`: Image file (JPEG or PNG)

#### Responses:
- **200 OK:** Returns details about the predicted skincare product.
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
- **400 Bad Request:**
  ```json
  {
     "detail": "File is Not an Image"
  }
  ```
- **500 Internal Server Error:**
   ```json
  {
     "detail": "Internal Server Error"
  }
  ```

### Health Check Endpoint (`GET /`)
Health check for API status.

#### Request:
- **Endpoint:** `/`
- **Method:** `GET`

#### Responses:
- **200 OK:** Returns "API WORKING".

## Preparation and Prerequisites

### Set Up Google Cloud

1. **Creating a Project on Google Cloud**
    - Open [Google Cloud Console](https://console.cloud.google.com/)
    - Create a new project or use an existing one

2. **Creating a SQL Instance on Google Cloud**
    - Create a MySQL instance
    - Set a password for the root user
    - Store the password in Secret Manager, name it as `scancare_sql_pwd`

4. **Creating a Database on Google Cloud**
   - Upload `bpom.sql` to Cloud Storage
   - Import the database into the MySQL instance

### Authenticate to Secret Manager Locally
(If you want to run the application locally)

1. **Installing Google Cloud SDK**
    - Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

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

3. **Modifying Access to Secret Manager**
   - Navigate to `connect.py` file
   - Find these sections:
     ```python
     sql_password = access_secret_version('YOUR_PROJECT_ID', 'scancare_sql_pwd','1')
     ```
   - Update `YOUR_PROJECT_ID` with your Google Cloud project ID

4. **Modifying Connection to Database**
   - Navigate to `connect.py` file
   - Find these sections:
     ```python
     def getconn():
       conn = connector.connect(
          "YOUR_SQL_INSTANCE_CONNECTION_NAME",
          "pymysql",
          user = "root",
          password = sql_password,
          db = "bpom",
       )
       return conn
     ```
   - Update `YOUR_SQL_INSTANCE_CONNECTION_NAME` with the connection name of your SQL instance

5. **Running the FastAPI Application**
    - Update the run configuration in `main.py`:
        ```python
        port = int(os.environ.get('PORT', 8080))
        print(f"Listening to http://localhost:{port}")
        uvicorn.run(app, host='localhost', port=port)
        ```

6. **Starting the Local Server**
    ```bash
    python main.py
    ```

7. **Accessing the API**
    - Utilize the provided API endpoints as documented earlier

### Testing With FastAPI Swagger UI
- View Swagger UI: `http://localhost:8080/docs` on your browser

## Deploying the Application to Cloud Run
```bash
# Cloning the Repository
git clone <repository_url>

# Change to the destined directory
cd <project_folder>

# Create a Docker Artifact Repository in a specified region
gcloud artifacts repositories create YOUR_REPOSITORY_NAME --repository-format=docker --location=YOUR_REGION

# Build Docker image for the ML API
docker buildx build --platform linux/amd64 -t YOUR_IMAGE_PATH:YOUR_TAG --build-arg PORT=8080 .

# Push the Docker image to the Artifact Repository
docker push YOUR_IMAGE_PATH:YOUR_TAG

# Deploy the Docker image to Cloud Run with allocated memory
gcloud run deploy --image YOUR_IMAGE_PATH:YOUR_TAG --memory 3Gi

# Fetching the service account associated with the newly deployed Cloud Run service
SERVICE_ACCOUNT=$(gcloud run services describe YOUR_SERVICE_NAME --platform=managed --region=YOUR_REGION --format="value(serviceAccountEmail)")

# Grant necessary IAM roles to the service account linked to the Cloud Run service
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member=serviceAccount:${SERVICE_ACCOUNT} --role=roles/secretmanager.secretAccessor

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member=serviceAccount:${SERVICE_ACCOUNT} --role=roles/cloudsql.client
```

## Developer
This project developed by:
* [Tsania Magistra Rahma Insani](https://github.com/tsaniamagistra)
* [Ni Putu Adnya Puspita Dewi](https://github.com/adnyaaa)
