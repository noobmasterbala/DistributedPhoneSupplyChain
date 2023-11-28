import threading
import os
from ConcurrencyControl import ConcurrencyControl
from RetryMechanism import RetryMechanism


class Task4:
    def __init__(self, inventory_operations, retryMech):
        self.inventory_operations = inventory_operations
        self.retryMech = retryMech

    def run(self):
        # Fetch original quantities
        original_quantities = self.inventory_operations.fetch_original_quantities()

        print("We reduce the quantities of inventory from two threads and verify that the transactions are executed in correct sequence")
        # Create and start threads
        thread1 = threading.Thread(target=self.inventory_operations.reduce_inventory_quantity, name = "Thread1")
        thread2 = threading.Thread(target=self.inventory_operations.reduce_inventory_quantity, name = "Thread2")
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        # Verify the quantities after thread execution
        self.inventory_operations.verify_quantities(original_quantities)

        self.retryMech.transaction_with_retry()

    @staticmethod
    def main():
        connection_string = os.environ["DATABASE_URL"]  # Replace with your actual connection string
        inventory_operations = ConcurrencyControl(connection_string)
        retryMech = RetryMechanism(connection_string)
        task4 = Task4(inventory_operations, retryMech)
        task4.run()

if __name__ == "__main__":

    Task4.main()


