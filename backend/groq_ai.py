import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_insights(data):

    prompt = f"""
    Analyze student performance and placement data:

    {data}

    Provide:
    - Top performers
    - Students at risk
    - Placement readiness
    - Skill gap analysis
    - Suggestions for improvement
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
