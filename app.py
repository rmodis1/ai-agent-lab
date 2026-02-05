#!/usr/bin/env python3
"""Application entrypoint.

This script initializes environment variables via python-dotenv and
provides a simple `main()` function as the program entrypoint.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os


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

    # Test query — the LLM will answer on its own without tools
    query = "What is 25 * 4 + 10?"
    print(f"\n🧪 Sending test query: {query}")

    response = llm.invoke(query)
    print(f"💬 Response: {response.content}")


if __name__ == "__main__":
    main()
