import asyncio
from pydantic import (
    BaseModel
)
from typing import (
    Any,
    Optional
)
from enum import (
    Enum,
    unique
)


@unique
class MessageChannelType(Enum):
    CLI = "cli"
    QQ = "qq"
    Agent = "agent"


class Message(BaseModel):
    channel_type: MessageChannelType
    content: str
    payload: Optional[Any] = None


class MessageHub:
    def __init__(self):
        self.__queue = asyncio.Queue()
        self.__input_queue = asyncio.Queue()
        self.__output_queue = asyncio.Queue()

    @property
    def input(self):
        return self.__input_queue

    @property
    def output(self):
        return self.__output_queue

    async def put(self, message: Message):
        await self.__queue.put(message)

    async def get(self) -> Message:
        return await self.__queue.get()


