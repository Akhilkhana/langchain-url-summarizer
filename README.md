# YouTube & URL Summarizer — LangChain + Groq

A Streamlit app that summarizes content from **YouTube videos** and **any webpage** in seconds, powered by a LangChain pipeline and a Groq-hosted LLaMA 3.1 model.

## Features

- **YouTube support** — paste a YouTube URL and the app extracts the video transcript automatically
- **Generic URL support** — paste any website link and the app scrapes and summarizes its text content
- **Fast inference** — uses Groq's hosted `llama-3.1-8b-instant` for near-instant summaries
- **300-word summaries** — concise, readable output regardless of content length
- **Bot-bypass headers** — spoofs a real browser User-Agent to handle sites that block scrapers
- **Input validation** — catches empty fields and malformed URLs before making any API calls

## Tech Stack

| Layer | Library |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| LLM | [Groq](https://groq.com) — `llama-3.1-8b-instant` |
| Orchestration | [LangChain](https://python.langchain.com) |
| YouTube loader | `YoutubeLoader` (langchain-community) |
| Web scraper | `UnstructuredURLLoader` (langchain-community) |
| URL validation | `validators` |

## Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com)

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/Akhilkhana/Youtube-URL-Summarization.git
cd Youtube-URL-Summarization
```

2. **Create and activate a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Usage

1. Enter your **Groq API key** in the sidebar
2. Paste a **YouTube video URL** or any **website URL** into the input field
3. Click **"Summarize the content from Youtube or URL"**
4. Read the 300-word summary in the green output box

**Supported URL formats:**
- YouTube: `https://www.youtube.com/watch?v=...`
- Websites: any valid `http://` or `https://` URL

## How It Works

1. The app validates the URL using the `validators` library
2. If the URL is a YouTube link, `YoutubeLoader` fetches the video transcript via the YouTube API
3. For all other URLs, `UnstructuredURLLoader` scrapes the page text (with SSL and User-Agent handling)
4. The loaded text is injected into a LangChain `PromptTemplate` asking for a 300-word summary
5. The prompt is passed through a chain: `PromptTemplate → ChatGroq → StrOutputParser`
6. The final summary string is displayed in the Streamlit UI

## Project Structure

```
Youtube-URL-Summarization/
├── app.py            # Main application — loader logic, LLM chain, and Streamlit UI
├── requirements.txt  # Python dependencies
└── README.md
```

## License

This project is open source. See [LICENSE](LICENSE) for details.
