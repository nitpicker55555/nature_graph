

from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
def message_template(role,new_info):
    new_dict={'role':role,'content':new_info}
    return new_dict

GPT_MODEL = "gpt-3.5-turbo-0613"
client = OpenAI()

def chat_single(messages,mode="",model="gpt-4o-mini"):
    if mode=="json":

        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            temperature=0,
            messages=messages
        )
        # print(response.usage)
    elif mode == 'stream':
        response = client.chat.completions.create(
        model=model,
        messages=messages,
            temperature=0,
        stream=True,
            max_tokens=2560

    )
        return response
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        temperature = 0,

        )

    # print(response)
    # response.usage.total_tokens
    # print(response.choices[0].message.content)

    return response.choices[0].message.content
