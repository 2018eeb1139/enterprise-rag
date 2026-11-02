import json
import requests
from datetime import datetime

from utilities.utilities import log

def get_current_time():
    return datetime.now()

def get_city_weather(city):
    response = requests.get(f"https://wttr.in/{city}?format=3",timeout=10)
    response.raise_for_status()
    return response.text

def get_user_city():
    return "Banglore"

def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f"{func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
        result = fn(**func_args)
        
    except Exception as e:
        result = f"Error while running function {func_name} : {e}"

    log(f"Result: {result}")

TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"returns the current date and time",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        } 
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"returns the weather of given city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get weather for"
                    }
                },
                "required":["city"]
            }
        } 
    },
    {
        "type":"function",
        "function":{
            "name":"get_user_city",
            "description":"returns the city where user lives",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time":get_current_time,
    "get_city_weather":get_city_weather,
    "get_user_city":get_user_city
}