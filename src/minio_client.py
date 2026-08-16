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

def upload_file(client, bucket, object_name, file_buffer):
    file_length = len(file_buffer.getbuffer())
    client.put_object(bucket, object_name, data=file_buffer, length=file_length)

if __name__ == "__main__":
    client = build_minio_client()
    exist = client.bucket_exists("bronze")
    print(f"Bucket existe: {exist}")