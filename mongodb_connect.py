from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection string
uri = "mongodb+srv://supply_user:phone@phonesupplychain.zdj9qzg.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Specify the database and collection
database_name = "supplychain"  # Replace with your actual database name
collection_name = "supplychain_collection"  # Replace with your actual collection name

# Access the specified database and collection
db = client[database_name]
collection = db[collection_name]

# Count the number of documents in the collection
num_documents = collection.count_documents({})

# Print the result
print(f"Number of documents in '{database_name}.{collection_name}': {num_documents}")
