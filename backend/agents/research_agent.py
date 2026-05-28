import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")

def research_answer(query, context):

    prompt = f"""
    Answer the question based on context.

    Context:
    {context}

    Question:
    {query}
    """

    response = model.generate_content(prompt)

    return response.text