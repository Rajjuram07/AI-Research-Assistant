from backend.rag_pipeline import retrieve_context
from backend.agents.research_agent import research_answer

def run_workflow(query):

    context = retrieve_context(query)

    answer = research_answer(query, context)

    return answer