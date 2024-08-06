import asyncio
import os

from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat")
async def ping(c: Context[ChatEvent]):
    if c.event.text == ":ping":
        msg = await c.bot.chat_updatable("GO!")
        await asyncio.sleep(1)
        await msg.append("!")
        await asyncio.sleep(1)
        await msg.append("!")
        await asyncio.sleep(1)
        await msg.prepend("My")
        await asyncio.sleep(1)
        await msg.overwrite("BanG Dream! Its MyGO!!!!!")
        await msg.complete()
        # Why so many ppl in HC like MyGO?


asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD"), bypass_dns=True))
