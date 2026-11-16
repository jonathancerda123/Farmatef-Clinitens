# Laboratorio PostgreSQL de CliniTENS

Ejecuta los comandos desde la raíz del repositorio. Se requiere Docker con contenedores Linux y Compose, y un entorno Python con los paquetes de `requirements.txt` y `psycopg[binary]`. Instala el driver en el entorno de QA.

```powershell
python -m pip install "psycopg[binary]>=3.1.12,<4"
docker compose -f qa/postgres/compose.yaml up -d --wait
python manage.py test FarmaTEFApp --settings=core.postgres_test_settings
```

La instancia usa PostgreSQL 17 y publica solo en `127.0.0.1:55432`. Las credenciales son ficticias. Django crea y descarta `test_clinitens_qa`. Los datos del ensayo residen en memoria temporal. El test concurrente envía dos entregas de cinco unidades sobre un único lote de siete unidades y exige un saldo de dos, una entrega confirmada y la reversión de la otra.

## 500 transacciones de base de datos

```powershell
docker compose -f qa/postgres/compose.yaml exec -T postgres pgbench -U clinitens_qa -i -s 1 clinitens_qa
docker compose -f qa/postgres/compose.yaml exec -T postgres pgbench -U clinitens_qa -c 10 -j 2 -t 50 -r clinitens_qa
docker compose -f qa/postgres/compose.yaml down
```

`pgbench` mide su carga SQL sintética con 10 clientes, 2 hilos y 50 transacciones por cliente. Guarda la versión de PostgreSQL, CPU y RAM asignadas, transacciones completadas, errores, latencia media y TPS. La capacidad de atender tráfico web requiere una medición HTTP con infraestructura y perfiles de carga definidos.

[Imagen oficial de PostgreSQL](https://hub.docker.com/_/postgres) · [pgbench](https://www.postgresql.org/docs/17/pgbench.html) · [Django y PostgreSQL](https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes)
