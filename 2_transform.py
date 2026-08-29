import json
import pandas as pd
import datetime 

#reading .json file into memory
with open("time_series_raw.json", "r") as file:
    raw_json = json.load(file)

#loading the .json file into a dataframe
df = pd.json_normalize(raw_json)

#creating a new column 'processed_at' and making sure the time stamp is in ISO - 8601 standard
df['processed_at'] = datetime.datetime.now()
df['processed_at'] = pd.to_datetime(df['processed_at'])
df['processed_at'] = df['processed_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

#standardizes headers to lowercase and drop any  duplicate column and  missing data in id column 
df.columns= df.columns.str.lower()
df =df.loc[:,~df.columns.duplicated()]
df = df.dropna(subset =['id'])



#storing as csv
df.to_csv("time_series_clean.csv", index = False)
print("time_series_clean.csv - successfully created")
