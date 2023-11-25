import subprocess
import os
import csv
import psycopg2
from datetime import datetime

conn = psycopg2.connect(os.environ["DATABASE_URL"])

with open("schema_dump.sql", "w") as f:
    try:
        cursor = conn.cursor()
        cursor.execute("EXPORT SCHEMA ALL TO STDOUT")
        schema_dump = cursor.fetchall()

        for line in schema_dump:
            f.write(line[0])
    except Exception as E:
        print(E)
