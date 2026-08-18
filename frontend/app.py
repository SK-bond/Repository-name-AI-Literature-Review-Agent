import streamlit as st
import requests

st.set_page_config(
    page_title="AI Literature Review Agent",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Literature Review Agent")

st.markdown(
    "### Generate a research literature review in seconds"
)

st.write(
    "Enter a research topic and the system will search for "
    "research papers, summarize them, identify research gaps, "
    "and generate a structured literature review."
)

st.divider()

topic = st.text_input(
    "🔎 Research Topic",
    placeholder="Example: Neural Networks"
)

if st.button("🚀 Generate Literature Review", use_container_width=True):

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        with st.spinner("Searching and generating your literature review..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/review",
                    json={"topic": topic},
                    timeout=600
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("✅ Literature Review Generated!")

                    st.divider()

                    st.markdown(data["review"])

                else:

                    st.error(
                        f"Backend error: {response.status_code}"
                    )

                    st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Backend is not running. "
                    "Start FastAPI first."
                )

            except Exception as e:

                st.error(f"Error: {e}")