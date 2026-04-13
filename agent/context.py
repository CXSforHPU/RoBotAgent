from agent.prompt import (
    IDENTITY_PROMPT,
    SKILLS_PROMPT
)
from agent.skills import (
    Skills
)
from typing import (
    Any,
    List,
    Dict,
    Optional
)


class Role:
    System = "system"
    User = "user"
    Assistant = "assistant"
    Tool = "tool"


class Context:
    def __init__(self):
        self.__skills = Skills()

    def init_messages(self) -> List[Dict[str, Any]]:
        return [
            {
                "role": Role.System,
                "content": self.__build_system_prompt()
            }
        ]

    @staticmethod
    def append_user_message(
            messages: List[Dict[str, Any]],
            content: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        messages.append({
            "role": Role.User,
            "content": content
        })
        return messages

    @staticmethod
    def append_assistant_message(
            messages: List[Dict[str, Any]],
            content: Optional[List[Dict[str, Any]]] = None,
            tool_calls: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        if content is None and tool_calls is None:
            return messages

        message: Dict[str, Any] = {
            "role": Role.Assistant,
        }
        if content is not None:
            message["content"] = content
        if tool_calls is not None:
            message["tool_calls"] = tool_calls

        messages.append(message)
        return messages

    @staticmethod
    def append_tool_message(
            messages: List[Dict[str, Any]],
            tool_call_id: str,
            content: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        messages.append({
            "role": Role.Tool,
            "tool_call_id": tool_call_id,
            "content": content
        })
        return messages

    def __build_system_prompt(self) -> str:
        parts = [IDENTITY_PROMPT]

        if len(self.__skills) > 0:
            parts.append(self.__build_skills_prompt())

        system_prompt = "\n\n---\n\n".join(parts)
        return system_prompt

    def __build_skills_prompt(self) -> str:
        return f"{SKILLS_PROMPT}\n{self.__skills.summary()}"


def demo():
    context = Context()
    system_prompt = context.init_messages()[-1]["content"]
    print(system_prompt)
    print(f"length: {len(system_prompt)}")


if __name__ == '__main__':
    demo()