import os
import csv
import time
import psycopg2
import random
from datetime import datetime
from create_table_calls import create_database_tables, insert_supplier_data_from_csv, insert_manufacturer_data_from_csv
from create_table_calls import insert_mobilephone_data_from_csv, insert_warehouse_data_from_csv, insert_inventory_data_from_csv
from create_table_calls import insert_orders_data_from_csv, insert_order_details_data_from_csv
from create_indexing import create_index
from create_caching import get_data_with_caching


    # SQL statements to create tables
drop_table_sql=["""    
    DROP TABLE IF EXISTS Supplier;
    DROP TABLE IF EXISTS Inventory;
    DROP TABLE IF EXISTS OrderDetails;
    DROP TABLE IF EXISTS MobilePhone;
    DROP TABLE IF EXISTS Warehouse;
    DROP TABLE IF EXISTS Orders;
    DROP TABLE IF EXISTS Manufacturer;            
    """]


create_tables_sql = [
    """
    CREATE TABLE Supplier (
        SupplierID SERIAL PRIMARY KEY,
        SupplierName VARCHAR(255),
        ContactInfo TEXT,
        Address TEXT
    )
    """,
    """
    CREATE TABLE Manufacturer (
        ManufacturerID SERIAL PRIMARY KEY,
        ManufacturerName VARCHAR(255),
        Country VARCHAR(255),
        ContactInfo TEXT
    )
    """,
    """
    CREATE TABLE MobilePhone (
        MobilePhoneID SERIAL PRIMARY KEY,
        ManufacturerID INT,
        ModelName VARCHAR(255),
        Price DECIMAL(10, 2),
        ReleaseDate DATE,
        FOREIGN KEY (ManufacturerID) REFERENCES Manufacturer(ManufacturerID)
    )
    """,
    """
    CREATE TABLE Warehouse (
        WarehouseID SERIAL PRIMARY KEY,
        Location VARCHAR(255),
        Capacity INT
    )
    """,
    """
    CREATE TABLE Inventory (
        InventoryID SERIAL,
        MobilePhoneID INT,
        WarehouseID INT,
        Quantity INT,
        PurchaseDate DATE,
        FOREIGN KEY (MobilePhoneID) REFERENCES MobilePhone(MobilePhoneID),
        FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID),
        PRIMARY KEY (InventoryID)
    )
    """,
    """
    ALTER TABLE Inventory PARTITION BY RANGE (InventoryID) (
    PARTITION Inventory_P1 VALUES FROM (MINVALUE) TO (100),
    PARTITION Inventory_P2 VALUES FROM (101) TO (200)
    );
    """,
    """
    CREATE TABLE Orders (
        OrderID SERIAL PRIMARY KEY,
        CustomerName VARCHAR(255),
        OrderDate DATE,
        DeliveryDate DATE,
        Status VARCHAR(50)
    )
    """,
    """
    CREATE TABLE OrderDetails (
        OrderDetailID SERIAL PRIMARY KEY,
        OrderID INT,
        MobilePhoneID INT,
        Quantity INT,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (MobilePhoneID) REFERENCES MobilePhone(MobilePhoneID)
    )
    """
]



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


if __name__ == "__main__":


    #PART 1
    # create_database_tables(drop_table_sql,create_tables_sql)
    # insert_supplier_data_from_csv('InputData/Supplier.csv')
    # insert_manufacturer_data_from_csv('InputData/Manufacturer.csv')
    # insert_mobilephone_data_from_csv('InputData/MobilePhone.csv')
    # insert_warehouse_data_from_csv('InputData/Warehouse.csv')
    # insert_inventory_data_from_csv('InputData/Inventory.csv')
    # insert_orders_data_from_csv('InputData/Order.csv')
    # insert_order_details_data_from_csv('InputData/OrderDetails.csv')
    #check_data_insertion()


    #PART 2
    # vertical_fragmentation()
    


    #PART 3 OPTIMIZATION
    #Indexing
    create_index('Supplier', 'SupplierName')
    create_index('Inventory', 'Quantity')
    create_index('OrderDetails', 'OrderID')
    check_index_performance('OrderDetails', 'OrderID', '178')

    #Caching
    order_id = 178
    query = "SELECT * FROM OrderDetails WHERE OrderID = %s"
    start_time = time.time()
    data = get_data_with_caching(query, (order_id,))
    end_time = time.time()
    print(f"Data: {data}")
    print(f"Time taken for the first call: {end_time - start_time} seconds")

    # Timing the second call (cached)
    start_time = time.time()
    data = get_data_with_caching(query, (order_id,))
    end_time = time.time()
    print(f"Data: {data}")
    print(f"Time taken for the second call: {end_time - start_time} seconds")

    # Call the function to check data insertion with random samples -> Proof
    check_data_insertion_random_sample()

    pass