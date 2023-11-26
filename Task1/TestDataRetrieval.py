import os
import csv
import psycopg2

def check_data_insertion():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    for table in ['Supplier', 'Manufacturer', 'MobilePhone', 'Warehouse', 'Inventory', 'Orders', 'OrderDetails']:
        cursor.execute(f"SELECT * FROM {table} LIMIT 2;") 
        results = cursor.fetchall() 
        print(f"Data from {table}: {results}") 
    cursor.close()
    conn.close()


def check_data_insertion_random_sample():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    for table in ['Supplier', 'Manufacturer', 'MobilePhone', 'Warehouse', 'Inventory', 'Orders', 'OrderDetails']:
        cursor.execute(f"SELECT * FROM {table} ORDER BY RANDOM() LIMIT 10;") 
        results = cursor.fetchall() 
        print(f"Random sample from {table}: {results}") 
    cursor.close()
    conn.close()