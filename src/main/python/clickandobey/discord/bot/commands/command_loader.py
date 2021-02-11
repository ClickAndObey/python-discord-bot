"""
Module containing the Hello Bot made to interact on Discord.
"""

import os
import yaml

from logging import Logger
from typing import Dict, List

from clickandobey.discord.bot.commands.basic_command import BasicCommand
from clickandobey.discord.bot.commands.function_command import FunctionCommand
from clickandobey.discord.bot.commands.string_command import StringCommand


class CommandLoader:
    """
    Hello Bot made to interact on Discord
    """

    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__commands: Dict[str, BasicCommand] = {
            "commands": FunctionCommand(
                "commands",
                "Use this to look at all available commands from this bot.",
                self.__get_commands
            )
        }

    # Setup for the Class

    def load_commands(self, yaml_file_directory: str) -> None:
        """
        Given a yaml file, load up all commands. A command has a name and a return, where the return can be a "string"
        or a "method". If it is a method, an import will be done of the module specified.
        :param yaml_file_directory: Directory storing the yaml files specifying the commands.
        """
        self.__logger.info(f"Loading commands from {yaml_file_directory}...")
        if not os.path.exists(yaml_file_directory):
            self.__logger.warning(f"Commands file '{yaml_file_directory}' doesn't exist.")
            return

        for file_name in os.listdir(yaml_file_directory):
            if not file_name.endswith(".yaml"):
                continue

            yaml_file_path = os.path.join(yaml_file_directory, file_name)
            with open(yaml_file_path) as yaml_file:
                # Empty yaml returns as None, so make sure to return as at least an empty dictionary.
                config_from_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
                self.__logger.info(f"Loaded configuration file {yaml_file_directory}.")
                for command in config_from_yaml["commands"]:
                    command_name = command["name"]
                    if command_name in self.__commands:
                        self.__logger.warning(f"Command '{command_name}' already exists. Crashing the bot...")
                    self.__load_string_command(command_name, command["help"], command["return"])
        self.__logger.info(f"Commands loaded from {yaml_file_directory}.")

    def __load_string_command(self, command_name: str, command_help: str, return_string: str):
        self.__commands[command_name] = StringCommand(command_name, command_help, return_string)

    def perform_command(self, command_name: str, args: List[str]) -> str:
        """
        Given a command to perform, run the command and return its string output.
        """
        if command_name not in self.__commands:
            return "Unknown Command! Type !commands for a full list of available commands."

        return self.__commands[command_name].perform(args)

    # pylint: disable=unused-argument
    def __get_commands(self, args: List[str]) -> str:
        return_string = ""
        for command in self.__commands.values():
            return_string += f"{command.usage()}\n"
        return_string = return_string.strip()
        return return_string

    def log_usage(self):
        """
        Log the available commands.
        """
        self.__logger.info(f"Commands found: \n{self.perform_command('commands', [])}")
