import requests
import pandas as pd

def get_data():
    # FEMA NFIP Claims endpoint
    url = 'https://www.fema.gov/api/open/v2/FimaNfipClaims'

    # Fetch the data from FEMA
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Normalize the JSON data to a pandas DataFrame
        df = pd.json_normalize(data['FimaNfipClaims'])
        return df
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return None
    
if __name__ == "__main__":
    df = get_data()
    print(df)