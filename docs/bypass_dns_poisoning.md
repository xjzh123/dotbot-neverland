# Bypass DNS poisoning

To bypass DNS poisoning in China, just use `bot.connect(channel, nick, bypass_dns=True)`. This will connect to the real IP address (hardcoded in the lib) of hack.chat, with a custom host header and disable SSL check.

> **NOTE:** If censorship towards hack.chat escalates, this may become ineffective.
