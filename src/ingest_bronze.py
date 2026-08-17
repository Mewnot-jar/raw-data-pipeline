import pandas as pd
from src.minio_client import build_minio_client, list_objects_in_bucket, download_object_to_memory, list_company_prefixes
from src.postgres_client import build_postgres_engine, create_schema_if_not_exists, load_dataframe
from config.settings import MINIO_BUCKET

def sanitize_name(name):
    return name.lower().replace(" ", "_").replace("'", "")

def main():
    minio_client = build_minio_client()
    engine = build_postgres_engine()

    companies = list_company_prefixes(minio_client, MINIO_BUCKET)
    print(f"Empresas encotradas en raw: {companies}")

    for company in companies:
        schema_name = sanitize_name(company)
        create_schema_if_not_exists(engine, schema_name)
        object_names = list_objects_in_bucket(minio_client, MINIO_BUCKET, prefix=f"{company}/")

        for object_name in object_names:
            buffer = download_object_to_memory(minio_client, MINIO_BUCKET, object_name)
            df = pd.read_csv(buffer)

            file_name = object_name.split("/")[-1] #"annex1.csv"
            table_name = sanitize_name(file_name.rsplit(".", 1)[0]) #"annex1"
            load_dataframe(engine, df, schema_name, table_name)
            print(f"Cargado: {schema_name}.{table_name} ({len(df)} filas)")

if __name__ == "__main__":
    main()