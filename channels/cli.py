from prompt_toolkit import PromptSession
from agent.message_hub import (
    Message,
    MessageChannelType,
    MessageHub,
)


class CLIChannel:
    def __init__(
            self,
            message_bus: MessageHub
    ):
        self.__message_bus = message_bus
        self.__session = PromptSession()

    async def start(self):
        while True:
            content = await self.__session.prompt_async('/>:')
            if not content:
                continue

            message = Message(
                content=content,
                channel_type=MessageChannelType.CLI,
            )
            await self.__message_bus.input.put(message)
