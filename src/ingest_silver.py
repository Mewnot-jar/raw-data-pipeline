from src.postgres_client import build_postgres_engine, list_bronze_schemas, list_tables_in_schema, read_table, create_schema_if_not_exists, load_dataframe
from src.standardize import auto_clean

def main():
    engine = build_postgres_engine()

    bronze_schemas = list_bronze_schemas(engine)
    print(f"Schemas bronze encontrados: {bronze_schemas}")

    for bronze_schema in bronze_schemas:
        silver_schema = bronze_schema.replace("_bronze", "_silver")
        create_schema_if_not_exists(engine, silver_schema)

        tables = list_tables_in_schema(engine, bronze_schema)

        for table_name in tables:
            df = read_table(engine, bronze_schema, table_name)
            df = auto_clean(df)

            load_dataframe(engine, df, silver_schema, table_name)
            print(f"Limpiado: {bronze_schema}.{table_name} -> {silver_schema}.{table_name}")
if __name__ == "__main__":
    main()