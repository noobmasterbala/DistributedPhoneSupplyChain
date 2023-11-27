import os
import csv
import psycopg2
from datetime import datetime

def horizonatl_fragmentation():
    print("Table Inventory has been Horizontal Fragmented with RANGE PARTITIONING")
    print("Column InventoryID is used for partitioning \n")
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    try:
        # cursor.execute("SELECT * FROM inventory")
        cursor.execute("SHOW PARTITIONS FROM TABLE inventory")
        response = cursor.fetchall()
        for row in response:
            print(f"Database: {row[0]}\nTable: {row[1]}\nPartition: {row[2]}\nRange: {row[6]}\nConfig: {row[8]}\n")

    except Exception as E:
        print(E)
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


def vertical_fragmentation():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS Supplier_Name (SupplierID SERIAL PRIMARY KEY, SupplierName VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Supplier_Contact (SupplierID INT PRIMARY KEY, ContactInfo TEXT, Address TEXT)")

        # Insert data into Supplier_Name and Supplier_Contact during vertical fragmentation
        cursor.execute("INSERT INTO Supplier_Name (SupplierID, SupplierName) SELECT SupplierID, SupplierName FROM Supplier")
        cursor.execute("INSERT INTO Supplier_Contact (SupplierID, ContactInfo, Address) SELECT SupplierID, ContactInfo, Address FROM Supplier")


        # Fetch and display data from the fragmented tables
        cursor.execute("SELECT * FROM Supplier_Name")
        supplier_name_data = cursor.fetchall()
        print("Supplier_Name Table (Vertical Fragmentation):")
        for row in supplier_name_data:
            print(row)

        cursor.execute("SELECT * FROM Supplier_Contact")
        supplier_contact_data = cursor.fetchall()
        print("Supplier_Contact Table (Vertical Fragmentation):")
        for row in supplier_contact_data:
            print(row)
    except Exception as E:
        print(E)
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


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



if __name__ == "__main__":
    print("HORIZONTAL FRAGMENTATION \n")
    horizonatl_fragmentation()
    print(" -------------------------------------- \n")
    print("VERTICAL FRAGMENTATION")
    vertical_fragmentation()
    print(" -------------------------------------- \n")
    print("DATABASE REPLICATION ")
    show_replicas()