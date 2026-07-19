import requests
import pandas as pd
import time


BASE_URL = "https://data.ijf.org/api/get_json"

COMPETITION_ID = "3204"   # Qingdao Grand Prix 2026


def get_contests(competition_id):
    """
    Get all contests from a competition
    """

    params = {
        "params[action]": "contest.find",
        "params[id_competition]": competition_id,
        "params[order_by]": "cnum"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    return data["contests"]



def get_events(contest_code):
    """
    Get event-level data for one contest
    """

    params = {
        "params[action]": "contest.find",
        "params[contest_code]": contest_code,
        "params[part]": "events"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    return data["contests"][0]["events"]



def extract_techniques(contest, events):
    """
    Convert nested event JSON into rows
    """

    rows = []

    for event in events:

        for tag in event.get("tags", []):

            rows.append({

                "competition":
                    contest.get("competition_name"),

                "date":
                    contest.get("competition_date"),

                "weight":
                    contest.get("weight"),

                "contest_code":
                    contest.get("contest_code_long"),

                "winner":
                    contest.get(
                        "person_white"
                        if contest.get("id_winner")
                        == contest.get("id_person_white")
                        else "person_blue"
                    ),

                "white":
                    contest.get("person_white"),

                "blue":
                    contest.get("person_blue"),

                "country_white":
                    contest.get("country_white"),

                "country_blue":
                    contest.get("country_blue"),

                "time_seconds":
                    event.get("time_real"),

                "technique":
                    tag.get("name"),

                "score_type":
                    tag.get("group_name"),

                "tag_group":
                    tag.get("id_group")
            })

    return rows



def clean_techniques(df):
    """
    Remove penalties and non-technique events
    """

    remove_events = [
        "Non-Combativity",
        "False-Attack",
        "Avoid-Grip",
        "Right",
        "Left",
        "Shido"
    ]

    df = df[
        ~df["technique"].isin(remove_events)
    ]

    return df



def main():

    print("Downloading contests...")

    contests = get_contests(COMPETITION_ID)

    print(
        f"Found {len(contests)} contests"
    )


    all_rows = []


    for i, contest in enumerate(contests):

        code = contest.get(
            "contest_code_long"
        )

        print(
            f"{i+1}/{len(contests)} {code}"
        )


        try:

            events = get_events(code)

            rows = extract_techniques(
                contest,
                events
            )

            all_rows.extend(rows)


        except Exception as e:

            print(
                "Failed:",
                code,
                e
            )


        # avoid hammering API
        time.sleep(0.2)



    df = pd.DataFrame(all_rows)


    print(
        "\nRaw events:",
        len(df)
    )


    df = clean_techniques(df)


    print(
        "Clean techniques:",
        len(df)
    )


    print(
        df.head()
    )


    df.to_csv(
        "data/processed/judo_techniques.csv",
        index=False
    )


    print(
        "\nSaved data/judo_techniques.csv"
    )



if __name__ == "__main__":
    main()