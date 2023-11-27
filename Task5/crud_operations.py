
def crud_create(collection):
    """CREATE (INSERT) OPERATION"""

    # Document to be inserted
    new_document = {
        "name": "New Phone",
        "brand": "Brand XYZ",
        "price": 599.99,
        "stock": 100
    }

    # Insert the document into the collection
    result = collection.insert_one(new_document)

    # Print the result
    print("\nCREATE (INSERT) OPERATION:")
    if result.inserted_id:
        print(f"Document successfully inserted with ID: {result.inserted_id}")
    else:
        print("Failed to insert document.")

def crud_read(collection):
    """READ (QUERY) OPERATION"""
    # Find a document by a specific field (e.g., name)
    query = {"name": "New Phone"}
    found_document = collection.find_one(query)

    # Print the result
    print("\nREAD (QUERY) OPERATION:")
    if found_document:
        print("Found document:")
        print(found_document)
    else:
        print("Document not found.")

def crud_update(collection):
    """UPDATE OPERATION"""
    # Update a document by a specific field (e.g., name)
    query = {"name": "New Phone"}
    update_data = {"$set": {"price": 649.99, "stock": 50}}

    # Update the document
    update_result = collection.update_one(query, update_data)

    # Print the result
    print("\nUPDATE OPERATION:")
    if update_result.modified_count > 0:
        print(f"Document successfully updated. Modified {update_result.modified_count} field(s).")
    else:
        print("No document was updated.")

def crud_delete(collection):
    """DELETE OPERATION"""
    # Delete a document by a specific field (e.g., name)
    query = {"name": "New Phone"}

    # Delete the document
    delete_result = collection.delete_one(query)

    # Print the result
    print("\nDELETE OPERATION:")
    if delete_result.deleted_count > 0:
        print(f"Document successfully deleted. Deleted {delete_result.deleted_count} document(s).")
    else:
        print("No document was deleted.")
