from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv(override=True)
logger = getLogger(__name__)

with st.sidebar:
    video_id = st.text_input(
        label="YouTube Video ID",
        value=getenv("YOUTUBE_VIDEO_ID", "dQw4w9WgXcQ"),
        key="YOUTUBE_VIDEO_ID",
        type="default",
    )
    languages = st.text_input(
        label="Languages (comma-separated)",
        value=getenv("YOUTUBE_LANGUAGES", "en,ja"),
        key="YOUTUBE_LANGUAGES",
        type="default",
    )
    "[YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)"

st.title("YouTube Playground")


def is_configured():
    return video_id and languages


if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

if st.button("Transcribe Video", disabled=not is_configured()):
    video_id = st.session_state.get("YOUTUBE_VIDEO_ID")
    languages = st.session_state.get("YOUTUBE_LANGUAGES").split(",")

    try:
        with st.spinner("Fetching transcript..."):
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id=video_id,
                languages=languages,
            )
            transcript_text = " ".join(entry["text"] for entry in transcript if "text" in entry)
            st.success(f"Transcript for video {video_id}:")
            # text box to display the transcript
            st.text_area(
                label="Transcript",
                value=transcript_text,
                height=2000,
                key="transcript_text",
            )
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"An unexpected error occurred: {e}")
