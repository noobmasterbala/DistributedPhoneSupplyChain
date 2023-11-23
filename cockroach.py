import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])

with conn.cursor() as cur:

    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)


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

def create_database_tables():
    # Connect to the PostgreSQL database
    try:
        # conn = psycopg2.connect(database='postgres', user=MY_USERNAME, password=PASSWORD, host='localhost', port='5432')
        cursor = conn.cursor()

        # Create tables
        for drop_table in drop_table_sql:
            cursor.execute(drop_table)
            conn.commit()
        print("dropped all tables")

        for create_table_sql in create_tables_sql:
            cursor.execute(create_table_sql)
            # print("executed table ", create_table_sql )
        conn.commit()
        print("Tables created successfully!")        

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    #entering data here 

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

import os
import csv
import psycopg2

def insert_supplier_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])


    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Insert data into the Supplier table
                    cur.execute("""
                        INSERT INTO Supplier (SupplierID, SupplierName, ContactInfo, Address)
                        VALUES (%s, %s, %s, %s)
                    """, (row['SupplierID'], row['SupplierName'], row['ContactInfo'], row['Address']))

            conn.commit()
            print("Data inserted into the Supplier table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()

def insert_manufacturer_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Insert data into the Manufacturer table
                    cur.execute("""
                        INSERT INTO Manufacturer (ManufacturerID, ManufacturerName, Country, ContactInfo)
                        VALUES (%s, %s, %s, %s)
                    """, (row['ManufactureID'], row['ManufactureName'], row['Country'], row['Contact']))

            conn.commit()
            print("Data inserted into the Manufacturer table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()


def insert_mobilephone_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Extract year from ReleaseYear and construct a date
                    release_year = int(row['ReleaseYear'])
                    release_date = f"{release_year}-01-01"

                    # Insert data into the MobilePhone table
                    cur.execute("""
                        INSERT INTO MobilePhone (MobilePhoneID, ManufacturerID, ModelName, Price, ReleaseDate)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (row['MobilePhoneID'], row['ManufactureID'], row['ModelName'], row['Price'], release_date))

            conn.commit()
            print("Data inserted into the MobilePhone table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()

def insert_warehouse_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Insert data into the Warehouse table
                    cur.execute("""
                        INSERT INTO Warehouse (WarehouseID, Location, Capacity)
                        VALUES (%s, %s, %s)
                    """, (row['WarehouseID'], row['Location'], row['Capacity']))

            conn.commit()
            print("Data inserted into the Warehouse table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()


from datetime import datetime

def insert_inventory_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Adjust the format for the 'm/d/yy' date format
                    purchase_data = row['PurchaseDate']
                    purchase_date = datetime.strptime(purchase_data, '%m/%d/%y')

                    # Insert data into the Inventory table
                    cur.execute("""
                        INSERT INTO Inventory (InventoryID, MobilePhoneID, WarehouseID, Quantity, PurchaseDate)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (row['InventoryID'], row['MobilePhoneID'], row['WarehouseID'], row['Quantity'], purchase_date))

            conn.commit()
            print("Data inserted into the Inventory table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()


def insert_orders_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Adjust the format for the 'm/d/yyyy' date format
                    order_date = datetime.strptime(row['OrderDate'], '%m/%d/%Y')
                    delivery_date = datetime.strptime(row['DeliveryDate'], '%m/%d/%Y') if row['DeliveryDate'] else None

                    # Insert data into the Orders table
                    cur.execute("""
                        INSERT INTO Orders (OrderID, CustomerName, OrderDate, DeliveryDate, Status)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (row['OrderID'], row['CustomerName'], order_date, delivery_date, row['Status']))

            conn.commit()
            print("Data inserted into the Orders table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()

def insert_order_details_data_from_csv(csv_file_path):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])

    try:
        with conn.cursor() as cur:
            with open(csv_file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    # Insert data into the OrderDetails table
                    cur.execute("""
                        INSERT INTO OrderDetails (OrderDetailID, OrderID, MobilePhoneID, Quantity)
                        VALUES (%s, %s, %s, %s)
                    """, (row['OrderDetailID'], row['OrderID'], row['MobilePhoneID'], row['Quantity']))

            conn.commit()
            print("Data inserted into the OrderDetails table successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

    finally:
        conn.close()





if __name__ == "__main__":
    # create_database_tables()
    # insert_supplier_data_from_csv('InputData/Supplier.csv')
    # insert_manufacturer_data_from_csv('InputData/Manufacturer.csv')
    # insert_mobilephone_data_from_csv('InputData/MobilePhone.csv')
    # insert_warehouse_data_from_csv('InputData/Warehouse.csv')
    # insert_inventory_data_from_csv('InputData/Inventory.csv')
    # insert_orders_data_from_csv('InputData/Order.csv')
    # insert_order_details_data_from_csv('InputData/OrderDetails.csv')

    pass