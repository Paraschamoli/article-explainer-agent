# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""Article Explainer Agent - A Bindu AI Agent for Article Analysis."""

import argparse
import asyncio
import json
import logging
import os
import sys
import traceback
from pathlib import Path
from typing import Any, cast

from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from .agents import run_article_explanation

# Load environment variables from .env file
load_dotenv()

# Global agent instance
agent: Any = None
_initialized = False
_init_lock = asyncio.Lock()

# Setup logging
_logger = logging.getLogger(__name__)


def load_config() -> dict[str, Any]:
    """Load agent config from `agent_config.json` or return defaults."""
    config_path = Path(__file__).parent / "agent_config.json"

    if config_path.exists():
        try:
            with open(config_path) as f:
                return cast(dict[str, Any], json.load(f))
        except (OSError, json.JSONDecodeError) as exc:
            _logger.warning("Failed to load config from %s", config_path, exc_info=exc)

    return {
        "name": "article-explainer-agent",
        "description": "AI-powered multi-specialist article explainer assistant",
        "deployment": {
            "url": "http://127.0.0.1:3774",
            "expose": True,
            "protocol_version": "1.0.0",
        },
    }


class ArticleExplainerAgent:
    """Article Explainer Agent wrapper following the medical-diagnostics-agent pattern."""

    def __init__(self, model_name: str = "gpt-4o"):
        """Initialize article explainer agent with model name."""
        self.model_name = model_name

        # Model selection logic (only supports OpenRouter)
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        if openrouter_api_key:
            # Use OpenRouter API key with OpenAI client
            self.model = ChatOpenAI(  # type: ignore[call-arg]
                model_name=model_name,
                openai_api_key=SecretStr(openrouter_api_key),
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0,
            )
            print(f"✅ Using OpenRouter model: {model_name}")
        else:
            # Define error message separately to avoid TRY003
            error_msg = (
                "No API key provided. Set OPENROUTER_API_KEY environment variable.\n"
                "For OpenRouter: https://openrouter.ai/keys"
            )
            raise ValueError(error_msg)

    async def arun(self, messages: list[dict[str, str]]) -> str:
        """Run the agent with the given messages - matches medical-diagnostics-agent pattern."""
        # Extract article content from messages
        article_content = ""
        for message in messages:
            if message.get("role") == "user":
                article_content = message.get("content", "")
                break

        if not article_content:
            return "Error: No article content provided in the user message."

        try:
            # Run the article explanation pipeline (async)
            final_explanation = await run_article_explanation(article_content, self.model_name)

            # Format the response
            response = f"""### Article Analysis:

{final_explanation}

---
*Analysis performed by AI Article Explainer Agent*
*Specialist inputs: Developer, Summarizer, Explainer, Analogy Creator, Vulnerability Expert*
*Model: {self.model_name}*
"""

        except Exception as e:
            error_msg = f"Error during article explanation: {e!s}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            return error_msg
        else:
            return response


async def initialize_agent() -> None:
    """Initialize article explainer agent with proper model."""
    global agent

    # Get API key from environment (only supports OpenRouter)
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")

    # Model selection logic (only OpenRouter)
    if openrouter_api_key:
        agent = ArticleExplainerAgent(model_name)
        print(f"✅ Using OpenRouter model: {model_name}")
    else:
        # Define error message separately to avoid TRY003
        error_msg = (
            "No API key provided. Set OPENROUTER_API_KEY environment variable.\n"
            "For OpenRouter: https://openrouter.ai/keys"
        )
        raise ValueError(error_msg)

    print("✅ Article Explainer Agent initialized")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages - matches medical-diagnostics-agent pattern."""
    global agent
    if not agent:
        # Define error message separately to avoid TRY003
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    # Run the agent and get response - matches medical-diagnostics-agent pattern
    return await agent.arun(messages)


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization - matches medical-diagnostics-agent pattern."""
    global _initialized

    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Article Explainer Agent...")
            await initialize_agent()
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Article Explainer Agent resources...")


def main() -> None:
    """Run the main entry point for the Article Explainer Agent."""
    parser = argparse.ArgumentParser(description="Bindu Article Explainer Agent")
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "gpt-4o"),
        help="Model name to use (env: MODEL_NAME, default: gpt-4o)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to agent_config.json (optional)",
    )
    args = parser.parse_args()

    # Set environment variables if provided via CLI
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model

    print("🤖 Article Explainer Agent - AI Multi-Specialist Article Analysis")
    print("📚 Capabilities: Code examples, summaries, explanations, analogies, critical analysis")
    print("👥 Specialist Team: Developer, Summarizer, Explainer, Analogy Creator, Vulnerability Expert")

    # Load configuration
    config = load_config()

    try:
        # Bindufy and start the agent server
        print("🚀 Starting Bindu Article Explainer Agent server...")
        print(f"🌐 Server will run on: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Article Explainer Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup on exit
        asyncio.run(cleanup())


# Bindufy and start the agent server
if __name__ == "__main__":
    main()
