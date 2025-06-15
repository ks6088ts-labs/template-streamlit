import logging

import typer
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from template_streamlit.agents.langgraph.graph import BasicAgent
from template_streamlit.agents.langgraph.tools import get_tools
from template_streamlit.ai.client import Client
from template_streamlit.ai.settings import Settings

load_dotenv(override=True)
logger = logging.getLogger(__name__)
app = typer.Typer(
    add_completion=False,
    help="Agent CLI",
)


def create_graph():
    return BasicAgent(
        llm=Client(
            settings=Settings(),
        ).get_azure_chat_openai(),
        tools=get_tools(),
    ).create_graph()


@app.command()
def langgraph(
    system_prompt: str = "You are a helpful assistant.",
    prompt: str = "hello",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Processing with LangGraph: {prompt}")

    response = create_graph().invoke(
        {
            "messages": [
                AIMessage(content=system_prompt),
                HumanMessage(content=prompt),
            ]
        }
    )
    logger.info(f"Response: {response}")
    print(response["messages"][-1].content)


@app.command()
def draw_mermaid_png(
    output: str = "mermaid_graph.png",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    create_graph().get_graph().draw_mermaid_png(
        output_file_path=output,
    )


if __name__ == "__main__":
    app()
