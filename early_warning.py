from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

PROMPT = """You are an assistant that warns a team lead about delivery risks.
Read the team snapshot below and answer in exactly this format:

risk_level: low | medium | high
reason: one or two sentences, using only facts from the snapshot
suggested_action: one concrete next step

Describe situations, never blame individual people.

Team snapshot:
{snapshot}
"""


def get_warning(snapshot: str) -> str:
    client = genai.Client()
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
