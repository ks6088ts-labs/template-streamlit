import logging
import uuid
from typing import Annotated

import typer

from template_streamlit.agents.chatbot_with_tools import graph
from template_streamlit.loggers import get_logger

app = typer.Typer(
    add_completion=False,
    help="Workflows CLI",
)

# Set up logging
logger = get_logger(__name__)


@app.command()
def chatbot_with_tools(
    prompt: Annotated[
        str,
        typer.Option(
            "--prompt",
            "-p",
            help="Prompt for the skeleton",
        ),
    ] = "Hello World",
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
):
    # Set up logging
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug(f"This is a debug message with prompt: {prompt}")
    config = {
        "configurable": {
            "thread_id": uuid.uuid4().hex,
        },
    }

    while True:
        exit_code = "q"
        query = input(f"Enter a query(type '{exit_code}' to exit): ")
        if query == exit_code:
            break

        events = graph.stream(
            input={
                "messages": [
                    ("user", query),
                ]
            },
            config=config,
            stream_mode="values",
        )
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()


if __name__ == "__main__":
    app()
