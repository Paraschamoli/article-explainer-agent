"""Article explainer agents using LangChain."""

import asyncio
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

# Error messages
NO_API_KEY_ERROR = "No API key provided. Set OPENROUTER_API_KEY environment variable."


class ArticleAgent:
    """Base class for article explainer agents."""

    def __init__(self, article_content: str, role: str, model_name: str = "gpt-4o"):
        """Initialize article agent with content, role, and model."""
        self.article_content = article_content
        self.role = role

        # Get API key from environment (only supports OpenRouter)
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        if openrouter_api_key:
            # Use OpenRouter API key with OpenAI client
            self.model = ChatOpenAI(  # type: ignore[call-arg]
                model_name=model_name,
                openai_api_key=SecretStr(openrouter_api_key),
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0,
            )
        else:
            raise ValueError(NO_API_KEY_ERROR)

        self.prompt_template = self._create_prompt_template()
        self.chain = self.prompt_template | self.model | StrOutputParser()

    def _create_prompt_template(self) -> PromptTemplate:
        """Create role-specific prompt template."""
        templates = {
            "Developer": """
                You are Developer agent.

                Goal: Provide ONLY technical implementation details, code examples, and architectural components.

                Focus EXCLUSIVELY on:
                - Technical implementation details
                - Code examples and pseudocode
                - APIs, tools, and technologies
                - Development patterns and best practices

                DO NOT provide summaries, explanations for beginners, analogies, or security analysis.

                Article Content: {article_content}
            """,
            "Summarizer": """
                You are Summarizer agent.

                Goal: Provide ONLY a concise summary with key takeaways.

                Focus EXCLUSIVELY on:
                - 5-8 bullet points maximum
                - Total length 80-120 words
                - Most important findings and conclusions
                - Quick overview for busy readers

                DO NOT provide technical details, explanations, analogies, or security analysis.

                Article Content: {article_content}
            """,
            "Explainer": """
                You are Explainer agent.

                Goal: Provide ONLY step-by-step conceptual explanations for beginners.

                Focus EXCLUSIVELY on:
                - Clear, educational explanations
                - Step-by-step breakdowns
                - Beginner-friendly language
                - Conceptual understanding (not technical implementation)

                DO NOT provide code examples, summaries, analogies, or security analysis.

                Article Content: {article_content}
            """,
            "Analogy Creator": """
                You are Analogy Creator agent.

                Goal: Provide ONLY real-world analogies and metaphors.

                Focus EXCLUSIVELY on:
                - Simple, relatable analogies
                - Real-world comparisons
                - Metaphors that make abstract concepts concrete
                - Non-technical explanations

                DO NOT provide technical details, summaries, step-by-step explanations, or security analysis.

                Article Content: {article_content}
            """,
            "Vulnerability Expert": """
                You are Vulnerability Expert agent.

                Goal: Provide ONLY security risks, vulnerabilities, and mitigation strategies.

                Focus EXCLUSIVELY on:
                - Security vulnerabilities
                - Potential risks and threats
                - Mitigation strategies
                - Security best practices

                DO NOT provide technical implementation details, summaries, explanations, or analogies.

                Article Content: {article_content}
            """,
        }

        return PromptTemplate.from_template(templates[self.role])

    async def run(self) -> str:
        """Run the agent analysis."""
        print(f"{self.role} is running...")
        try:
            response = await self.chain.ainvoke({"article_content": self.article_content})
        except Exception as e:
            print(f"Error occurred in {self.role}: {e}")
            return f"Error: {e!s}"
        else:
            return response


