import threading
from ConcurrencyControl import ConcurrencyControl


class Task4:
    def __init__(self, inventory_operations):
        self.inventory_operations = inventory_operations

    def run(self):
        # Fetch original quantities
        original_quantities = self.inventory_operations.fetch_original_quantities()

        # Create and start threads
        thread1 = threading.Thread(target=self.inventory_operations.reduce_inventory_quantity)
        thread2 = threading.Thread(target=self.inventory_operations.reduce_inventory_quantity)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        # Verify the quantities after thread execution
        self.inventory_operations.verify_quantities(original_quantities)

    @staticmethod
    def main():
        connection_string = "your_connection_string"  # Replace with your actual connection string
        inventory_operations = ConcurrencyControl(connection_string)
        task4 = Task4(inventory_operations)
        task4.run()

if __name__ == "__main__":
    
    Task4.main()


