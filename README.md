# [dotbot-neverland](https://github.com/xjzh123/dotbot-neverland)

A hack.chat bot framework which is simple, powerful, robust.

PyPI: [dotbot-neverland](https://pypi.org/project/dotbot-neverland/)

Installation with pip: `pip install dotbot-neverland`

## Why?

- Well typed

  All kinds of message are typed and you have IntelliSense. No need to deal with messy and unpredictable json objects.

- We do the messy part

  You only need to deal with bot logic, with these things available for free:

  - Parse whisper and emote message from server message like `XXX whispered: ...`
  - List of online users
  - Current nickname of your bot
  - Query full user info with nickname
  - ...

- For the future

  Dotbot-neverland is designed for [asyncio](https://docs.python.org/3/library/asyncio.html).
  
  Also, it is written in the latest syntax of Python 3.12. Therefore, it only supports `python >= 3.12`.

**Why Not?** There are also some limitations. If you need one of the followings, we suggest you choose [hvicorn](https://github.com/Hiyoteam/hvicorn):

- Synchronous or threaded API
- Compatible with older versions of Python

## Quickstart

```py
import asyncio
import os

from dotbot_neverland import Bot, ChatEvent, Context, SelfJoinEvent, WhisperEvent

bot = Bot()


@bot.on("onlineSet")
async def hello(c: Context[SelfJoinEvent]):
    await c.bot.chat("Hello from dotbot-neverland!")


@bot.on("chat", "whisper")
async def ping(c: Context[ChatEvent | WhisperEvent]):
    if c.event.text == "ping":
        await c.reply("pong!")


asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD")))
```

## Documentation

[/docs](https://github.com/xjzh123/dotbot-neverland/tree/master/docs)

## TODO

- [x] Bypass DNS poisoning
- [x] Graceful ignore self
- [ ] Informative error message
  - [x] Error during parcing
- [x] Update-able chat message
- [x] Graceful shutdown
- [ ] Command-like system
- [ ] Reusable collection of listeners
- [ ] Profiling and optimization
- [ ] Hook system and logging
- [ ] anti rate-limit and warnings
  - [ ] modelling of common warnings
  - [ ] built-in auto reconnecting
  - [ ] ability to know whether a message is accepted by HC (difficult)
  - [ ] optional auto-retry mechanism
- [ ] Documentation
  - [x] Articles
  - [ ] Generated API reference
  - [ ] Docstrings

## Credits

- foolishbird by light/await

  This inspired me to start both making HC bots and learning Python.

- [hvicorn](https://github.com/Hiyoteam/hvicorn) by [0x24a](https://github.com/0x24a)

  This bot framework realized my dream of a "well typed" bot framework. It is very creative compared to previous bot frameworks, and dotbot-neverland references it heavily. Actually, the whole design of dotbot-neverland is inspired by hvicorn.
