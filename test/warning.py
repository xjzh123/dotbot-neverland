import asyncio
import os

from dotbot_neverland import Bot, Context, SelfJoinEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.send("/")


asyncio.run(bot.connect("lounge", "test", os.getenv("HC_PWD"), bypass_dns=True))
