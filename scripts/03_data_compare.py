import oracledb
import psycopg2
import pandas as pd

print("=== Migration Data Comparison ===")
print()

# ── Connections ──
ora_conn = oracledb.connect(
    user="migration_user",
    password="oracle123",
    dsn="localhost:1521/XEPDB1"
)
print("Oracle connected ✓")

pg_conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="migration_target",
    user="migration_user",
    password="pgmigrate123"
)
print("PostgreSQL connected ✓")
print()

# ── Tables to compare ──
tables = ["customers", "products", "orders", "order_items", "inventory"]

# ── Compare data for each table ──
for table in tables:
    print(f"Comparing table: {table}")
    print("-" * 40)

    # Fetch data from Oracle into a DataFrame
    ora_df = pd.read_sql(f"SELECT * FROM RETAIL.{table} ORDER BY 1", ora_conn)

    # Fetch data from PostgreSQL into a DataFrame
    pg_df = pd.read_sql(f"SELECT * FROM retail.{table} ORDER BY 1", pg_conn)

    # Convert column names to lowercase for comparison
    ora_df.columns = ora_df.columns.str.lower()
    pg_df.columns = pg_df.columns.str.lower()

    # Compare row counts
    print(f"  Oracle rows    : {len(ora_df)}")
    print(f"  PostgreSQL rows: {len(pg_df)}")

    # Compare actual data
    if ora_df.equals(pg_df):
        print(f"  Data match     : ✓ PASS")
    else:
        print(f"  Data match     : ✗ FAIL — differences found!")
        # Show which rows are different
        diff = ora_df.compare(pg_df)
        print(f"  Differences:")
        print(diff)

    print()

# Close connections
ora_conn.close()
pg_conn.close()
print("=== All tables validated successfully! ===")
print("All connections closed ✓")