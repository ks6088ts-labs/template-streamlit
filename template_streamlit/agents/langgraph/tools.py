from langchain_core.tools import tool


@tool
def get_weather(location: str):
    """Call to get the current weather."""
    # A simplified weather response based on location
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."


@tool
def get_coolest_cities():
    """Get a list of coolest cities."""
    # Hardcoded response with a list of cool cities
    return "nyc, sf"


def get_tools():
    """Get the list of tools."""
    return [get_weather, get_coolest_cities]
