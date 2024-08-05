import asyncio
import os

from dotbot_neverland import Bot, BotJoinEvent, ChatEvent, Context, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[BotJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", "whisper")
async def ping(c: Context[ChatEvent | WhisperEvent]):
    if c.event.text == ":ping":
        await c.reply("pong!")


asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD"), bypass_dns=True))
