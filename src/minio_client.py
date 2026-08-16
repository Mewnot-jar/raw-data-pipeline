from minio import Minio
from config.settings import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

#Construye el cliente de Minio con las credenciales de minio en .env
def build_minio_client():
    client = Minio(
        endpoint=MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    return client
#Sube un archivo al bucket especificado, se le entrega el cliente, bucket, nombre de la ruta que tendra el archivo en el bucket
#y los bytes reales del archivo
def upload_file(client, bucket, object_name, file_buffer):
    #Mide el tamaño del archivo en el buffer
    file_length = len(file_buffer.getbuffer())
    #Sube el archivo al bucket en Minio
    client.put_object(bucket, object_name, data=file_buffer, length=file_length)

if __name__ == "__main__":
    #Crea al cliente
    client = build_minio_client()
    #Cheka si existe el bucket
    exist = client.bucket_exists("bronze")
    print(f"Bucket existe: {exist}")