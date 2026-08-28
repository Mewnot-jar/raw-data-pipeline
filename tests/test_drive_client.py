import pytest
from src.drive_client import build_drive_service, list_company_folders, list_files_in_company, download_file_to_memory
from config.settings import DRIVE_ROOT_FOLDER_ID

def test_build_drive_service_succeeds():
    service = build_drive_service()
    assert service is not None

def test_drive_credentials_are_valid():
    service = build_drive_service()
    companies = list_company_folders(service, DRIVE_ROOT_FOLDER_ID)
    assert isinstance(companies, list)

def test_can_extract_company_list():
    service = build_drive_service()
    companies = list_company_folders(service, DRIVE_ROOT_FOLDER_ID)
    assert isinstance(companies, list)
    for company in companies:
        assert "id" in company
        assert "name" in company

def test_can_extract_files_from_first_company_with_data():
    service = build_drive_service()
    companies = list_company_folders(service, DRIVE_ROOT_FOLDER_ID)

    company_with_file = None
    files = []

    for company in companies:
        files = list_files_in_company(service, company["id"])
        if files:
            company_with_file = company
            break
    if company_with_file is None:
        pytest.skip("Ninguna compañia tiene archivos para probar la extraccion")

    first_file = files[0]
    buffer = download_file_to_memory(service, first_file["id"])
    content = buffer.read()
    assert len(content) > 0