import psycopg2
from retry import retry
import os
import random

class RetryMechanism:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.fail = True

    @retry(tries=3, delay=2)
    def transaction_with_retry(self):
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        try:
            print("Starting transaction to show the implemented Retry mechanism...")
            # Simulate a random failure
            if self.fail:
                self.fail = False
                raise Exception("Simulated Transaction Failure")
            print("Updating inventory...")
            cur.execute("UPDATE Inventory SET Quantity = Quantity - 10;")
            cur.execute("COMMIT;")
            print("Transaction Succeeded: Inventory updated")
        except Exception as e:
            print(f"Transaction Failed with error: {e}")
            cur.execute("ROLLBACK;")
            raise
        finally:
            print("Closing connection...")
            conn.close()
