from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from crud_operations import crud_create, crud_read, crud_update, crud_delete
from sample_queries import retrieve_suppliers, retrieve_manufacturer, retrieve_inventory, retrieve_order, retrieve_warehouses

# MongoDB connection string
uri = "mongodb+srv://supply_user:phone@phonesupplychain.zdj9qzg.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Specify the database and collection
database_name = "supplychain"
collection_name = "supplychain_collection"
# Access the specified database and collection
db = client[database_name]
collection = db[collection_name]

# Count the number of documents in the collection
num_documents = collection.count_documents({})
# Print the result
print(f"Number of documents in '{database_name}.{collection_name}': {num_documents}")

if __name__ == "__main__":
    crud_create(collection)
    crud_read(collection)
    crud_update(collection)
    crud_delete(collection)
    print("\n --------------------------------------------------------- \n")
    print("SAMPLE QUERIES and DATA RETRIEVAL \n")
    retrieve_suppliers(db)
    retrieve_manufacturer(db)
    retrieve_inventory(db)
    retrieve_order(db)
    retrieve_warehouses(db)
