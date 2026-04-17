from agent.tool import (
    tools,
    tool_registry
)
from agent.context import (
    Context
)
from api.ollama import (
    chat,
    ChatResponse
)
from agent.utils import (
    print_content,
    print_reasoning,
    print_tool_calls
)
from agent.utils import (
    to_content,
    format_text
)
import json
import copy
from typing import (
    List,
    Dict,
    Any
)


class AgentLoop:
    def __init__(
            self,
            context: Context,
            max_iterations: int = 40,
    ):
        self.__context = context
        self.__max_iterations = max_iterations

    async def run(
            self,
            messages: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        iteration = 0

        local_messages = copy.deepcopy(messages)

        while iteration < self.__max_iterations:
            iteration += 1

            response: ChatResponse = await chat(
                messages=local_messages,
                tools=tools,
                on_reasoning=print_reasoning,
                on_content=print_content,
                on_tool_calls=print_tool_calls,
            )

            content = to_content(
                text=f"<think>\n{response.reasoning}\n</think>\n{response.content}"
            )
            local_messages = self.__context.append_assistant_message(
                messages=local_messages,
                content=content,
                tool_calls=response.tool_calls,
            )

            if len(response.tool_calls) == 0:
                return [
                    format_text(text=response.content)
                ]

            for tool_call in response.tool_calls:
                is_image = False
                tool_call_id = tool_call["id"]
                tool_name = tool_call["function"]["name"]
                tool_arguments = tool_call["function"]["arguments"]
                tool_result: List[Dict[str, Any]] = await tool_registry.execute(
                    name=tool_name,
                    arguments=json.loads(tool_arguments),
                )

                str_result = json.dumps(tool_result, indent=4, ensure_ascii=False)
                if len(str_result) > 300:
                    str_result = str_result[:300] + "..."
                print_tool_calls(str_result)

                for i in tool_result:
                    if i["type"] == "image_url":
                        self.__context.append_user_message(
                            local_messages,
                            tool_result
                        )
                        is_image = True
                
                if not is_image:
                    local_messages = self.__context.append_tool_message(
                        messages=local_messages,
                        tool_call_id=tool_call_id,
                        content=tool_result
                    )

        return [{
            "type": "text",
            "text": f"抱歉，我的能力有限，无法回复您的问题"
        }]
