"""
Module used to define the operation to perform when a command is called.
"""

from typing import List

from clickandobey.discord.bot.commands.basic_command import BasicCommand


class StringCommand(BasicCommand):
    """
    Class representing a string command to be run.
    """

    def __init__(self, name: str, help_string: str, return_string: str):
        super().__init__(name, help_string)
        self.__return_string = return_string

    # pylint: disable=unused-argument
    def perform(self, args: List[str]) -> str:
        """
        Perform the command via the string it was initialized with.
        """
        return self.__return_string
