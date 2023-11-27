def retrieve_suppliers(db):
#Retrieve number of Suppliers:
    all_suppliers = db.supplier.find({})
    l = 0
     
    for supplier in all_suppliers:
        l +=1
        supplier_sample = supplier
    print(" Retrieving Number of suppliers : ", l)
    print(" Sample retrieval data from supplier:", supplier_sample)

def retrieve_manufacturer(db):
#Retrieve number of MobilePhones Manufactured in a Specific Year
    manufactured_year_to_retrieve = 2021
    mobilephones_in_year = db.mobilePhone.find({"ReleaseYear": manufactured_year_to_retrieve})
    l = 0
    for mobilephone in mobilephones_in_year:
        # print(mobilephone)
        l+=1
        sample_mobilephone = mobilephone
    print("\n \n Number of mobilephones manufactured in 2021", l)
    print("Sample retrieval data from manufacturer :", sample_mobilephone)


def retrieve_inventory(db):
#Retrieve Inventory Items in a Specific Warehouse:
    warehouse_id_to_retrieve = 80  # Replace with the desired WarehouseID
    inventory_in_warehouse = db.inventory.find({"WarehouseID": warehouse_id_to_retrieve})
    print("\n")
    print("Inventory items present in warehouse 80")
    for inventory_item in inventory_in_warehouse:
        print(inventory_item)


def retrieve_order(db):
#Retrieve OrderDetails for a Specific MobilePhone 80:
    mobilephone_id_to_retrieve = 68  # Replace with the desired MobilePhoneID
    order_details_for_mobilephone = db.orderDetails.find({"MobilePhoneID": mobilephone_id_to_retrieve})
    print("\n")
    print("Retrieve OrderDetails for a Specific MobilePhone 68")
    for order_detail in order_details_for_mobilephone:
        print(order_detail)


def retrieve_warehouses(db):
#Retrieve Warehouses in a Specific Location - Sweden
    location_to_retrieve = "Sweden"  # Replace with the desired location
    warehouses_in_location = db.warehouse.find({"Location": location_to_retrieve})
    print("\n")
    print("Retrieve Warehouses in a Specific Location - Sweden")
    for warehouse in warehouses_in_location:
        print(warehouse)
