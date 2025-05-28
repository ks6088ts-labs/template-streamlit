import json
import logging

import typer
from dotenv import load_dotenv

from template_streamlit.dify.client import Client
from template_streamlit.dify.settings import Settings

load_dotenv(override=True)

logger = logging.getLogger(__name__)
app = typer.Typer(
    add_completion=False,
    help="Dify API",
)


def get_client():
    """Get the Dify API client."""
    return Client(
        settings=Settings(),
    )


@app.command()
def workflows_run(
    input: str = "hello world",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    logger.info("Running workflows")
    client = get_client()
    response = client.workflows_run(
        inputs={
            "requirements": input,
        }
    )
    print(
        json.dumps(
            response,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    app()
