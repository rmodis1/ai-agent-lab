#!/usr/bin/env python3
"""Application entrypoint.

This script initializes environment variables via python-dotenv and
provides a simple `main()` function as the program entrypoint.
"""

from dotenv import load_dotenv
import os


def main() -> None:
    """Main entrypoint for the application.

    Loads environment variables from a `.env` file (if present) and
    prints a startup message.
    """
    load_dotenv()
    app_name = os.getenv("APP_NAME", "LangChain Agent")
    print(f"🚀 Starting {app_name}...")


if __name__ == "__main__":
    main()
