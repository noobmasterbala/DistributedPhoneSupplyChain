import os
import csv
import psycopg2
from datetime import datetime
import time

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



def check_index_performance(table_name, column_name, search_value):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    try:
        # Construct the query
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
        start_time = time.time()

        # Execute the query
        cursor.execute(query, (search_value,))

        # Fetch the results (optional, depending on whether you want to see the data)
        results = cursor.fetchall()

        # Measure the time taken
        end_time = time.time()
        time_taken = end_time - start_time

        print(f"Query executed in {time_taken:.4f} seconds")

        # Optionally print the results
        for row in results:
            print(row)
    except Exception as error:
        print(f"Error executing query: {error}")
    finally:
        cursor.close()
        conn.close()