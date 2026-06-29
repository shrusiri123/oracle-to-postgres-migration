import oracledb
import psycopg2

print("Starting Oracle connection test...")

# Oracle connection details
username = "migration_user"
password = "oracle123"
host = "localhost"
port = 1521
service = "XEPDB1"

# Connect to Oracle
connection = oracledb.connect(
    user=username,
    password=password,
    dsn=f"{host}:{port}/{service}"
)

print("Connected to Oracle successfully!")
print("Oracle version:", connection.version)

# PostgreSQL connection details
pg_host = "localhost"
pg_port = 5433
pg_database = "migration_target"
pg_username = "migration_user"
pg_password = "pgmigrate123"

# Connect to PostgreSQL
pg_connection = psycopg2.connect(
    host=pg_host,
    port=pg_port,
    dbname=pg_database,
    user=pg_username,
    password=pg_password
)

print("Connected to PostgreSQL successfully!")
pg_cursor = pg_connection.cursor()
pg_cursor.execute("SELECT version();")
pg_version = pg_cursor.fetchone()
print("PostgreSQL version:", pg_version[0])

pg_cursor.execute("SET search_path TO retail, public;")
print("Search path set to retail schema ✓")

# Close all connections
pg_cursor.close()
pg_connection.close()
connection.close()

print("All connections closed successfully!")
print("Script 1 complete!")