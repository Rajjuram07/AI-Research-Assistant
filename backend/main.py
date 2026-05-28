from fastapi import FastAPI, UploadFile

from backend.services.pdf_service import extract_text
from backend.rag_pipeline import store_document
from backend.graph_workflow import run_workflow

from backend.agents.summary_agent import (
    summarize_text,
    generate_insights
)

app = FastAPI()

# Global storage
DOCUMENT_TEXT = ""


@app.get("/")
def home():

    return {
        "message": "AI Research Assistant Running"
    }


# ---------------- UPLOAD ---------------- #

@app.post("/upload")
async def upload_pdf(file: UploadFile):

    global DOCUMENT_TEXT

    try:

        contents = await file.read()

        with open("temp.pdf", "wb") as f:
            f.write(contents)

        text = extract_text("temp.pdf")

        DOCUMENT_TEXT = text

        store_document(text)

        return {
            "message": "Document uploaded successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ---------------- Q&A ---------------- #

@app.get("/ask")
def ask_question(query: str):

    try:

        answer = run_workflow(query)

        return {
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ---------------- SUMMARY ---------------- #

@app.get("/summary")
def get_summary():

    global DOCUMENT_TEXT

    try:

        if DOCUMENT_TEXT == "":

            return {
                "error": "No document uploaded"
            }

        summary = summarize_text(DOCUMENT_TEXT)

        return {
            "summary": summary
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ---------------- INSIGHTS ---------------- #

@app.get("/insights")
def get_insights():

    global DOCUMENT_TEXT

    try:

        if DOCUMENT_TEXT == "":

            return {
                "error": "No document uploaded"
            }

        insights = generate_insights(DOCUMENT_TEXT)

        return {
            "insights": insights
        }

    except Exception as e:

        return {
            "error": str(e)
        }