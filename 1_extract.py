#import libraries
import json
import requests

url = "https://api.restful-api.dev/objects" #targetting the endpoint

try:  #Downloading the data
    response = requests.get(url, timeout = 10)   
    response.raise_for_status()
    data = response.json() 
     
     # saving the data
    with open("time_series_raw.json", "w") as file:  
        json.dump(data, file, indent =4)

    print("Extraction completed. `time_series_raw.json` created ")   

except requests.exceptions.RequestException as e:
    print(f"Extraction failed due to a network or HTTP error: {e}")
except json.JSONDecodeError:
    print("Extraction failed: The server responded, but the data was not valid JSON.")
except IOError as e:
    print(f"Extraction failed due to a file writing error: {e}")


    