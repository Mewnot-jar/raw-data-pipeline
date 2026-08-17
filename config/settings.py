import os
from dotenv import load_dotenv

load_dotenv()

#Drive credentials
CREDENTIALS_PATH = os.getenv("CREDENTIALS")
DRIVE_ROOT_FOLDER_ID = os.getenv("DRIVE_ID")

#Minio credentials
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

#Postgres credentials
HOST_DB = os.getenv("HOST_DB")
PORT_DB = os.getenv("PORT_DB")
DATABASE = os.getenv("DATABASE")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")