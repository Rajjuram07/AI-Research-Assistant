from google import genai
from backend.config import GEMINI_API_KEY

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------- SUMMARY ---------------- #

def summarize_text(text):

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
            You are an AI Research Assistant.

            Generate a professional summary of this document.

            Document:
            {text[:12000]}
            """
        )

        return response.text

    except Exception as e:

        return f"Summary generation failed: {str(e)}"


# ---------------- INSIGHTS ---------------- #

def generate_insights(text):

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
            You are an AI Research Assistant.

            Extract key insights from this document.

            Include:
            - Main findings
            - Technologies discussed
            - Challenges
            - Business impact
            - Recommendations

            Document:
            {text[:12000]}
            """
        )

        return response.text

    except Exception as e:

        return f"Insights generation failed: {str(e)}"