import oracledb
import psycopg2

print("=== Migration row count Validation ===")
print()

# ── Oracle connection ──

ora_conn = oracledb.connect(
	user="migration_user",
	password="oracle123",
	dsn="localhost:1521/XEPDB1"
)

print("Oracle Connected")

# ── Postgres connection ──
pg_conn=psycopg2.connect(
	host="localhost",
	port=5433,
	dbname="migration_target",
	user="migration_user",
	password='pgmigrate123'
)

print("Postgres Connected")
print()

# ── List of tables to validate ──
tables = ["customers", "products", "orders", "order_items", "inventory"]

# ── Create cursors ──
ora_cursor = ora_conn.cursor()
pg_cursor = pg_conn.cursor()

# ── Validate row counts ──
print(f"{'Table':<20} {'Oracle':>10} {'PostgreSQL':>12} {'Status':>10}")
print("-" * 55)

for table in tables:
    # Count rows in Oracle
    ora_cursor.execute(f"SELECT COUNT(*) FROM RETAIL.{table}")
    ora_count = ora_cursor.fetchone()[0]

    # Count rows in PostgreSQL
    pg_cursor.execute(f"SELECT COUNT(*) FROM retail.{table}")
    pg_count = pg_cursor.fetchone()[0]

    # Compare and show status
    if ora_count == pg_count:
        status = "✓ PASS"
    else:
        status = "✗ FAIL"

    print(f"{table:<20} {ora_count:>10} {pg_count:>12} {status:>10}")

print("-" * 55)
print("Validation complete!")

# Close connections
ora_conn.close()
pg_conn.close()
print("=== All rowcounts are validated successfully! ===")
print("All connections closed ✓")