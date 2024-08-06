import asyncio

from dotbot_neverland import Bot

bot = Bot()


@bot.on("onlineSet")
async def hello(c):
    await c.bot.chat("Hello from dotbot-neverland!")


asyncio.run(bot.connect("lounge", "hello"))
