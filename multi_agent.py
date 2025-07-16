# from crewai import Agent, Task, Crew
# from crewai.tools import tool  # ✅ This is the correct tool decorator
# from langchain_openai import OpenAI
# from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Setup LLM
# llm = OpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
# search = TavilySearchAPIWrapper()

# # ✅ Correct tool definition using @tool
# @tool
# def web_search_tool(query: str) -> str:
#     """Searches the web for information using Tavily.
    
#     Args:
#         query: The search query string to look up information about.
#     """
#     try:
#         results = search.results(query)
#         return str(results)
#     except Exception as e:
#         return f"Search failed: {str(e)}"

# # Define the Researcher Agent
# researcher = Agent(
#     role="Researcher",
#     goal="Collect facts and recent insights from the web about a given topic.",
#     backstory="You're a professional researcher specialized in fast online investigation.",
#     tools=[web_search_tool],
#     verbose=True,
#     llm=llm
# )

# # Define the Writer Agent
# writer = Agent(
#     role="Writer",
#     goal="Write a clear, concise, and informative summary report based on research findings.",
#     backstory="You're a skilled writer who turns raw research into compelling reports.",
#     verbose=True,
#     llm=llm
# )

# # Loop for user input
# print("📘 Multi-Agent Research System")
# print("Type a topic to research and summarize, or type 'exit' to quit.\n")

# while True:
#     user_topic = input("🔍 Enter a topic: ")

#     if user_topic.strip().lower() in ["exit", "quit"]:
#         print("👋 Exiting. Goodbye!")
#         break

#     # ✅ Added expected_output field to both tasks
#     task1 = Task(
#         description=f"Research the topic: '{user_topic}'. Return key facts and recent developments.",
#         agent=researcher,
#         expected_output="A comprehensive list of key facts, statistics, recent developments, and relevant information about the researched topic."
#     )

#     task2 = Task(
#         description="Using the researcher's notes, write a 300-word educational summary for a general audience.",
#         agent=writer,
#         expected_output="A well-structured 300-word educational summary that presents the research findings in an accessible format for a general audience."
#     )

#     crew = Crew(
#         agents=[researcher, writer],
#         tasks=[task1, task2],
#         verbose=True
#     )

#     try:
#         result = crew.kickoff()  # ✅ Changed from crew.run() to crew.kickoff()
#         print("\n✅ Final Report:\n", result, "\n")
#     except Exception as e:
#         print(f"❌ Error occurred: {e}")
#         print("Please check your API keys and try again.\n")

#...............................................>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from crewai import Agent, Task, Crew
from crewai.tools import tool
from langchain_openai import ChatOpenAI  # Changed from OpenAI to ChatOpenAI
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify API keys are loaded
openai_key = os.getenv("OPENAI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

if not openai_key:
    print("❌ OPENAI_API_KEY not found in environment variables!")
    exit(1)

if not tavily_key:
    print("❌ TAVILY_API_KEY not found in environment variables!")
    exit(1)

print("✅ API keys loaded successfully")

# Setup LLM with better configuration
try:
    llm = ChatOpenAI(
        # model="gpt-3.5-turbo",  # Specify model explicitly
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=openai_key,
        max_retries=1
    )
    print("✅ LLM initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize LLM: {e}")
    exit(1)

# Setup search with API key
try:
    search = TavilySearchAPIWrapper(tavily_api_key=tavily_key)
    print("✅ Search tool initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize search tool: {e}")
    exit(1)

# Tool definition with better error handling
@tool
def web_search_tool(query: str) -> str:
    """Searches the web for information using Tavily.
    
    Args:
        query: The search query string to look up information about.
    
    Returns:
        str: Search results as a formatted string.
    """
    try:
        print(f"🔍 Searching for: {query}")
        results = search.results(query)
        
        # Format results for better readability
        if isinstance(results, list) and results:
            formatted_results = []
            for i, result in enumerate(results[:5]):  # Limit to top 5 results
                if isinstance(result, dict):
                    title = result.get('title', 'No title')
                    content = result.get('content', result.get('snippet', 'No content'))
                    url = result.get('url', 'No URL')
                    formatted_results.append(f"{i+1}. {title}\n   {content}\n   Source: {url}\n")
                else:
                    formatted_results.append(f"{i+1}. {str(result)}\n")
            
            return "\n".join(formatted_results)
        else:
            return f"Search completed but no results found for: {query}"
            
    except Exception as e:
        error_msg = f"Search failed for query '{query}': {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

# Define agents with simplified configuration
researcher = Agent(
    role="Web Researcher",
    goal="Search the web and gather comprehensive information about the given topic",
    backstory="You are an expert researcher who knows how to find and summarize relevant information from web searches.",
    tools=[web_search_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False
)

writer = Agent(
    role="Content Writer",
    goal="Create clear and informative summaries based on research findings",
    backstory="You are a skilled writer who excels at turning research data into readable, engaging content for general audiences.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

# Main execution loop
print("\n📘 Multi-Agent Research System")
print("Type a topic to research and summarize, or type 'exit' to quit.\n")

while True:
    user_topic = input("🔍 Enter a topic: ").strip()

    if user_topic.lower() in ["exit", "quit", ""]:
        print("👋 Exiting. Goodbye!")
        break

    print(f"\n🚀 Starting research on: {user_topic}")
    
    try:
        # Create tasks
        research_task = Task(
            description=f"""
            Search the web for comprehensive information about '{user_topic}'.
            Focus on:
            - Key definitions and concepts
            - Recent developments and trends
            - Important applications or use cases
            - Current market status or adoption
            - Expert opinions or notable quotes
            
            Provide detailed findings with sources.
            """,
            agent=researcher,
            expected_output="A comprehensive research report with key facts, recent developments, and sourced information about the topic."
        )

        writing_task = Task(
            description=f"""
            Based on the research findings, write a clear 300-word educational summary about '{user_topic}'.
            
            Structure the summary as follows:
            1. Brief introduction explaining what the topic is
            2. Key points and recent developments
            3. Applications or significance
            4. Conclusion with future outlook
            
            Write for a general audience using clear, accessible language.
            """,
            agent=writer,
            expected_output="A well-structured 300-word educational summary that presents the research findings in an accessible format for a general audience."
        )

        # Create and run crew
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            verbose=True,
            process="sequential"  # Ensure tasks run in order
        )

        # Execute the crew
        result = crew.kickoff()
        
        print("\n" + "="*80)
        print("✅ FINAL REPORT")
        print("="*80)
        print(result)
        print("="*80 + "\n")

    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        print("Please check your API keys and internet connection.\n")
        
        # Additional debugging info
        if "rate limit" in str(e).lower():
            print("💡 Tip: You may have hit API rate limits. Wait a moment and try again.")
        elif "auth" in str(e).lower() or "key" in str(e).lower():
            print("💡 Tip: Check that your API keys are correct and have sufficient credits.")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            print("💡 Tip: Check your internet connection.")
        
        continue

