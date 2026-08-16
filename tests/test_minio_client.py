import pytest
from src.minio_client import build_minio_client, verify_bucket_exists
from config.settings import MINIO_BUCKET

def test_verify_bucket_exists_with_real_bucket():
    client = build_minio_client()
    verify_bucket_exists(client, MINIO_BUCKET)


def test_verify_bucket_exists_without_bucket():
    client = build_minio_client()
    with pytest.raises(ValueError):
        verify_bucket_exists(client, "not-real-bucket")