class MultiSpecialistTeam:
    """Agent that synthesizes reports from multiple specialists."""

    def __init__(
        self,
        developer_report: str,
        summarizer_report: str,
        explainer_report: str,
        analogy_creator_report: str,
        vulnerability_expert_report: str,
        model_name: str = "gpt-4o",
    ):
        """Initialize multi-specialist team with specialist reports."""
        self.developer_report = developer_report
        self.summarizer_report = summarizer_report
        self.explainer_report = explainer_report
        self.analogy_creator_report = analogy_creator_report
        self.vulnerability_expert_report = vulnerability_expert_report
        self.model_name = model_name

        # Create synthesis prompt template
        synthesis_template = """
            Act like a multi-specialist team of article analysis experts.
            You will receive an article analysis from a Developer, Summarizer, Explainer, Analogy Creator, and Vulnerability Expert.

            Task: Create a comprehensive, well-structured analysis that combines all perspectives WITHOUT repetition.

            Structure the output EXACTLY as follows:

            # Comprehensive Analysis of [Topic]

            ## Developer Perspective
            [Technical implementation details, code examples, APIs, tools]

            ## Summarizer Perspective
            [Concise summary, key points, TL;DR]

            ## Explainer Perspective
            [Step-by-step explanation, beginner-friendly breakdown]

            ## Analogy Creator Perspective
            [Real-world analogies, metaphors, simple comparisons]

            ## Vulnerability Expert Perspective
            [Security risks, vulnerabilities, mitigation strategies]

            ## Final Synthesis
            [Comprehensive conclusion combining all insights]

            ---
            *Analysis performed by AI Article Explainer Agent*
            *Specialist inputs: Developer, Summarizer, Explainer, Analogy Creator, Vulnerability Expert*
            *Model: gpt-4o*

            Developer Report: {developer_report}

            Summarizer Report: {summarizer_report}

            Explainer Report: {explainer_report}

            Analogy Creator Report: {analogy_creator_report}

            Vulnerability Expert Report: {vulnerability_expert_report}
        """

        # Create the model using the same pattern as specialist agents
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import PromptTemplate
        from langchain_openai import ChatOpenAI

        # Get API key from environment (only supports OpenRouter)
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        if openrouter_api_key:
            model = ChatOpenAI(  # type: ignore[call-arg]
                model_name=model_name,
                openai_api_key=SecretStr(openrouter_api_key),
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0,
            )
        else:
            raise ValueError(NO_API_KEY_ERROR)

        # Create synthesis chain
        self.chain = PromptTemplate.from_template(synthesis_template) | model | StrOutputParser()

    async def run(self) -> str:
        """Run the multi-specialist analysis."""
        print("MultiSpecialistTeam is running...")
        try:
            response = await self.chain.ainvoke({
                "developer_report": self.developer_report,
                "summarizer_report": self.summarizer_report,
                "explainer_report": self.explainer_report,
                "analogy_creator_report": self.analogy_creator_report,
                "vulnerability_expert_report": self.vulnerability_expert_report,
            })
        except Exception as e:
            print(f"Error occurred in MultiSpecialistTeam: {e}")
            return f"Error: {e!s}"
        else:
            return response


class Developer(ArticleAgent):
    """Developer specialist agent."""

    def __init__(self, article_content: str, model_name: str = "gpt-4o"):
        """Initialize developer agent with article content and model."""
        super().__init__(article_content, "Developer", model_name)


class Summarizer(ArticleAgent):
    """Summarizer specialist agent."""

    def __init__(self, article_content: str, model_name: str = "gpt-4o"):
        """Initialize summarizer agent with article content and model."""
        super().__init__(article_content, "Summarizer", model_name)


class Explainer(ArticleAgent):
    """Explainer specialist agent."""

    def __init__(self, article_content: str, model_name: str = "gpt-4o"):
        """Initialize explainer agent with article content and model."""
        super().__init__(article_content, "Explainer", model_name)


class AnalogyCreator(ArticleAgent):
    """Analogy Creator specialist agent."""

    def __init__(self, article_content: str, model_name: str = "gpt-4o"):
        """Initialize analogy creator agent with article content and model."""
        super().__init__(article_content, "Analogy Creator", model_name)


class VulnerabilityExpert(ArticleAgent):
    """Vulnerability Expert specialist agent."""

    def __init__(self, article_content: str, model_name: str = "gpt-4o"):
        """Initialize vulnerability expert agent with article content and model."""
        super().__init__(article_content, "Vulnerability Expert", model_name)


async def run_article_explanation(article_content: str, model_name: str = "gpt-4o") -> str:
    """Run the complete article explanation pipeline.

    Args:
        article_content: The article content text
        model_name: The name of the model to use

    Returns:
        Final explanation from the multi-specialist team
    """
    # Create specialist agents with their own model instances
    agents = {
        "Developer": Developer(article_content, model_name),
        "Summarizer": Summarizer(article_content, model_name),
        "Explainer": Explainer(article_content, model_name),
        "Analogy Creator": AnalogyCreator(article_content, model_name),
        "Vulnerability Expert": VulnerabilityExpert(article_content, model_name),
    }

    # Run all agents concurrently
    tasks = [agent.run() for agent in agents.values()]
    responses = await asyncio.gather(*tasks)

    # Map responses back to agent names
    agent_names = list(agents.keys())
    specialist_reports = dict(zip(agent_names, responses, strict=False))

    # Create and run multi-specialist team
    team = MultiSpecialistTeam(
        developer_report=specialist_reports["Developer"],
        summarizer_report=specialist_reports["Summarizer"],
        explainer_report=specialist_reports["Explainer"],
        analogy_creator_report=specialist_reports["Analogy Creator"],
        vulnerability_expert_report=specialist_reports["Vulnerability Expert"],
        model_name=model_name,
    )

    # Run the team and get final analysis
    final_analysis = await team.run()
    return final_analysis
