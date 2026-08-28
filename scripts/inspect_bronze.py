from src.postgres_client import build_postgres_engine,  list_bronze_schemas, list_tables_in_schema, read_table

def inspect_table(engine, schema_name, table_name):

    df = read_table(engine, schema_name, table_name)

    print(f"----- {schema_name}.{table_name} ------")
    print("\n---- Tipos de datos ----")
    print(df.dtypes)
    print("\n---- Nulls por columna ----")
    print(df.isnull().sum())
    print("\n---- Primeras filas ----")
    print(df.head())

def main():
    engine = build_postgres_engine()
    schemas = list_bronze_schemas(engine)

    for schema_name in schemas:
        tables = list_tables_in_schema(engine,schema_name)
        for table_name in tables:
            inspect_table(engine, schema_name, table_name)

if __name__ == "__main__":
    main()
