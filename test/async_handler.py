import asyncio
import os

from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", "whisper")
async def ping(c: Context[ChatEvent | WhisperEvent]):
    if c.event.text == ":ping":
        await c.reply("1")
        await asyncio.sleep(2)
        await c.reply("3")


@bot.on("chat", "whisper")
async def ping2(c: Context[ChatEvent | WhisperEvent]):
    if c.event.text == ":ping":
        await asyncio.sleep(1)
        await c.reply("2")
        await asyncio.sleep(2)
        await c.reply("4")


asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD"), bypass_dns=True))
