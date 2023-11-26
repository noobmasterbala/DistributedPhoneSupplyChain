import os
import csv
import psycopg2
from datetime import datetime


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