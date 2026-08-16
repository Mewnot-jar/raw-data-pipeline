from src.drive_client import build_drive_service, list_company_folders, list_files_in_company, download_file_to_memory
from src.minio_client import build_minio_client, upload_file, verify_bucket_exists
from config.settings import DRIVE_ROOT_FOLDER_ID, MINIO_BUCKET

def main():
    #Se construye el servicio de drive y el cliente de Minio
    service = build_drive_service()
    client = build_minio_client()

    #Si el bucket existe seguimos
    verify_bucket_exists(client, MINIO_BUCKET)

    #Lista las compañias dentro del drive con el DRIVE_ROOT_FOLDER_ID
    companies = list_company_folders(service, DRIVE_ROOT_FOLDER_ID)

    #Lista donde se acumularan los archivos que fallen
    failed_files = []

    #Itera en cada compañia
    for company in companies:
        #Crea una lista de diccionarios guardando cada compañia
        files = list_files_in_company(service, company["id"])
        #Itera en cada archivo
        for file in files:
            try:
                #Descarga el archivo actual file["id"] y devuelve el BytesIO con sus bytes
                buffer = download_file_to_memory(service, file["id"])  
                #Arma el string de ruta de destino en Minio
                #Como company name y file name cambian en cada vuelta el string cambia
                object_name = f"{company['name']}/{file['name']}"
                #Le pasa los 4 parametros para subir el archivo
                upload_file(client, MINIO_BUCKET, object_name, buffer)
                print(f"Subido: {object_name}")
            except Exception as e:
                error_msg = f"{company['name']}/{file['name']} -> {e}"
                print(f"Error: {error_msg}")
                failed_files.append(error_msg)
    print("--- Resumen ---")
    if not failed_files:
        print("Todo se subio sin errores")
    else:
        print(f"{len(failed_files)} archivo(s) fallaron:")
        for error_msg in failed_files:
            print(f" - {error_msg}")



if __name__ == "__main__":
    main()