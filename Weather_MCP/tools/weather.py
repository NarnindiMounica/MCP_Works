import urllib
from urllib import request

def get_weather(location:str)->str:
    """
    Fetches the weather for a given loaction

    Args:
    location(str): The city of location name (example: London, New York)
    
    Returns:
    str: concise weather information for the location.
    """

    try:
        url=f"https://wttr.in/{location}?format=3"
        with urllib.request.urlopen(url) as response:
            result = response.read().decode("utf-8").strip()
            return result

    except Exception as e:
        return f"Error : {e}"
    
#print(get_weather(location="vizag"))