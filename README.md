# Python Discord Bot

Simple discord bot created in Python. Currently, it takes in a `commands.yaml` file and will return a string based on
the command given.

## Usage

Follow the steps found [here](https://realpython.com/how-to-make-a-discord-bot-python/) to set up a new bot with discord
and copy the token in to an environment variable `export DISCORD_TOKEN=<Your_Token>`. Then run

```bash
@docker run \
    --rm \
    -v path_to_your_commands_directory:/commands \
    --env DISCORD_TOKEN=${DISCORD_TOKEN} \
    --name ${APP_CONTAINER_NAME} \
    ghcr.io/clickandobey/python-discord-bot:1.0.0
```

Alternatively for the above command you can build a docker image based off of this bot, and overwrite the contents of
the `/commands` directory. This allows you to remove the mount line (the one with `-v`).

## Quick Start

1. Run `make`

## Useful Documents

* [Development](docs/development.md)