import requests
import pandas as pd
import time


def get_match_events(contest_code):

    url = "https://data.ijf.org/api/get_json"

    params = {
        "params[action]": "contest.find",
        "params[contest_code]": contest_code,
        "params[part]": "events"
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data["contests"][0]["events"]


def parse_events(contest_code, events):

    rows = []

    for event in events:

        for tag in event.get("tags", []):

            rows.append({
                "contest_code": contest_code,
                "time": event["time_real"],
                "technique": tag["name"],
                "score_type": tag["group_name"]
            })

    return rows


events = get_match_events(
    "gp_chn2026_0001_m_0066_0067"
)

rows = parse_events(
    "gp_chn2026_0001_m_0066_0067",
    events
)

df = pd.DataFrame(rows)

print(df)