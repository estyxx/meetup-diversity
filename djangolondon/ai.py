import openai
from openai import OpenAI
from djangolondon.env import Env
import re


def extract_speakers(env: Env, description: str) -> list[str]:
    client = OpenAI(api_key=env.OPENAI_API_KEY)
    prompt = (
        f"Extract all speaker names from the following event description and "
        f"clean them of any extraneous punctuation or symbols. List each name separately: {description}"
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
    names = speakers.split("\n")
    print(names)
    return names


# def clean_speaker_names(speakers):
#     cleaned_names = []
#     for name in speakers:
#         # Remove common prefixes and symbols
#         name = re.sub(r"^[-\s]*Speaker names:\s*", "", name, flags=re.IGNORECASE)
#         name = re.sub(r"^[-\s]*Speaker:\s*", "", name, flags=re.IGNORECASE)
#         name = re.sub(r"^-[\s]*", "", name)  # Remove leading dashes and spaces
#         name = re.sub(r"\n", "", name)  # Remove newlines within names
#         name = re.sub(
#             r"strawberry|wagtail|django-stubs", "", name, flags=re.IGNORECASE
#         )  # Remove specific unwanted words
#         name = name.strip()  # Trim whitespace from both ends of the name string
#         if name:  # Ensure the name is not empty after cleaning
#             cleaned_names.append(name)
#     return cleaned_names


def clean_speaker_names(speakers):
    # Remove common prefixes and symbols
    speakers = re.sub(r"^[-\s]*Speaker names:\s*", "", speakers, flags=re.IGNORECASE)
    speakers = re.sub(r"^[-\s]*Speaker:\s*", "", speakers, flags=re.IGNORECASE)
    speakers = re.sub(r"^-[\s]*", "", speakers)  # Remove leading dashes and spaces
    speakers = re.sub(
        r"\n", " ", speakers
    )  # Replace newlines with spaces to prevent word merging
    speakers = re.sub(
        r"strawberry|wagtail|django-stubs|djangoproject\.com",
        "",
        speakers,
        flags=re.IGNORECASE,
    )  # Remove specific unwanted words
    # Clean up quotation marks and any trailing punctuation like commas, periods, or hyphens
    speakers = re.sub(r'[",\.\-]+$', "", speakers.strip())
    # Further strip any extraneous whitespace created by previous replacements
    speakers = re.sub(r"\s+", " ", speakers).strip()

    return speakers


def extract_gender(env: Env, name: str) -> str:
    client = OpenAI(api_key=env.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Based on traditional associations and not implying identity, would the name '{name}' be more commonly associated with a male or female?",
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


def parse_gender_simple(text):
    lower_text = text.lower()
    if "female" in lower_text:
        return "female"
    elif "male" in lower_text:
        return "male"
    return "unspecified"
