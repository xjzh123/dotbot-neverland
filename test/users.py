import asyncio
import os

from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", "whisper")
async def ping(c: Context[ChatEvent | WhisperEvent]):
    match c.event.text.split():
        case [":users"]:
            await c.reply(
                "```py\n{}\n```".format(str(list(c.bot.nicks))), whisper_newline=True
            )
        case [":hash", str() as n] if n in c.bot.users_dict:
            await c.reply(c.bot.users_dict[n].hash)
        case [":hash"]:
            await c.reply(c.get_user().hash)


asyncio.run(bot.connect("lounge", "users", os.getenv("HC_PWD"), bypass_dns=True))
