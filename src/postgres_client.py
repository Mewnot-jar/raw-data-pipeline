from sqlalchemy import create_engine, text
from config.settings import HOST_DB, PORT_DB, DATABASE, USER_DB, PASSWORD_DB

def build_postgres_engine():
    connection_url = (
        f"postgresql://{USER_DB}:{PASSWORD_DB}"
        f"@{HOST_DB}:{PORT_DB}/{DATABASE}"
    )
    return create_engine(connection_url)

def create_schema_if_not_exists(engine, schema_name):
    with engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        connection.commit()

def load_dataframe(engine, df, schema_name, table_name):
    df.to_sql(table_name, engine, schema=schema_name, if_exists="replace", index=False)