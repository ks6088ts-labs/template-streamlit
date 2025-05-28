from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv

from template_streamlit.dify.client import Client
from template_streamlit.dify.settings import Settings

load_dotenv(override=True)
logger = getLogger(__name__)


def create_client():
    return Client(
        settings=Settings(),
    )


with st.sidebar:
    dify_api_key = st.text_input(
        label="Dify API Key",
        value=getenv("DIFY_API_KEY", ""),
        key="DIFY_API_KEY",
        type="password",
    )
    "[Getting Started > API Access](https://docs.dify.ai/en/openapi-api-access-readme)"

st.title("Dify Playground")

input = st.text_area(
    label="Context",
    value="",
    key="CONTEXT",
    height=300,
)


def is_configured():
    return dify_api_key and input and len(input) > 0


if not is_configured():
    st.warning("Please fill in the required fields at the sidebar and the context input box.")


if st.button("Run workflow", disabled=not is_configured()):
    try:
        client = create_client()
        with st.spinner("Creating client..."):
            response = client.workflows_run(
                inputs={
                    "requirements": input,
                },
            )
            st.success("Client created successfully!")
            st.json(response)
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        st.error(f"Error creating client: {e}")
