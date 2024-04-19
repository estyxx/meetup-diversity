import openai
from openai import OpenAI

from djangolondon.env import Env


def extract_speakers(env: Env, description: str) -> list[str]:
    client = OpenAI(api_key=env.OPENAI_API_KEY)
    prompt = (
        "Please extract all the speaker names from the given event description, "
        "ensuring to clean them of any extraneous punctuation, numbers, or symbols. "
        "Only include names of individuals, and exclude any technologies "
        "(e.g., Flask, Django, Python) or software companies (e.g., JetBrains). "
        "If no companies are mentioned explicitly, leave that part blank. "
        "Present only the names separated by ', ' from the description provided: "
        f"{description}"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="gpt-3.5-turbo",
        )

        speakers = response.choices[0].message.content or ""

    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)

    # Assuming the response contains names separated by commas
    names = speakers.split(", ")
    print(names)
    return names


def extract_gender(env: Env, name: str) -> str:
    client = OpenAI(api_key=env.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Based on traditional associations and not implying identity, "
                        f"would the name '{name}' be more commonly associated with a "
                        "male or female? "
                        "Give a short answer, 'female' or 'male' or 'other'"
                    ),
                },
            ],
            model="gpt-3.5-turbo",
            max_tokens=50,
        )

        response = response.choices[0].message.content or ""
        print(name, response)
        return parse_gender_simple(response)
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)

    return ""


def parse_gender_simple(text: str) -> str:
    lower_text = text.lower()
    if "female" in lower_text:
        return "female"
    elif "male" in lower_text:
        return "male"
    return "unspecified"
