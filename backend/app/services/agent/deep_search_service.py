import asyncio
import logging
import os
import time
import uuid

from smolagents import CodeAgent, LiteLLMModel
from smolagents.default_tools import DuckDuckGoSearchTool

# Using the requested import path
from app.services.github.schema import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)


def _create_agent() -> CodeAgent:
    """Initializes the expensive agent object."""
    logger.info("Initializing Deep Search Agent...")
    # Skip initialization if in demo mode
    if os.getenv("DEMO_MODE", "false").lower() == "true":
        logger.info("DEMO_MODE enabled: Skipping Deep Search Agent initialization.")
        return None # type: ignore

    if "ANTHROPIC_API_KEY" not in os.environ:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set.")

    model_id = "claude-sonnet-4-20250514"
    model = LiteLLMModel(model_id=model_id, temperature=0.1)
    search_tool = DuckDuckGoSearchTool()
    agent = CodeAgent(tools=[search_tool], model=model, max_steps=2)
    logger.info("Deep Search Agent created successfully!")
    return agent


# --- One-Time Initialization ---
# This agent is created once when the module is first imported.
deep_search_agent = _create_agent()
AGENT_ID = f"deep-search-func-{str(uuid.uuid4())[:8]}"


async def run_deep_search(agent_request: AgentRequest) -> AgentResponse:
    """Runs the agent with a user's prompt."""
    start_time = time.time()
    prompt = agent_request.prompt+"\n\nThe final answer should be less then 50 sentences."
    logger.info(f"Agent running search for: '{prompt[:70]}...'")

    try:
        # Check for DEMO_MODE
        if os.getenv("DEMO_MODE", "false").lower() == "true":
            logger.info("DEMO_MODE is enabled. Returning mock deep search response.")
            await asyncio.sleep(2.0) # Simulate search time
            final_answer = (
                f"**[DEMO MODE] Deep Search Result for: {agent_request.prompt}**\n\n"
                "Based on the analysis of the request, here are the key findings:\n\n"
                "1. **Market Trends**: The AI agent market is rapidly evolving with a focus on autonomous task execution.\n"
                "2. **Competitor Analysis**: Key players are integrating multi-modal capabilities (text, image, voice).\n"
                "3. **Strategic Recommendations**: Focus on user experience and seamless integration with existing workflows.\n\n"
                "This is a simulated response for demonstration purposes."
            )
        else:
            # Run the synchronous agent.run in a separate thread
            if deep_search_agent is None:
                 raise RuntimeError("Deep Search Agent not initialized (check API keys).")
            final_answer = await asyncio.to_thread(deep_search_agent.run, prompt)
    except Exception as e:
        raise RuntimeError(f"Agent execution failed: {e}")

    execution_time = time.time() - start_time
    return AgentResponse(
        response=final_answer,
        agent_id=AGENT_ID,
        execution_time=execution_time,
        metadata={"prompt_length": len(prompt)},
    )