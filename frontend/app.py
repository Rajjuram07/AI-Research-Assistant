import streamlit as st
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

# ---------------- TITLE ---------------- #

st.title("📚 AI Research Assistant")

st.markdown(
    "### Multi-Agent RAG System using Gemini + Pinecone + LangGraph"
)

# ---------------- METRICS ---------------- #

col1, col2, col3 = st.columns(3)

col1.metric("LLM", "Gemini 3.5 Flash")
col2.metric("Vector DB", "Pinecone")
col3.metric("Framework", "LangGraph")

st.divider()

# ---------------- FILE UPLOAD ---------------- #

st.subheader("📄 Upload Research Document")

uploaded_file = st.file_uploader(
    "Upload PDF File",
    type=["pdf"]
)

# Upload button
if uploaded_file and not st.session_state.document_uploaded:

    if st.button("Upload Document"):

        files = {
            "file": uploaded_file
        }

        with st.spinner("Uploading and processing document..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/upload",
                    files=files
                )

                data = response.json()

                if "message" in data:

                    st.session_state.document_uploaded = True

                elif "error" in data:

                    st.error(data["error"])

                else:

                    st.error("Upload failed")

            except Exception as e:

                st.error(f"Error: {e}")

# Show upload status
if st.session_state.document_uploaded:

    st.success("Document uploaded successfully")

st.divider()

# ---------------- TABS ---------------- #

tab1, tab2, tab3 = st.tabs(
    ["💬 Q&A", "📄 Summary", "📊 Insights"]
)

# ================= TAB 1 ================= #

with tab1:

    st.subheader("🤖 Ask Questions About Your Document")

    st.markdown("### 💡 Suggested Questions")

    st.markdown("""
    - What is this document about?
    - Summarize the document
    - What are the key findings?
    - What technologies are discussed?
    - What are the challenges mentioned?
    """)

    query = st.text_input(
        "Enter your question"
    )

    if st.button("Ask AI"):

        if not st.session_state.document_uploaded:

            st.warning("Please upload a document first.")

        elif not query.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating AI response..."):

                try:

                    response = requests.get(
                        "http://127.0.0.1:8000/ask",
                        params={"query": query}
                    )

                    data = response.json()

                    if "answer" in data:

                        st.markdown("## 📌 AI Response")

                        st.write(data["answer"])

                        st.session_state.chat_history.append(
                            {
                                "question": query,
                                "answer": data["answer"]
                            }
                        )

                    elif "error" in data:

                        st.error(data["error"])

                    else:

                        st.error("Question failed")

                except Exception as e:

                    st.error(f"Error: {e}")

    # Chat History
    if st.session_state.chat_history:

        st.divider()

        st.subheader("📝 Chat History")

        for chat in reversed(st.session_state.chat_history):

            st.markdown(f"### ❓ {chat['question']}")
            st.write(chat['answer'])

# ================= TAB 2 ================= #

with tab2:

    st.subheader("📄 AI Generated Summary")

    if st.button("Generate Summary"):

        if not st.session_state.document_uploaded:

            st.warning("Please upload a document first.")

        else:

            with st.spinner("Generating summary..."):

                try:

                    response = requests.get(
                        "http://127.0.0.1:8000/summary"
                    )

                    data = response.json()

                    if "summary" in data:

                        st.success("Summary Generated Successfully")

                        st.write(data["summary"])

                    elif "error" in data:

                        st.error(data["error"])

                    else:

                        st.error(data)

                except Exception as e:

                    st.error(f"Error: {e}")

# ================= TAB 3 ================= #

with tab3:

    st.subheader("📊 Research Insights")

    if st.button("Generate Insights"):

        if not st.session_state.document_uploaded:

            st.warning("Please upload a document first.")

        else:

            with st.spinner("Generating insights..."):

                try:

                    response = requests.get(
                        "http://127.0.0.1:8000/insights"
                    )

                    data = response.json()

                    if "insights" in data:

                        st.success("Insights Generated Successfully")

                        st.write(data["insights"])

                    elif "error" in data:

                        st.error(data["error"])

                    else:

                        st.error(data)

                except Exception as e:

                    st.error(f"Error: {e}")

# ---------------- FOOTER ---------------- #

st.divider()

st.markdown(
    """
    ### ⚡ Tech Stack

    - FastAPI
    - Streamlit
    - Gemini 3.5 Flash
    - Pinecone
    - LangGraph
    - Sentence Transformers
    - CrewAI
    """
)