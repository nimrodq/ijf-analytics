import requests
import json

url = "https://data.ijf.org/api/get_json"

params = {
    "params[action]": "contest.find",
    "params[contest_code]": "gp_chn2026_0001_m_0066_0067",
    "params[part]": "info,score_list,media,events"
}

response = requests.get(url, params=params)

print(response.status_code)

data = response.json()

print(json.dumps(data, indent=2)[:5000])