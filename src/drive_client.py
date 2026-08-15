import os
from config.settings import CREDENTIALS_PATH
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def build_drive_service():
    
    credentials_path = CREDENTIALS_PATH
    if credentials_path is None:
        raise ValueError("Falta la variable de entorno CREDENTIALS en el .env")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError("La ruta no existe.")
    
    credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    return service

def list_company_folders(service, root_folder_id):
    query = f"'{root_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"

    result = service.files().list(
        q=query,
        fields="files(id, name)"
    ).execute()

    return result["files"]


if __name__ == "__main__":
    service = build_drive_service()
    root_folder_id = os.getenv("DRIVE_ID")
    folder_list = list_company_folders(service, root_folder_id)
    print(f"Conexion exitosa: {service}")
    print(f"Carpetas encontradas: {folder_list}")