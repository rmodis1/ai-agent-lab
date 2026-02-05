#!/usr/bin/env python3
"""Application entrypoint.

This script initializes environment variables via python-dotenv and
provides a simple `main()` function as the program entrypoint.
"""

from datetime import datetime
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import os


def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result.

    Uses Python's eval() for demonstration purposes only.
    WARNING: eval() is unsafe with untrusted input — do not use in production.

    Args:
        expression: A string containing a mathematical expression (e.g., "25 * 4 + 10").

    Returns:
        The result as a string, or an error message if evaluation fails.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def get_current_time(input: str) -> str:
    """Return the current date and time as a formatted string.

    Args:
        input: Not used — required by the Tool interface.

    Returns:
        The current date and time in YYYY-MM-DD HH:MM:SS format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def reverse_string(text: str) -> str:
    """Reverse the given string.

    Args:
        text: The string to reverse.

    Returns:
        The input string reversed.
    """
    return text[::-1]


def main() -> None:
    """Main entrypoint for the application.

    Loads environment variables from a `.env` file (if present) and
    prints a startup message.
    """
    load_dotenv()
    app_name = os.getenv("APP_NAME", "LangChain Agent")
    print(f"🚀 Starting {app_name}...")

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ Error: GITHUB_TOKEN not found in environment variables.")
        print("💡 To fix this:")
        print("   1. Create a .env file in the project root")
        print("   2. Add your token: GITHUB_TOKEN=your_token_here")
        print("   3. Generate a token at https://github.com/settings/tokens")
        return

    print("✅ GITHUB_TOKEN loaded successfully.")

    llm = ChatOpenAI(
        model="openai/gpt-4o",
        temperature=0,
        base_url="https://models.github.ai/inference",
        api_key=github_token,
    )

    print("🤖 ChatOpenAI model initialized.")

    tools = [
        # Tool(
        #     name="Calculator",
        #     func=calculator,
        #     description="Use this tool to evaluate mathematical expressions. "
        #     "Pass a valid math expression as a string (e.g., '25 * 4 + 10'). "
        #     "Returns the computed result. Use this whenever the user asks a math question.",
        # ),
        # Tool(
        #     name="get_current_time",
        #     func=get_current_time,
        #     description="Use this tool to get the current date and time. "
        #     "Use this whenever the user asks what time or date it is.",
        # ),
    ]

    print(f"🛠️ Tools registered: {[t.name for t in tools]}")

    # Create agent with tools
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use your tools to answer questions. "
         "Always respond in plain text — never use LaTeX or markdown formatting."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    print("🤖 Agent created successfully.")

    # Test query — agent has no tools, so it will attempt this on its own
    query = "Reverse the string 'Hello World'"
    print(f"\n🧪 Sending test query: {query}")

    try:
        result = agent_executor.invoke({"input": query})
        print(f"\n💬 Result: {result['output']}")
    except Exception as e:
        print(f"\n❌ Error running agent: {e}")


if __name__ == "__main__":
    main()
