import psycopg2
import functools
import os

@functools.lru_cache(maxsize=100)
def get_data_with_caching(query, parameters):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    try:
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        return results
    except Exception as error:
        print(f"Error: {error}")
        return None
    finally:
        cursor.close()
        conn.close()

# Example usage:
# Assuming you want to fetch data from the Supplier table for a specific SupplierName
# supplier_name = "Some Supplier Name"
# query = "SELECT * FROM Supplier WHERE SupplierName = %s"
# data = get_data_with_caching(query, (supplier_name,))
# print(data)
