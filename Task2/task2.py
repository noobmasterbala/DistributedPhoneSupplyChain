import os
import csv
import psycopg2
from datetime import datetime
from fragmentation import horizonatl_fragmentation, vertical_fragmentation
from replication import show_replicas

if __name__ == "__main__":
    print("HORIZONTAL FRAGMENTATION \n")
    horizonatl_fragmentation()
    print(" -------------------------------------- \n")
    print("VERTICAL FRAGMENTATION")
    vertical_fragmentation()
    print(" -------------------------------------- \n")
    print("DATABASE REPLICATION ")
    show_replicas()