import pandas as pd
import sqlite3

#reading time_series_clean.csv to memory
df= pd.read_csv("time_series_clean.csv")

#Establishing a connection to time_series_warehouse.db
conn = sqlite3.connect("time_series_warehouse.db")
cursor = conn.cursor()

#enforcing a primary key to 'id'
cursor.execute("""
       create table if not exists new_tracking_logs (
id TEXT PRIMARY KEY,
 name TEXT,
 "data.color" TEXT,
 "data.capacity" TEXT,
 data TEXT,
 "data.capacity gb" TEXT,
 "data.price" TEXT,
 "data.generation" TEXT,
 "data.year" TEXT,
 "data.cpu model" TEXT,
 "data.hard disk size" TEXT,
 "data.strap colour" TEXT,
 "data.case size" TEXT,
 "data.description" TEXT,
 "data.screen size" TEXT,
 "processed_at" TEXT );
 """)


#using 'INSERT OR IGNORE to create a loop
try:
    df.to_sql("new_tracking_logs", con=conn, if_exists = "append", index = False)
    conn.commit()

except sqlite3.IntegrityError:
    print("Status: Duplicate tracking log detected. Ingestion safely skipped for existing records")

#verifying audit query
validated_df = pd.read_sql_query("SELECT * FROM new_tracking_logs LIMIT 5;", conn)

print("\n .....Validated Logs.....")
print(validated_df)

#closing datebase connection
conn.close()
print("\n Databased successfully closed")