"""
Module used to define the operation to perform when a command is called.
"""

from typing import Callable, List

from clickandobey.discord.bot.commands.basic_command import BasicCommand


class FunctionCommand(BasicCommand):
    """
    Class representing a function command to be run.
    """

    def __init__(self, name: str, help_string: str, function: Callable[[List[str]], str]):
        super().__init__(name, help_string)
        self.__function = function

    def perform(self, args: List[str]) -> str:
        """
        Perform the command via the string it was initialized with.
        """
        return self.__function(args)
