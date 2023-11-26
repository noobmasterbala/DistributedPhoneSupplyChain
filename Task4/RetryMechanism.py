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
            # Simulate a random failure
            if self.fail:
                self.fail = False
                raise Exception("Simulated Transaction Failure")
            # Perform successful operation here
            cur.execute("UPDATE Inventory SET Quantity = Quantity - 10;")
            cur.execute("COMMIT;")
            print("Transaction Succeeded")
        except Exception as e:
            print(f"Transaction Failed with error: {e}")
            cur.execute("ROLLBACK;")
            raise
        finally:
            conn.close()