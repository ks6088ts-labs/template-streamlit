import asyncio
from logging import getLogger

import streamlit as st
from dotenv import load_dotenv

from template_streamlit.msgraph.client import Client
from template_streamlit.msgraph.settings import Settings

load_dotenv(override=True)
logger = getLogger(__name__)

with st.sidebar:
    "Microsoft Graph API"


def get_client():
    return Client(
        settings=Settings(),
    )


st.title("Microsoft Graph API Playground")

st.divider()
st.write("### User Operations")
if st.button("Get Users"):

    async def async_get_users():
        return await get_client().get_users()

    try:
        with st.spinner("Fetching users..."):
            users = asyncio.run(async_get_users())
            st.write("Users:")
            for user in users.value:
                st.write(f"- {user.display_name}, Email: {user.mail}, ID: {user.id}")
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        logger.error(f"Error fetching users: {e}")

st.divider()
st.write("### Outlook Calendar Operations")

# Get calendar events for a specific user
user_id = st.text_input("Enter User ID for Calendar")
if st.button("Get Calendar Events"):

    async def async_get_calendar_events(user_id: str):
        return await get_client().get_calendar_events(user_id)

    try:
        with st.spinner("Fetching calendar events..."):
            events = asyncio.run(async_get_calendar_events(user_id))
            st.write("Calendar Events:")
            for event in events.value:
                st.write(f"- {event.subject}, Start: {event.start}, End: {event.end}")
    except Exception as e:
        st.error(f"Error fetching calendar events: {e}")
        logger.error(f"Error fetching calendar events: {e}")
