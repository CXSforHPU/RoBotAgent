import botpy
from botpy.message import (
    C2CMessage
)
from pydantic import (
    BaseModel
)
from agent.message_hub import (
    Message,
    MessageChannelType,
    MessageHub,
)


class QQMessagePayload(BaseModel):
    user_openid: str
    message_id: str
    message_type: int = 0
    message_sequence: int = 0


class QQChannel(botpy.Client):
    def __init__(
            self,
            message_bus: MessageHub
    ):
        intents = botpy.Intents(public_messages=True)
        super().__init__(
            intents=intents
        )
        self.__message_hub = message_bus

    async def on_c2c_message_create(
            self,
            message: C2CMessage
    ) -> None:
        await self.__message_hub.input.put(Message(
            content=message.content,
            channel_type=MessageChannelType.QQ,
            payload=QQMessagePayload(
                user_openid=message.author.user_openid,
                message_id=message.id,
            )
        ))

    async def send(self, message: Message) -> None:
        await self.api.post_c2c_message(
            openid=message.payload.user_openid,
            msg_type=message.payload.message_type,
            msg_id=message.payload.message_id,
            msg_seq=message.payload.message_sequence,
            content=message.content
        )

