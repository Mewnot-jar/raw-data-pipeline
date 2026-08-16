from src.drive_client import build_drive_service, list_company_folders, list_files_in_company, download_file_to_memory
from src.minio_client import build_minio_client, upload_file
from config.settings import DRIVE_ROOT_FOLDER_ID

def main():
    service = build_drive_service()
    client = build_minio_client()

    companies = list_company_folders(service, DRIVE_ROOT_FOLDER_ID)
    company = companies[1]

    files = list_files_in_company(service, company["id"])
    first_file = files[0]

    buffer = download_file_to_memory(service, first_file["id"])
    object_name = f"{company['name']}/{first_file['name']}"
    bucket = "bronze"
    upload_file(client, bucket, object_name, buffer)

    print(f"Subido: {object_name}")

if __name__ == "__main__":
    main()