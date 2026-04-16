# conda env: ManTouAgent
# author: Kuang Liang

import json
import asyncio
from prompt_toolkit.patch_stdout import patch_stdout
from agent.message_hub import (
    Message,
    MessageChannelType,
    MessageHub
)
from channels.qq import (
    QQChannel
)
from channels.cli import (
    CLIChannel
)
from env import (
    QQ_APP_ID,
    QQ_APP_SECRET
)
from agent.context import (
    Context
)
from agent.loop import (
    AgentLoop
)
from agent.utils import (
    to_content
)


async def main():
    message_bus = MessageHub()

    # cli_channel = CLIChannel(
    #     message_bus=message_bus
    # )
    qq_channel = QQChannel(
        message_bus=message_bus,
    )

    # asyncio.create_task(cli_channel.start())
    asyncio.create_task(qq_channel.start(
        appid=QQ_APP_ID,
        secret=QQ_APP_SECRET,
    ))

    context = Context()
    loop = AgentLoop(
        context=context,
    )

    try:

        messages = context.init_messages()

        with patch_stdout():
            while True:
                message: Message = await message_bus.input.get()
                messages = context.append_user_message(
                    messages=messages,
                    content=to_content(
                        text=message.content
                    )
                )


                content = await loop.run(
                    messages=messages
                )
                messages = context.append_assistant_message(
                    messages=messages,
                    content=content,
                )

                if message.channel_type == MessageChannelType.QQ:
                    await qq_channel.send(
                        Message(
                            content=content[-1]["text"],
                            channel_type=MessageChannelType.Agent,
                            payload=message.payload
                        )
                    )

    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == '__main__':
    asyncio.run(main())

    # 现在几点了
    # 帮我查看一下 {workspace}/1.txt文件写的啥
    # 帮我访问一下 http://192.168.0.104:9999/demo/agent/text
    # 帮我访问一下 http://192.168.0.104:9999/demo/agent/image/jpg