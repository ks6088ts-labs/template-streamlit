import logging

import typer
from dotenv import load_dotenv

from template_streamlit.storage.client import Client
from template_streamlit.storage.settings import Settings

load_dotenv(override=True)

logger = logging.getLogger(__name__)
app = typer.Typer(
    add_completion=False,
    help="Azure Storage CLI",
)


def get_client(authentication_method: str):
    """Get the storage client."""
    return Client(
        settings=Settings(),
        authentication_method=authentication_method,
    )


@app.command()
def create_container(
    container_name: str,
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Creating container: {container_name}")
    response = get_client(authentication_method).create_container(container_name)
    print(f"Container created: {response}")


@app.command()
def delete_container(
    container_name: str,
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Deleting container: {container_name}")
    response = get_client(authentication_method).delete_container(container_name)
    print(f"Container deleted: {response}")


@app.command()
def list_containers(
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info("Listing containers")
    containers = get_client(authentication_method).list_containers()
    for container in containers:
        print(f"Container: {container['name']}")


@app.command()
def upload_blob(
    container_name: str,
    blob_name: str,
    data: str,
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Uploading blob: {blob_name} to container: {container_name}")
    response = get_client(authentication_method).upload_blob(container_name, blob_name, data)
    print(f"Blob uploaded: {response}")


@app.command()
def download_blob(
    container_name: str,
    blob_name: str,
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Downloading blob: {blob_name} from container: {container_name}")
    data = get_client(authentication_method).download_blob(container_name, blob_name)
    print(f"Blob downloaded: {data}")


@app.command()
def delete_blob(
    container_name: str,
    blob_name: str,
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Deleting blob: {blob_name} from container: {container_name}")
    response = get_client(authentication_method).delete_blob(container_name, blob_name)
    print(f"Blob deleted: {response}")


@app.command()
def list_blobs(
    container_name: str,
    authentication_method: str = "CONNECTION_STRING",
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Listing blobs in container: {container_name}")
    blobs = get_client(authentication_method).list_blobs(container_name)
    for blob in blobs:
        print(f"Blob: {blob['name']}")


if __name__ == "__main__":
    app()
