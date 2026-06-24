import requests
import os
from dotenv import load_dotenv



load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

print("OPEN_ROUTER_API_KEY exists:", bool(os.getenv("OPEN_ROUTER_API_KEY")))

URL = "https://openrouter.ai/api/v1/chat/completions"


def build_prompt(query: str) -> str:
    return f"""
You are an expert AI Travel Planner.

Destination Request:
{query}

Generate:
1. Destination Overview
2. Best Time To Visit
3. Day Wise Itinerary
4. Budget Breakdown
5. Local Transport
6. Famous Foods
7. Tourist Attractions
8. Travel Tips
9. Safety Tips
10. Packing Suggestions
"""


def get_travel_plan(query: str):

    if not OPEN_ROUTER_API_KEY:
        return "❌ OPEN_ROUTER_API_KEY missing in .env"

    try:
        response = requests.post(
            URL,
            headers={
                "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat-v3-0324",
                "messages": [
                    {"role": "user", "content": build_prompt(query)}
                ]
            },
            timeout=60
        )

        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Error: {str(e)}"