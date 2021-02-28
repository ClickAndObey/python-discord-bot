# Python Discord Bot

Simple discord bot created in Python. Currently, it takes in both yaml and python files to dynamically generate
commands. The python files must individually define an attribute `COMMAND` which is of type
`clickandobey.discord.bot.commands.function_command.FunctionCommand`, while the yaml file can load multiple commands or
a single one depending on your preference.

* [Example YAML](src/main/commands/hello.yaml)
* [Example Python](src/main/commands/who_wins.py)

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

Example:

1. Create a new file `Dockerfile`:

```Dockerfile
FROM ghcr.io/clickandobey/python-discord-bot:1.0.0

COPY python_command.py /commands/python_command.py
COPY yaml_commands.yaml /commands/yaml_commands.yaml
```

2. Run these commands:

```bash
docker build -t <your_image_name> -f Dockerfile_from_above .
docker run \
    --rm \
    -it \
    --env DISCORD_TOKEN=${DISCORD_TOKEN} \
    --name ${APP_CONTAINER_NAME} \
    <your_image_name>
```

## Quick Start

1. Run `make`

## Useful Documents

* [Development](docs/development.md)