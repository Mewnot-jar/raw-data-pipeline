# raw-data-pipeline

> 🚧 **Proyecto en proceso.** Las capas `raw` y `bronze` están funcionando de punta a punta. La capa `silver` (limpieza real de datos: tipos correctos, manejo de nulls, reglas de negocio) todavía no está implementada.

Un pipeline pequeño de ingeniería de datos que extrae datasets de Kaggle (descargados manualmente y organizados por empresa en Google Drive) hacia un lake con arquitectura inspirada en el patrón medallón, usando MinIO como almacenamiento de objetos y PostgreSQL para la capa estructurada.

## Arquitectura

```
Google Drive
     │  /KaggleDatasets/<Empresa>/archivo.csv
     ▼
ingest_raw.py  ──────────────►  Bucket MinIO "raw"
                                  raw/<empresa>/archivo.csv

ingest_bronze.py
     │  lee cada CSV bajo raw/<empresa>/
     ▼
PostgreSQL (Supabase)
     <empresa>_bronze.<tabla>        (un schema por empresa, una tabla por CSV)
     │
     ▼  pg_dump
Bucket MinIO "bronze"
     bronze/<empresa>/<schema>.sql
```

> **Nota sobre nombres:** este proyecto usa `raw` / `bronze` en vez de los términos clásicos del patrón medallón (`bronze` / `silver`). Acá, `raw` cumple el rol del "bronze" clásico (datos sin tocar), y `bronze` cumple el rol del "silver" clásico (datos estructurados y consultables en Postgres). Una capa `silver` real (limpieza de datos: tipos correctos, manejo de nulls, reglas de negocio) está planeada pero todavía no implementada.

## Estructura del proyecto

```
raw-data-pipeline/
├── src/
│   ├── drive_client.py     # autenticación, listado y descarga de Drive (service account, solo lectura)
│   ├── minio_client.py     # conexión a MinIO, subida/descarga, verificación de buckets
│   ├── postgres_client.py  # conexión a Postgres, carga de schemas/tablas, export a .sql, introspección de bronze
│   ├── ingest_raw.py       # orquestador: Drive → MinIO (raw)
│   └── ingest_bronze.py    # orquestador: raw → Postgres (bronze) → export .sql → MinIO (bronze)
├── scripts/
│   └── inspect_bronze.py   # herramienta de exploración: imprime tipos/nulls/preview de cada tabla en bronze
├── config/
│   └── settings.py         # carga centralizada de variables de entorno
├── tests/
│   ├── test_drive_client.py    # tests de integración (conexión y extracción real contra Drive)
│   └── test_minio_client.py    # tests de verificación de buckets y conectividad
├── .env.example
└── requirements.txt
```

## Requisitos

- Python 3.11+
- Docker (para MinIO local)
- Un proyecto de Google Cloud con la Drive API habilitada y una service account (scope de solo lectura) con acceso a la carpeta de Drive origen
- Un proyecto de Supabase (PostgreSQL) — usa el **Transaction pooler** para las consultas normales y el **Session pooler** para `pg_dump`
- `pg_dump` instalado localmente y disponible en el `PATH`

## Instalación

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\Activate.ps1 en Windows
pip install -r requirements.txt
```

Copia `.env.example` a `.env` y completa:

```
CREDENTIALS=./credentials/service_account.json
DRIVE_ROOT_FOLDER_ID=

MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_BUCKET=raw
MINIO_BRONZE_BUCKET=bronze

POSTGRES_HOST=
POSTGRES_PORT=6543          # Transaction pooler de Supabase
POSTGRES_DUMP_PORT=5432     # Session pooler de Supabase (necesario para pg_dump)
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

Levanta MinIO local:

```bash
docker compose up -d
```

Crea los buckets `raw` y `bronze` desde la consola de MinIO (`http://localhost:9001`) antes de correr el pipeline.

## Uso

```bash
# Drive → MinIO (raw). Detecta archivos nuevos / renombrados /
# modificados / sin cambios por empresa usando el ID de Drive de
# cada archivo, sin volver a subir lo que no cambió.
python -m src.ingest_raw

# raw (MinIO) → Postgres (bronze) → export .sql → MinIO (bronze).
# Recorre todas las empresas encontradas en el bucket raw.
python -m src.ingest_bronze

# Herramienta de exploración: imprime tipos de dato, cantidad de
# nulls y una vista previa de cada tabla en cada schema *_bronze.
# Úsala antes de escribir las reglas de limpieza de la capa silver.
python -m scripts.inspect_bronze
```

Correr la suite de tests (son tests de integración — se conectan de verdad contra Drive/MinIO/Postgres):

```bash
python -m pytest -v
```

## Estado del proyecto / pendientes

- [x] Drive → MinIO (raw), con detección de cambios (nuevo / renombrado / modificado / sin cambios) vía metadata de archivos
- [x] Verificación de buckets, manejo de errores por archivo con resumen al final de la corrida
- [x] raw → Postgres (bronze), un schema por empresa, una tabla por CSV
- [x] Export del schema de Postgres a `.sql`, subido al bucket `bronze`
- [x] `bronze` generalizado para recorrer todas las empresas encontradas en `raw`
- [ ] Capa `silver`: limpieza real de datos (tipos correctos, manejo de nulls, reglas de negocio) — en curso
- [ ] Logging estructurado (reemplazar `print` por `logging`)
- [ ] Reintentos automáticos ante fallos de red
- [ ] Ejecución programada (cron/systemd)

## Stack tecnológico

Python · pandas · SQLAlchemy · psycopg2 · MinIO (Python SDK) · Google Drive API v3 · PostgreSQL (Supabase) · Docker · pytest
