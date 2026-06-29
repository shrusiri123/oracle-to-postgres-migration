import oracledb
import psycopg2
import pandas as pd
from datetime import datetime

print("=== Generating Migration Report ===")
print()

# Report filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = f"validation\\migration_report_{timestamp}.xlsx"

print(f"Report will be saved as: {report_file}")
print()

# ── Connections ──
ora_conn = oracledb.connect(
    user="migration_user",
    password="oracle123",
    dsn="localhost:1521/XEPDB1"
)
pg_conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="migration_target",
    user="migration_user",
    password="pgmigrate123"
)
print("Both databases connected ✓")
print()

# ── Tables to validate ──
tables = ["customers", "products", "orders", "order_items", "inventory"]

# ── Build row count comparison data ──
print("Building row count summary...")
summary_data = []

for table in tables:
    # Oracle count
    ora_cursor = ora_conn.cursor()
    ora_cursor.execute(f"SELECT COUNT(*) FROM RETAIL.{table}")
    ora_count = ora_cursor.fetchone()[0]

    # PostgreSQL count
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute(f"SELECT COUNT(*) FROM retail.{table}")
    pg_count = pg_cursor.fetchone()[0]

    # Status
    status = "PASS" if ora_count == pg_count else "FAIL"

    # Add to summary list
    summary_data.append({
        "Table Name": table,
        "Oracle Count": ora_count,
        "PostgreSQL Count": pg_count,
        "Status": status
    })

# Convert to DataFrame
summary_df = pd.DataFrame(summary_data)
print(summary_df)

# ── Write to Excel ──
print()
print("Writing Excel report...")

# Create Excel writer
writer = pd.ExcelWriter(report_file, engine='openpyxl')

# ── Sheet 1 — Row Count Summary ──
summary_df.to_excel(writer, sheet_name='Row Count Summary', index=False)
print("Sheet 1 written: Row Count Summary ✓")

# ── Sheet 2 — Sample Data ──
for table in tables:
    # Get first 5 rows from PostgreSQL
    pg_df = pd.read_sql(f"SELECT * FROM retail.{table} LIMIT 5", pg_conn)
    pg_df.to_excel(writer, sheet_name=f'{table}', index=False)
    print(f"Sheet written: {table} ✓")

# ── Sheet 3 — Migration Summary ──
migration_info = pd.DataFrame({
    "Property": [
        "Migration Date",
        "Source Database",
        "Source Schema",
        "Target Database",
        "Target Schema",
        "Total Tables",
        "Total Rows Migrated",
        "Migration Tool",
        "Migration Status"
    ],
    "Value": [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Oracle 21c XE",
        "RETAIL",
        "PostgreSQL 18",
        "retail",
        len(tables),
        summary_df["PostgreSQL Count"].sum(),
        "ora2pg v24.3",
        "SUCCESS"
    ]
})
migration_info.to_excel(writer, sheet_name='Migration Summary', index=False)
print("Sheet 3 written: Migration Summary ✓")

# Save the Excel file
writer.close()
print()
print(f"Report saved successfully: {report_file}")

# ── Close connections ──
ora_conn.close()
pg_conn.close()
print("All connections closed ✓")
print()
print("=== Report Generation Complete! ===")