import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv(find_dotenv())
nvapi_key = os.getenv('NVIDIA_API_KEY')

# Initialize the OpenAI client for verification
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvapi_key 
)

def NIM_verifier(query, response):
    # Responsible for how the model="meta/llama3-70b-instruct acts upon the query and response relationship
    verification_instructions = ("""You are the verifier to determine if the following response '{response}' 
                                 is a reasonable answer to the query '{query}'. If the response seems reasonable
                                  and addresses the query, state in one sentence verbatim: "This output has been 
                                 verified through use of NVIDIA NIMs." If the response cannot be correct, state: 
                                 "There may have been a problem parsing the data." Then, in one short sentence only:
                                  If the final answer was not clear try to rewrite the exact query which was, "{query}", in a way
                                  that might work better for LangChain agents that interact with pandas dataframes and
                                  answer CSV questions. Do not state anything in your repsponse about LangChain, pandas,
                                  or CSV to the human. Include relevant financial equations in your suggestion to ensure
                                  the correctness of the mathematical approach."""
    )
    
    formatted_instructions = verification_instructions.format(query=query, response=response)

    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[
            {"role": "user", "content": f"Query: {query}"},
            {"role": "user", "content": f"Answer: {response}"},
            {"role": "user", "content": formatted_instructions}
        ],
        temperature=0.2,
        top_p=1,
        max_tokens=1024,
        stream=True
    )

    # Collect the full response from the model
    full_response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content

    return full_response