import os
import json
import requests
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def get_temperature(latitude:float, longitude:float) -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",
        "timezone": "auto"
    }

    try:
        response = requests.get(url=url, params=params, timeout=3.0)
        response.raise_for_status()
        response = response.json()
        temp = response['current']['temperature_2m']
        units = response['current_units']['temperature_2m']
        return f"The temperature is {temp} {units}"
    except requests.HTTPError:
        return f"API Error getting temperature."
    except Exception as e:
        return f"Error getting temperature: {e}"

tools = [
    {
        "type":"function",
        "function":{
            "name": "get_temperature",
            "description":"Returns temperature at a location.",
            "parameters":{
                "type":"object",
                "properties":{
                    "latitude":{
                        "type":"number",
                        "description":"Location latitude",
                    },
                    "longitude":{
                        "type":"number",
                        "description":"Location longitude"
                    },
                },
                "required":["latitude", "longitude"],
            },
        },
    },
]

tool_mapping ={
    "get_temperature":get_temperature,
}

def agent_chat(query:str):
    messages = [
        {"role":"user", "content":query}
        ]
    
    while True:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        messages.append(response_message.model_dump())

        print("DBG - messages:", messages)
        if not response_message.tool_calls:
            return response_message.content
        
        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            print(f"DBG - calling function {func_name} with args: {func_args}")
            func_output = tool_mapping[func_name](**func_args)
            print(f"DBG- func_output:", func_output)
            messages.append({
                "role":"tool",
                "name":func_name,
                "content":func_output,
                "tool_call_id":tool_call.id,
            })


query="What is the temperature in Boston and Paris?"
print(agent_chat(query))

