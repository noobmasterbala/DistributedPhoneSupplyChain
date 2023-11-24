import os
import csv
import psycopg2
from datetime import datetime

def create_index(table_name, column_name):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    try:
        index_name = f"idx_{table_name}_{column_name}"
        create_index_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name})"
        cursor.execute(create_index_sql)

        conn.commit()
        print(f"Index {index_name} created successfully on {table_name}({column_name})")
    except Exception as error:
        print(f"Error creating index: {error}")
    finally:
        cursor.close()
        conn.close()
