import json
from groq import Groq
import os


class Tools:
    def __init__(self):
        self.tools = {}
        self.functions = {}

    def add_tool(self, function, description):
        self.tools[function.__name__] = description
        self.functions[function.__name__] = function
    
    def get_tools(self):
        return list(self.tools.values())

    def function_call(self, tool_call_response):
        function_name = tool_call_response.function.name
        arguments = json.loads(tool_call_response.function.arguments)

        f = self.functions[function_name]
        result = f(**arguments)

        return {
            "role": "tool",
            "type": "function_call_output",
            "call_id": tool_call_response.id,
            "output": json.dumps(result, indent=2),
        }


def shorten(text, max_length=50):
    return text if len(text) <= max_length else text[:max_length-3] + "..."

class ChatAssistant:
    def __init__(self, tools, developer_prompt, model='meta-llama/llama-4-scout-17b-16e-instruct'):
        #meta-llama/llama-4-scout-17b-16e-instruct
        self.tools = tools
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.developer_prompt = developer_prompt
        

    def call_model(self, chat_messages):
        return self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            tools=self.tools.get_tools(),
            tool_choice="auto"
        )

    
    def run(self):
        chat_messages = [
            {"role": "system", "content": self.developer_prompt}
        ]

        while True:
            question = input()
            if question == 'stop':
                break

            
            message = {"role": "user",   "content": question}
            chat_messages.append(message)

            while True:

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=chat_messages,
                    tools=self.tools.get_tools(),
                    tool_choice="auto"    # or "manual" if you want to force a tool call
                )

                fin_reason = response.choices[0].finish_reason

                has_message = False

                if fin_reason == 'tool_calls':
                    tool_calls = response.choices[0].message.tool_calls
                    for tool_call in tool_calls:
                        print('tool_call')
                        print(tool_call)
                        print()
                        res = self.tools.function_call(tool_call)
                        chat_messages.append(
                            {
                                "role": "tool",
                                "content": str(res),
                                "tool_call_id": tool_call.id,
                            }
                        )
                elif fin_reason == 'stop':
                    has_message = True
                    print('has_message')
                    print(response.choices[0].message.content)
                    print()

                if has_message:
                    break





if __name__ == "__main__":
    # Example tool
    def search_faq(query: str):
        return {"results": ["Entry1", "Entry2"]}

    faq_params = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search term"}
        },
        "required": ["query"]
    }

    

    tools = Tools()
    tools.add_tool(search_faq, faq_params)

    assistant = ChatAssistant(tools, "You are a course teaching assistant.")
    assistant.run()
