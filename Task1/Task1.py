
from CreateTables import createTables
from InsertData import insert_supplier_data_from_csv, insert_manufacturer_data_from_csv
from InsertData import insert_mobilephone_data_from_csv, insert_warehouse_data_from_csv, insert_inventory_data_from_csv
from InsertData import insert_orders_data_from_csv, insert_order_details_data_from_csv
from TestDataRetrieval import check_data_insertion, check_data_insertion_random_sample

def insertData():
    insert_supplier_data_from_csv('InputData/Supplier.csv')
    insert_manufacturer_data_from_csv('InputData/Manufacturer.csv')
    insert_mobilephone_data_from_csv('InputData/MobilePhone.csv')
    insert_warehouse_data_from_csv('InputData/Warehouse.csv')
    insert_inventory_data_from_csv('InputData/Inventory.csv')
    insert_orders_data_from_csv('InputData/Order.csv')
    insert_order_details_data_from_csv('InputData/OrderDetails.csv')

def testInsertionAndRetrieval():
    check_data_insertion()
    check_data_insertion_random_sample()

#PART 1
if __name__ == "__main__":
    createTables()
    insertData()
    testInsertionAndRetrieval()