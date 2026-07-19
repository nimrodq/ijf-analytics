import requests
import pandas as pd

url = "https://data.ijf.org/api/get_json"

params = {
    "params[action]": "contest.find",
    "params[id_competition]": "3204",
    "params[order_by]": "cnum"
}

response = requests.get(url, params=params)

print(response.status_code)

data = response.json()

print(data.keys())

df = pd.json_normalize(data["contests"])

print(df.head())
print(df.columns)