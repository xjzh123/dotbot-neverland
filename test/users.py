import asyncio
import os

from dotbot_neverland import Bot, BotJoinEvent, ChatEvent, Context, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[BotJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", "whisper")
async def ping(c: Context[ChatEvent | WhisperEvent]):
    if c.event.text == ":users":
        await c.reply(
            "```py\n{}\n```".format(list(str(c.bot.nicks))), whisper_newline=True
        )


asyncio.run(bot.connect("lounge", "users", os.getenv("HC_PWD"), bypass_dns=True))
