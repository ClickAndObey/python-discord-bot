"""
Module containing the Hello Bot made to interact on Discord.
"""

from discord import Client
from logging import Logger

from clickandobey.discord.bot.commands.command_loader import CommandLoader


class CommandLoaderBot(Client):
    """
    Hello Bot made to interact on Discord
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
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!"):
            content_split = message.content[1:].split(" ")
            command_name = content_split[0]
            args = content_split[1:]
            await message.reply(self.__command_loader.perform_command(command_name, args), mention_author=True)
