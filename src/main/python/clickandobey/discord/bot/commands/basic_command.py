"""
Module used to define the operation to perform when a command is called.
"""

from typing import List


class BasicCommand:
    """
    Class representing a string command to be run.
    """

    def __init__(self, name: str, help_string: str):
        self.__name = name
        self.__help_string = help_string

    def usage(self) -> str:
        """
        Return the help string for the command.
        """
        return f"!{self.__name}: {self.__help_string}"

    def perform(self, args: List[str]) -> str:
        """
        Perform the command via the string it was initialized with.
        """
        raise NotImplementedError()
