from minio import Minio
from config.settings import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

def build_minio_client():
    client = Minio(
        endpoint=MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    return client

if __name__ == "__main__":
    client = build_minio_client()
    exist = client.bucket_exists("bronze")
    print(f"Bucket existe: {exist}")