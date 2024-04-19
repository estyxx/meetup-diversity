from djangolondon.env import Env
from djangolondon.meetup import authorize
from djangolondon.meetup import graphql_query

from pathlib import Path
from djangolondon.data_saver import save_to_excel, save_to_json
from djangolondon.ai import extract_speakers, extract_gender
import pandas as pd


def main():
    env = Env.get_env()
    print(env)

    authorize(env)
    query = Path("query.graphql").read_text()

    # Making the GraphQL query call
    result = graphql_query(query)
    edges = result["data"]["groupByUrlname"]["pastEvents"]["edges"]

    names = {}
    events_list = []
    for edge in edges:
        event = edge["node"]
        description = event["description"].split(" a talk ")[0]
        date_time = (
            pd.to_datetime(event["dateTime"], utc=True).date().strftime("%d/%m/%Y")
        )

        speakers = extract_speakers(env, description)
        for speaker in speakers:
            if speaker not in names:
                gender = extract_gender(env, speaker)
                names[speaker] = gender

            event_info = {
                "ID": event["id"],
                "Date Time": date_time,
                "Title": event["title"],
                "Event URL": event["eventUrl"],
                "Description": description,
                "Host Name": event["host"]["name"] if event["host"] else "",
                "Venue Name": event["venue"]["name"] if "venue" in event else "Online",
                "Is Online": event["isOnline"],
                "Hosts": ", ".join([host["name"] for host in event["hosts"]]),
                "Speaker": speaker,
                "Speaker Gender": names[speaker],
            }
            print(f"writing: {speaker}")
            events_list.append(event_info)

    # Save to Excel and JSON
    save_to_excel(events_list)
    save_to_json([edge["node"] for edge in edges])

    print(f"Processed and saved {len(events_list)} events.")


if __name__ == "__main__":
    main()