import logging

import typer
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv(override=True)
logger = logging.getLogger(__name__)
app = typer.Typer(
    add_completion=False,
    help="YouTube Transcript API",
)


@app.command()
def transcribe(
    video_id: str = "dQw4w9WgXcQ",
    languages: str = "en,ja",  # Comma-separated list of languages
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Transcribing video: {video_id}")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=languages.split(","),
        )
        typer.echo(f"Transcript for video {video_id}:")
        # extract text from transcript entries and squash them together
        transcript = [{"text": entry["text"]} for entry in transcript if "text" in entry]
        typer.echo(" ".join(entry["text"] for entry in transcript))
    except Exception as e:
        logger.error(f"Error fetching transcript: {e}")
        typer.echo(f"Error fetching transcript: {e}")


if __name__ == "__main__":
    app()
