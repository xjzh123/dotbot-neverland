# Documentations

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
    if c.event.text == ":ping":
        await c.reply("pong!")


asyncio.run(bot.connect("lounge", "ping", os.getenv("HC_PWD"), bypass_dns=True))
```

## Listeners

You can listen to a certain type of event:

```py
@bot.on(ChatEvent)
def on_chat(c: Context[ChatEvent]):
   ...
```

Using a string alias is also OK:

```py
@bot.on("chat")
def on_chat(c: Context[ChatEvent]):
   ...
```

You can listen to multiple types of event:

```py
@bot.on("chat", "whisper")
def on_msg(c: Context[ChatEvent | WhisperEvent]):
   ...
```

> **NOTE:** Although technically there are some "is-a" relationships between the event types (e.g. whisper messages are like `{"cmd": "info", "type": "whisper"}`, so they are also info messages), and in dotbot-neverland, we also use inheritance and subclasses to represent such a relationship, when you listen to event types, only the smallest type will be matched.
>
> For example, this will NOT listen to whispers:
>
> ```py
> @bot.on(InfoEvent)
> def on_info(c: Context[InfoEvent]):
>    ...
> ```
>
> Only info messages that are not identified to be any smaller supported types (whispers, emotes and invites) will come to this listener.

You can register listeners that listen to ALL messages with `*`:

```py
@bot.on("*")
def on_msg(c: Context[Event]):
   ...
```

By default, a bot only respond to other users' messages, but not to those of itself.

If you want to disable this behavior and make your bot respond to its own messages, use `ignore_self=False`:

```py
@bot.on("chat", ignore_self=False)
async def on_chat(c: Context[ChatEvent]):
    ...
```

## Bot features

A bot can send messages:

```py
await bot.chat("Hello!")
await bot.send("Hello!")  # The same as chat
await bot.whisper(nick, "Hello!")
await bot.emote(nick, "Hello!")
await bot.change_nick(new_nick)
await bot.change_color("66ccff")
await bot.send_json({"cmd": "kick", "nick": bad_nick})  # Wow! Are you a moderator?
```

You can access the bot's parameters:

```py
bot.channel
bot.nick
bot.password
```

The bot knows what users are online:

```py
bot.users
bot.nicks
bot.users_dict[nick]
```

## Using contexts

Context provides more powerful functions over those of bots and messages.

You can access `c.bot` and `c.event`.

You can reply to a message:

```py
c.reply("pong!")
```

If this message is a chat message, your bot will use chat to reply. If it is a whisper message, your bot will use whisper to reply.

You can get full user info from the message:

```py
c.get_user()
```

This will query `bot.users_dict` with the nick given in the message.

You can also use `c.get_channel()` to get the channel if it is provided by the message.

## Updatable Messages

See this example:

```py
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
```
