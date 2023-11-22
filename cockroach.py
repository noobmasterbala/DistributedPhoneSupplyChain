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

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()



if __name__ == "__main__":
    create_database_tables()