import asyncio
import os

from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", ignore_self=True)  # ignore_self is default True, so this can be omitted
async def ping(c: Context[ChatEvent]):
    if c.event.text == ":ping":
        await c.reply(":ping")


asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD"), bypass_dns=True))
