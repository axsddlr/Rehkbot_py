# Rehkbot

Personal Discord bot

## Requirements

- Python 3.6 and up - https://www.python.org/downloads/
- git - https://git-scm.com/download/

### ENV

rename `.env.example` to `.env` then store your token and some other private info like this:

```
DISCORD_TOKEN =
DISCORD_BOT_ID =
TWITCH_CLIENT_ID =
TWITCH_CLIENT_SECRET =
WEBHOOK_URL =
```

### CONFIG.ini (for twitchlive_notify)

rename `config_example.ini` to `config.ini` then store your token and some other private info like this:

```
[Twitch]
User =
ImagePriority = Game

[Discord]
Message =
Description =

```

### PM2

PM2 is an alternative script provided by NodeJS, which will reboot your bot whenever it crashes and keep it up with a nice status. You can install it by doing `npm install -g pm2` and you should be done.

```
# Start the bot
pm2 start pm2.json

# Tips on common commands
pm2 <command> [name]
  start discordbot.py    Run the bot again if it's offline
  list                    Get a full list of all available services
  stop discordbot.py     Stop the bot
  reboot discordbot.py   Reboot the bot
```
