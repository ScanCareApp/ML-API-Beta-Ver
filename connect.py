from google.cloud.sql.connector import Connector
import sqlalchemy

# Function to retrieve CloudSQL instance password from Secret Manager
def access_secret_version(project_id, secret_id, version_id):
    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")

    return payload

# Store CloudSQL instance password in a local variable    
sql_password = access_secret_version('capstone-scancare-406911', 'scancare_sql_pwd','1')


# Initialize Connector object
connector = Connector()

# Function to return database connection
def getconn():
    conn = connector.connect(
        "capstone-scancare-406911:asia-southeast2:scancare",
        "pymysql",
        user = "root",
        password = sql_password,
        db = "bpom",
    )
    return conn

# Create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)