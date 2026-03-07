import asyncio
from mistralai import Mistral
from mistralai.models import UserMessage
import time
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class MistralConfig(BaseSettings):
    MISTRAL_API_KEY: SecretStr
    LLM:str = "mistral-small-2506"

    model_config = SettingsConfigDict(env_file="C:\\Users\\sebas\\source\\repos\\knowledge_companion\\.env", extra="ignore")


async def heartbeat():
    while True:
        print("Loop is free...")
        await asyncio.sleep(0.5)

async def response_w_hearbeat(client:Mistral, model:str, content:str):

    # Schedule the heartbeat concurrently
    hb_task = asyncio.create_task(heartbeat())

    # The loop will continue running heartbeat() while waiting for this:
    chat_response = await client.chat.complete_async(
        model=model,
        messages=[UserMessage(content=content)],
    )
    print(chat_response.choices[0].message.content)
    print("now we wait")
    await asyncio.sleep(2)
    hb_task.cancel()
    return chat_response

if __name__ == "__main__":
    config = MistralConfig()
    client = Mistral(api_key=config.MISTRAL_API_KEY.get_secret_value())
    response = asyncio.run(response_w_hearbeat(client=client, model=config.LLM, content="How far is the moon from earth?"))
    print(response.choices[0].message.content)