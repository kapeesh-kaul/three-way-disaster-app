import requests
import pandas as pd

# FEMA NFIP Claims endpoint
url = 'https://www.fema.gov/api/open/v2/FimaNfipClaims'

# Fetch the data from FEMA
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Normalize the JSON data to a pandas DataFrame
    df = pd.json_normalize(data['FimaNfipClaims'])
    print(df.head())
else:
    print(f"Failed to retrieve data, status code: {response.status_code}")

