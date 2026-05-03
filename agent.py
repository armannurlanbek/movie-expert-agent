from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from tools import tool_registry, tools


# Load env vars once before creating clients.
load_dotenv()

# Initialize API clients/keys used by the agent loop.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
imdb_key = os.getenv("IMDB_KEY")

# Conversation state sent to the Responses API.
input_list = []

# Outer loop: keep chat session running until user stops program.
while True:
    user_input = input("Ask a question: ")
    input_list.append({"role": "user", "content": f"{user_input}"})
    # Inner loop: keep resolving tool calls until model returns plain text.
    while True:

        response = client.responses.create(
            model = "gpt-4o-mini",
            instructions = "You are a movie expert. Answer questions about movies",
            input = input_list,
            tools = tools
        )
        input_list += response.output


        # Extract only function calls from model output.
        tool_calls = [item for item in response.output if item.type == "function_call"]

        if not tool_calls:
            print(f"\n[REASONING] Direct response — using conversation context")
            print(f"[RESPONSE PREVIEW] {response.output_text[:80]}...")
            break

        if tool_calls:
            print(f"\n[REASONING] Decided to call {len(tool_calls)} tool(s): {[t.name for t in tool_calls]}")

        # Execute each requested tool and return outputs back to the model.
        for item in tool_calls:
            print(f"\n[TOOL CALL] {item.name}({json.loads(item.arguments)})")
            func = tool_registry.get(item.name)

            if func is None:
                result = f"Unknown tool: {item.name}"
            
            args = json.loads(item.arguments)
            result = func(**args)

            input_list.append({
               "type": "function_call_output",
               "call_id": item.call_id,
               "output": result 
            })
            print(f"[TOOL RESULT] {result[:100]}...")
    
    # Print final natural-language answer after tool loop completes.
    print("Final answer: " + response.output_text)

    # Trim long histories by summarizing older turns.
    if len(input_list) > 11:

        user_indices = [i for i, m in enumerate(input_list) 
                if isinstance(m, dict) and m.get("role") == "user"]

        if len(user_indices) >= 3:
            cut_at = user_indices[2]  # keep last 2 turns intact
            messages_to_summarize = input_list[:cut_at]
            messages_to_keep = input_list[cut_at:]

            # Create a compact summary to reduce token usage.
            sum_response = client.responses.create(
                model = "gpt-4o-mini",
                instructions = f"You are AI agent summarizer. Your task is to summarize the oldest 5 messages into one summarized message.",
                input = f"Summarize these messages: {messages_to_summarize}"
        )
            summary_msg = {"role": "user", "content": f"Summary of earlier conversation: {sum_response.output_text}"}
            input_list[:] = [summary_msg] + messages_to_keep
