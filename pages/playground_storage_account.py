from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv

from template_streamlit.storage.client import Client
from template_streamlit.storage.settings import Settings

load_dotenv(override=True)
logger = getLogger(__name__)

with st.sidebar:
    "Blob"
    authentication_method = st.selectbox(
        label="Authentication Method",
        options=["CONNECTION_STRING", "PASSWORDLESS"],
        index=0,
        key="AZURE_STORAGE_AUTHENTICATION_METHOD",
    )
    connection_string = st.text_input(
        label="Connection String",
        value=getenv("AZURE_STORAGE_CONNECTION_STRING"),
        key="AZURE_STORAGE_CONNECTION_STRING",
        type="password",
    )
    container_name = st.text_input(
        label="Container Name",
        value="container",
        key="AZURE_STORAGE_CONTAINER_NAME",
        type="default",
    )
    blob_name = st.text_input(
        label="Blob Name",
        value="blob",
        key="AZURE_STORAGE_BLOB_NAME",
        type="default",
    )
    blob_data = st.text_area(
        label="Blob Data",
        value="This is a sample blob data.",
        key="AZURE_STORAGE_BLOB_DATA",
        height=200,
    )


def is_configured():
    return connection_string and container_name and blob_name


def create_client():
    return Client(
        settings=Settings(),
        authentication_method=authentication_method,
    )


st.title("Azure Storage Playground")

if not is_configured():
    st.error("Please configure the connection string, container name, and blob name in the sidebar.")

st.write("### Container Operations")

# Create container
if st.button("Create Container", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Creating container..."):
            response = client.create_container(container_name)
            st.success(f"Container created: {response}")
    except Exception as e:
        st.error(f"Error creating container: {e}")
        logger.error(f"Error creating container: {e}")

# Delete container
if st.button("Delete Container", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Deleting container..."):
            response = client.delete_container(container_name)
            st.success(f"Container deleted: {response}")
    except Exception as e:
        st.error(f"Error deleting container: {e}")
        logger.error(f"Error deleting container: {e}")

# List containers
if st.button("List Containers", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Listing containers..."):
            containers = client.list_containers()
            st.write("Containers:")
            for container in containers:
                st.write(f"- {container['name']}")
    except Exception as e:
        st.error(f"Error listing containers: {e}")
        logger.error(f"Error listing containers: {e}")

st.write("### Blob Operations")

# Upload blob
if st.button("Upload Blob", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Uploading blob..."):
            response = client.upload_blob(container_name, blob_name, blob_data)
            st.success(f"Blob uploaded: {response}")
    except Exception as e:
        st.error(f"Error uploading blob: {e}")
        logger.error(f"Error uploading blob: {e}")

# Download blob
if st.button("Download Blob", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Downloading blob..."):
            data = client.download_blob(container_name, blob_name)
            st.text_area("Blob Data", value=data, height=200)
            st.success("Blob downloaded successfully.")
    except Exception as e:
        st.error(f"Error downloading blob: {e}")
        logger.error(f"Error downloading blob: {e}")

# Delete blob
if st.button("Delete Blob", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Deleting blob..."):
            response = client.delete_blob(container_name, blob_name)
            st.success(f"Blob deleted: {response}")
    except Exception as e:
        st.error(f"Error deleting blob: {e}")
        logger.error(f"Error deleting blob: {e}")

# List blobs
if st.button("List Blobs", disabled=not is_configured()):
    client = create_client()
    try:
        with st.spinner("Listing blobs..."):
            blobs = client.list_blobs(container_name)
            st.write("Blobs:")
            for blob in blobs:
                st.write(f"- {blob['name']}")
    except Exception as e:
        st.error(f"Error listing blobs: {e}")
        logger.error(f"Error listing blobs: {e}")
