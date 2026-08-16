from minio import Minio
from config.settings import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET


def verify_bucket_exists(client, bucket):
    if not client.bucket_exists(bucket):
        raise ValueError(
            f"El Bucket '{bucket}' no existe en MinIO. Crealo antes de correr el script."
        )

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
def upload_file(client, bucket, object_name, file_buffer, metadata=None):
    #Mide el tamaño del archivo en el buffer
    file_length = len(file_buffer.getbuffer())
    #Sube el archivo al bucket en Minio
    client.put_object(
        bucket, 
        object_name, 
        data=file_buffer, 
        length=file_length,
        metadata=metadata
    )
def get_drive_metadata(stat):
    normalized =  {k.lower(): v for k, v in (stat.metadata or {}).items()}
    return{
        "drive_file_id": normalized.get("x-amz-meta-drive-file-id"),
        "drive_modified_time": normalized.get("x-amz-meta-drive-modified-time")
    }

def list_existing_objects_by_drive_id(client, bucket, company_name):

    existing = {}    

    objects = client.list_objects(bucket, prefix=f"{company_name}/", recursive=True)

    for obj in objects:
        stat = client.stat_object(bucket, obj.object_name)
        meta = get_drive_metadata(stat)
        if meta["drive_file_id"]:
            existing[meta["drive_file_id"]] = {
                "object_name": obj.object_name,
                "modified_time": meta["drive_modified_time"],
            }
    return existing



if __name__ == "__main__":
    #Crea al cliente
    client = build_minio_client()
    #Cheka si existe el bucket
    exist = client.bucket_exists(MINIO_BUCKET)
    print(f"Bucket existe: {exist}")