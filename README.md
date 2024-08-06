# dotbot-neverland

A hack.chat bot framework which is simple, powerful, robust.

## Documents

WIP

## TODO

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
  - [ ] ability to know whether a message is accepted by HC (difficult)
  - [ ] optional auto-retry mechanism

## Credits

- foolishbird by light/await

  This inspired me to start both making HC bots and learning Python.

- [hvicorn](https://github.com/Hiyoteam/hvicorn) by [0x24a](https://github.com/0x24a)

  This bot framework realized my dream of a "well typed" bot framework. It is very creative compared to previous bot frameworks, and dotbot-neverland references it heavily. Actually, the whole design of dotbot-neverland is inspired by hvicorn.
