import logging
from os import getenv

import typer
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from openai import AzureOpenAI
from openai.types.chat.chat_completion import ChatCompletion

load_dotenv()
logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def openai(
    prompt: str = "hello",
    stream: bool = False,
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Processing with OpenAI: {prompt}")

    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )

    if stream:
        for chunk in client.chat.completions.create(
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
        resonse: ChatCompletion = client.chat.completions.create(
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

    model: BaseChatOpenAI = AzureChatOpenAI(
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        openai_api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=getenv("AZURE_OPENAI_GPT_MODEL"),
    )

    if stream:
        for chunk in model.stream(input=prompt):
            print(chunk.content, end="|", flush=True)
    else:
        response = model.invoke(input=prompt)
        print(response.content)


if __name__ == "__main__":
    app()
