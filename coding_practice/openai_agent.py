import openai
import json

# Define the functions the LLM can call
def get_weather(location):
    """Fetch the current weather for a location (mock implementation)."""
    weather_data = {
        "New York": "Sunny, 22°C",
        "London": "Rainy, 15°C",
        "Tokyo": "Cloudy, 19°C"
    }
    return weather_data.get(location, "Weather data unavailable")

def book_hotel(location, nights):
    """Mock function to book a hotel."""
    return f"Booked a hotel in {location} for {nights} nights."

# Step 1: Define the function schemas for the LLM
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g., 'New York'"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "book_hotel",
        "description": "Book a hotel for a specified number of nights",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city to book the hotel in"
                },
                "nights": {
                    "type": "integer",
                    "description": "Number of nights to stay"
                }
            },
            "required": ["location", "nights"]
        }
    }
]

# Step 2: Call the LLM with the user query and function schemas
def run_conversation(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",  # Use a model that supports function calling
        messages=[{"role": "user", "content": query}],
        functions=functions,
        function_call="auto"  # Let the model decide if/which function to call
    )

    message = response.choices[0].message

    # Step 3: Handle function calls
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        arguments = json.loads(message["function_call"]["arguments"])

        if function_name == "get_weather":
            result = get_weather(arguments["location"])
        elif function_name == "book_hotel":
            result = book_hotel(arguments["location"], arguments["nights"])

        # Step 4: Send the function result back to the LLM
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": query},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": result
                }
            ]
        )
        return second_response.choices[0].message["content"]
    else:
        return message["content"]

# Example usage
query = "What's the weather in New York? Also, book a hotel there for 3 nights."
response = run_conversation(query)
print(response)
