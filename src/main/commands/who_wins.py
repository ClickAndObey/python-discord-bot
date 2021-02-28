"""
Command used to determine a winner between multiple "competitors". Takes an unlimited list of competitors and decides
who wins by randomly selecting one of them.
"""

import random
from typing import List

from clickandobey.discord.bot.commands.function_command import FunctionCommand


def __who_wins_function(args: List[str]) -> str:
    """
    Randomly select a "winner" from the given list.
    """
    return random.choice(args)


COMMAND = FunctionCommand(
    "WhoWins",
    "Function to pick a winner from a group.",
    __who_wins_function
)
