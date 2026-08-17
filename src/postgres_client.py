import os
import io
import subprocess
from sqlalchemy import create_engine, text
from config.settings import HOST_DB, PORT_DB, DATABASE, USER_DB, PASSWORD_DB, DUMP_PORT_DB

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

def export_schema_to_sql(schema_name):
    try:
        result = subprocess.run(
            [
                "pg_dump",
                "-h", HOST_DB,
                "-p", DUMP_PORT_DB,
                "-U", USER_DB,
                "-d", DATABASE,
                "-n", schema_name,
                "--no-owner",
                "--no-privileges",
            ],
            env={**os.environ, "PGPASSWORD": PASSWORD_DB},
            capture_output=True,
            check=True
        )
    except FileNotFoundError:
        raise RuntimeError(
            "pg_dump no esta instalado o no esta en el PATH."
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"pg_dump fallo: {e.stderr.decode()}")
    return io.BytesIO(result.stdout)

def load_dataframe(engine, df, schema_name, table_name):
    df.to_sql(table_name, engine, schema=schema_name, if_exists="replace", index=False)