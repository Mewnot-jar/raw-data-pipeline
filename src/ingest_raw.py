from src.drive_client import build_drive_service, list_company_folders, list_files_in_company, download_file_to_memory
from src.minio_client import build_minio_client, upload_file, verify_bucket_exists, list_existing_objects_by_drive_id
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
    uploaded_count = 0
    renamed_count = 0
    skipped_count = 0

    #Itera en cada compañia
    for company in companies:
        #Crea una lista de diccionarios guardando cada compañia
        files = list_files_in_company(service, company["id"])

        existing_objects = list_existing_objects_by_drive_id(
            client, MINIO_BUCKET, company["name"]
        )

        #Itera en cada archivo
        for file in files:
            try:
                expected_object_name = f"{company['name']}/{file['name']}"
                drive_file_id = file["id"]
                drive_modified_time = file["modifiedTime"]

                existing = existing_objects.get(drive_file_id)

                if existing == None:
                    action = "new"
                elif existing["object_name"] != expected_object_name:
                    action = "rename"
                elif existing["modified_time"] != drive_modified_time:
                    action = "modified"
                else:
                    action = "no_change"

                if action == "no_change":
                    print(f"El archivo {existing['object_name']} no tiene cambios, se omite.")
                    skipped_count += 1
                    continue

                buffer = download_file_to_memory(service, drive_file_id)
                metadata = {
                    "drive-file-id": drive_file_id,
                    "drive-modified-time": drive_modified_time,
                }
                upload_file(client, MINIO_BUCKET, expected_object_name, buffer, metadata=metadata)

                if action == "rename":
                    old_object_name = existing["object_name"]
                    client.remove_object(MINIO_BUCKET, old_object_name)
                    print(f"Renombrado: {old_object_name} -> {expected_object_name}")
                    renamed_count += 1
                else:
                    print(f"Subido ({action}): {expected_object_name}")
                    uploaded_count += 1
            except Exception as e:
                error_msg = f"{company['name']}/{file['name']} -> {e}"
                print(f"Error: {error_msg}")
                failed_files.append(error_msg)

    print("--- Resumen ---")
    if not failed_files:
        print(f"{uploaded_count} archivo(s) subidos/actualizados")
        print(f"{skipped_count} archivo(s) saltados")
        print(f"{renamed_count} archivo(s) renombrados")
    else:
        print(f"{len(failed_files)} archivo(s) fallaron:")
        for error_msg in failed_files:
            print(f" - {error_msg}")



if __name__ == "__main__":
    main()