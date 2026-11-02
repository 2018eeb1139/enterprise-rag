import os
import json
from groq import Groq
from dotenv import load_dotenv
from utilities.utilities import log
from tools import TOOLS, run_tool


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages=[]
MAX_STEPS=5

messages.append(
    {
        "role":"system",
        "content":"Act as a humble agent and always respond under 10 words."
    }
)

while(True):
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit","bye","goodbye"]:
        break

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL"),
                messages=messages,
                tools=TOOLS
            )
        
        msg = response.choices[0].message
        
        if not msg.tool_calls:
            break

        log(f"Step {step + 1} model requested {len(msg.tool_calls)} tool calls")

        messages.append(msg)

        for tool_call in msg.tool_calls: 
            result = run_tool(tool_call)
            messages.append(
                {
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":str(result)
                }
            )

    else:
        fallback = "Sorry I could not able to answer within step limit."
        messages.append(
                {
                    "role":"assistant",
                    "content":fallback
                }
            )
        continue

    messages.append(
        {
            "role":"assistant",
            "content":msg.content
        }
    )

    print(msg.content or "")




    



