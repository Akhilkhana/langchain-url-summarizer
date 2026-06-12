# --- Imports ---
import validators                          # URL validation library
import streamlit as st                     # Web UI framework
from langchain_core.prompts import PromptTemplate          # Template for structuring LLM prompts
from langchain_groq import ChatGroq                        # Groq-hosted LLM (fast inference)
from langchain_core.output_parsers import StrOutputParser  # Converts LLM output to plain string
from langchain_community.document_loaders import (
    YoutubeLoader,          # Loads transcript from a YouTube video URL
    UnstructuredURLLoader,  # Loads and parses text content from any webpage
)

# --- Page Configuration ---
# Sets the browser tab title and configures the Streamlit app layout
st.set_page_config(page_title="Langchain: summarize Text from Youtube or website")
st.title("Langchain: Summarize text from Youtube or website")
st.subheader("Summarize URL")

# --- Sidebar: API Key Input ---
# The Groq API key is entered in the sidebar as a password field (hidden input)
# Get your free key at: https://console.groq.com
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# --- URL Input ---
# Main input field where the user pastes a YouTube video URL or any website URL
generic_url = st.text_input("URL", label_visibility="collapsed")

# --- Prompt Template ---
# Instructs the LLM to summarize the loaded content in 300 words.
# {text} is a placeholder that gets filled with the actual page/video content at runtime.
prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# --- Summarize Button Logic ---
if st.button("Summarize the content from Youtube or URL"):

    # Validate that both inputs are filled in before proceeding
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")

    # Validate that the entered URL is a properly formatted web address
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a Youtube video or website URL")

    else:
        try:
            with st.spinner("Waiting..."):

                # --- Document Loading ---
                # Choose the appropriate loader based on the URL type:
                #   - YoutubeLoader  → extracts the video transcript via the YouTube API
                #   - UnstructuredURLLoader → scrapes and parses raw text from a webpage
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=False)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,  # Skips SSL cert check for sites with self-signed certs
                        # Spoof a real browser User-Agent to avoid bot-blocking by websites
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"},
                    )

                # Load returns a list of Document objects, each with a .page_content string
                data = loader.load()

                # --- LLM Chain Setup ---
                # Initialize the Groq LLM with a fast open-source model (Llama 3.1 8B)
                llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

                # Build a simple pipeline: prompt → LLM → plain string output
                chain = prompt | llm | StrOutputParser()

                # Combine all loaded document chunks into one string and send to the LLM
                output_summary = chain.invoke({"text": "\n\n".join(doc.page_content for doc in data)})

                # Display the generated summary in a green success box
                st.success(output_summary)

        except Exception as e:
            # Show the full exception traceback in the UI for easy debugging
            st.exception(f"Exception: {e}")
