from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

PROMPT = """You are an assistant that warns a team lead about delivery risks.
Read the team snapshot below and answer in exactly this format:

risk_level: low | medium | high
reason: one or two sentences, using only facts from the snapshot
suggested_action: one concrete next step

How to choose risk_level:
- high: the sprint goal is likely to be missed unless someone acts now
  (for example: work is blocked, or most work shows no progress, close to the end)
- medium: a warning sign that could become a problem if ignored,
  but nothing is blocked yet (for example: work concentrated on one person)
- low: work is progressing normally and no blockers are mentioned

Describe situations, never blame individual people.
Do not add facts or interpretations that are not in the snapshot.

Team snapshot:
{snapshot}
"""


def get_warning(snapshot: str) -> str:
    client = genai.Client(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(attempts=6, initial_delay=2.0)
        )
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(snapshot=snapshot),
    )
    return response.text


if __name__ == "__main__":
    example = (
        "Sprint ends in 2 days. 3 of 5 tickets are still 'In Progress'. "
        "Ana wrote 'waiting on API access' in her last 3 standups."
    )
    print(get_warning(example))
