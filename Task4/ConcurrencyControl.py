import psycopg2
import os

class ConcurrencyControl:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def reduce_inventory_quantity(self):
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE Inventory SET Quantity = Quantity - 10;")
                cur.execute("COMMIT;")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            
            conn.close()

    def fetch_original_quantities(self):
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT InventoryID, Quantity FROM Inventory ORDER BY InventoryID;")
                return cur.fetchall()
        finally:
            conn.close()

    def verify_quantities(self, original_quantities):
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT InventoryID, Quantity FROM Inventory ORDER BY InventoryID;")
                updated_quantities = cur.fetchall()

                for original, updated in zip(original_quantities, updated_quantities):
                    if original[1] - updated[1] != 20:
                        raise ValueError(f"Quantity mismatch for InventoryID {original[0]}: Original was {original[1]}, now is {updated[1]}")
                print("All quantities reduced correctly.")
        except Exception as e:
            print(f"Verification Error: {e}")
        finally:
            conn.close()
