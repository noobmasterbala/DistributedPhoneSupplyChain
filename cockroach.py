
from create_table_calls import create_database_tables, insert_supplier_data_from_csv, insert_manufacturer_data_from_csv
from create_table_calls import insert_mobilephone_data_from_csv, insert_warehouse_data_from_csv, insert_inventory_data_from_csv
from create_table_calls import insert_orders_data_from_csv, insert_order_details_data_from_csv

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


if __name__ == "__main__":
    create_database_tables(drop_table_sql,create_tables_sql)
    insert_supplier_data_from_csv('InputData/Supplier.csv')
    insert_manufacturer_data_from_csv('InputData/Manufacturer.csv')
    insert_mobilephone_data_from_csv('InputData/MobilePhone.csv')
    insert_warehouse_data_from_csv('InputData/Warehouse.csv')
    insert_inventory_data_from_csv('InputData/Inventory.csv')
    insert_orders_data_from_csv('InputData/Order.csv')
    insert_order_details_data_from_csv('InputData/OrderDetails.csv')
    pass