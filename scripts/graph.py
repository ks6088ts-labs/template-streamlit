import asyncio
import logging

import typer
from dotenv import load_dotenv

from template_streamlit.msgraph.client import Client
from template_streamlit.msgraph.settings import Settings

load_dotenv(override=True)

logger = logging.getLogger(__name__)
app = typer.Typer(
    add_completion=False,
    help="Azure Storage CLI",
)


async def async_get_users():
    client = Client(
        settings=Settings(),
    )
    users = await client.get_users()
    return users.value


async def async_get_calendar_events(user_id: str):
    client = Client(
        settings=Settings(),
    )
    events = await client.get_calendar_events(user_id)
    return events.value


@app.command()
def get_users(
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    users = asyncio.run(async_get_users())
    for user in users:
        typer.echo(f"User: {user.display_name}, Email: {user.mail}, ID: {user.id}")


@app.command()
def get_calendar_events(
    user_id: str,
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    events = asyncio.run(async_get_calendar_events(user_id))
    for event in events:
        typer.echo(f"Event: {event.subject}, Start: {event.start}, End: {event.end}")


if __name__ == "__main__":
    app()
