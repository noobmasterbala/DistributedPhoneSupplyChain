import os
import csv
import psycopg2
from datetime import datetime

def show_replicas():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW ZONE CONFIGURATION FROM RANGE default;")
        conn.commit()
        response = cursor.fetchall()
        for i in response:
            print(f"Table: {i[0]}\nConfiguration: {i[1]}\n")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()