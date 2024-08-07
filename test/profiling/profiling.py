import cProfile
import os

import asyncio
from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", "whisper")
async def ping(c: Context[ChatEvent | WhisperEvent]):
    if c.event.text == ":ping" or c.event.text == "!trip":
        await c.reply("pong!")
    elif c.event.text == ":quit":
        await c.bot.close()


def main():
    asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD"), bypass_dns=True))


cProfile.run("main()")
