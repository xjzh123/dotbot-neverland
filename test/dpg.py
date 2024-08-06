import asyncio
import os
import random
import re

from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.change_color("20201D")


say_regex = re.compile(r"说([一-龟]+)")


@bot.on("chat")
async def dpg(c: Context[ChatEvent]):
    if f"@{c.bot.nick}" in c.event.text:
        if (match := say_regex.search(c.event.text)):
            await c.bot.chat(match.group(1))
        else:
            if random.random() > 0.5:
                await c.bot.chat("ovo")


asyncio.run(bot.connect("lounge", "_", os.getenv("HC_PWD"), bypass_dns=True))
