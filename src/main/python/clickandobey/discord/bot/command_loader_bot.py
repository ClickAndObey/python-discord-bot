"""
Module containing the Hello Bot made to interact on Discord.
"""

from discord import Client
from logging import Logger

from clickandobey.discord.bot.commands.command_loader import CommandLoader


class CommandLoaderBot(Client):
    """
    Bot made to load commands for interaction on Discord
    """

    def __init__(self, command_loader: CommandLoader, logger: Logger, **options):
        super().__init__(**options)
        self.__logger = logger
        self.__command_loader = command_loader

    async def on_message(self, message):
        """
        Perform this method when a message comes in to the discord server we are watching.
        """
        # we do not want the bot to reply to itself
        self.__logger.debug(f"Message Author - {message.author.id}")
        if message.author.id == self.user.id:
            return

        self.__logger.debug(f"Message Content - {message.content}")
        if message.content.startswith("!"):
            content_split = message.content[1:].split(" ")
            command_name = content_split[0]
            self.__logger.debug(f"Command Name - {command_name}")
            args = content_split[1:]
            self.__logger.debug(f"Arguments - {args}")
            await message.reply(self.__command_loader.perform_command(command_name, args), mention_author=True)
