import os
from config.settings import CREDENTIALS_PATH, DRIVE_ROOT_FOLDER_ID
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

#Construye el servicio drive con las credenciales CREDENTIALS_PATH
def build_drive_service():
    
    credentials_path = CREDENTIALS_PATH
    if credentials_path is None:
        raise ValueError("Falta la variable de entorno CREDENTIALS en el .env")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError("La ruta no existe.")
    
    credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    return service

#Lista las carpetas de las compañias en el drive
def list_company_folders(service, root_folder_id):
    query = f"'{root_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"

    result = service.files().list(
        q=query,
        fields="files(id, name)"
    ).execute()

    return result["files"]

#Lista los archivos dentro de la compañia con company_folder_id
def list_files_in_company(service, company_folder_id):
    query = f"'{company_folder_id}' in parents"
    
    result = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()
    
    return result["files"]

if __name__ == "__main__":
    #Construye el servicio
    service = build_drive_service()
    #Consigue el ID de la carpeta de Drive dentro de .env
    root_folder_id = DRIVE_ROOT_FOLDER_ID
    #Imprime el servicio
    print(f"Conexion exitosa: {service}")

    #Lista las carpetas de cada compañia en el Drive
    companies = list_company_folders(service, root_folder_id)
    print(f"Empresas: {companies}")

    #Consigue la primera compañia 
    first_company = companies[0]
    #Busca en la primera compañia conseguida y trae sus archivos
    files = list_files_in_company(service, first_company["id"])
    #imprime los archivos dentro de la compañia (carpeta)
    print(f"Archivos en {first_company["name"]}: {files}")