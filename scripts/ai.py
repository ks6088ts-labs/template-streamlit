import logging
from os import getenv

import typer
from dotenv import load_dotenv
from openai.types.chat.chat_completion import ChatCompletion

from template_streamlit.ai.client import Client
from template_streamlit.ai.settings import Settings

load_dotenv(override=True)
logger = logging.getLogger(__name__)
app = typer.Typer(
    add_completion=False,
    help="Azure OpenAI CLI",
)


@app.command()
def openai(
    prompt: str = "hello",
    stream: bool = False,
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Processing with OpenAI: {prompt}")

    azure_openai = Client(
        settings=Settings(),
    ).get_azure_openai()

    if stream:
        for chunk in azure_openai.chat.completions.create(
            model=getenv("AZURE_OPENAI_GPT_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=True,
        ):
            if len(chunk.choices) <= 0:
                continue
            print(chunk.choices[0].delta.content, end="|", flush=True)
    else:
        resonse: ChatCompletion = azure_openai.chat.completions.create(
            model=getenv("AZURE_OPENAI_GPT_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        print(resonse.choices[0].message.content)


@app.command()
def langchain(
    prompt: str = "hello",
    stream: bool = False,
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Processing with LangChain: {prompt}")

    azure_chat_openai = Client(
        settings=Settings(),
    ).get_azure_chat_openai()

    if stream:
        for chunk in azure_chat_openai.stream(input=prompt):
            print(chunk.content, end="|", flush=True)
    else:
        response = azure_chat_openai.invoke(input=prompt)
        print(response.content)


if __name__ == "__main__":
    app()
