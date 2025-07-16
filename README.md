# Multi-Agent Research & Summarization System

A simple, sequential “crew” of AI agents that (1) searches the web via Tavily and (2) writes clear, 300-word summaries—built with CrewAI, LangChain, and OpenAI.

## 🚀 Features

- **Automatic API-driven Research**  
  Uses TavilySearchAPIWrapper to fetch top-results for any user-supplied topic.  
- **Two Specialized Agents**  
  1. **Web Researcher** – gathers key definitions, recent developments, expert opinions.  
  2. **Content Writer** – crafts a well-structured, 300-word educational summary.  
- **Crew Workflow**  
  Tasks run sequentially: research → write → deliver final report in your terminal.

## 📦 Prerequisites

- Python 3.10+  
- Valid API keys for:
  - **OpenAI** (for ChatOpenAI LLM)  
  - **Tavily** (for web search)  

## 🔧 Installation

1. **Clone this repository**  
   git clone <your-repo-url>
   cd <repo-folder>

2. **Install dependencies**
- pip install -r requirements.txt

3. **Configure your API keys**
- Create a .env file in the root directory:
- OPENAI_API_KEY=sk-…
- TAVILY_API_KEY=tv-…


**▶️ Usage**
- python multi_agent.py

- You'll see:
📘 Multi-Agent Research System
🔍 Enter a topic: climate change
🚀 Starting research on: climate change
...
✅ FINAL REPORT
[300-word summary here]

Type exit, quit or press Enter on an empty line to stop.


