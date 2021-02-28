"""
Module containing the Hello Bot made to interact on Discord.
"""

import os
import yaml

from importlib import util as importlibutil
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

    def load_yaml_commands(self, yaml_commands_directory: str) -> None:
        """
        Given a commands directory, load up all commands specified in the yaml files.
        :param yaml_commands_directory: Directory storing the yaml files specifying the commands.
        """
        self.__logger.info(f"Loading commands from {yaml_commands_directory}...")
        if not os.path.exists(yaml_commands_directory):
            self.__logger.warning(f"Commands directory '{yaml_commands_directory}' doesn't exist.")
            return

        for file_name in os.listdir(yaml_commands_directory):
            if not file_name.endswith(".yaml"):
                continue

            yaml_file_path = os.path.join(yaml_commands_directory, file_name)
            with open(yaml_file_path) as yaml_file:
                # Empty yaml returns as None, so make sure to return as at least an empty dictionary.
                config_from_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
                self.__logger.info(f"Loaded configuration file {yaml_commands_directory}.")
                for command in config_from_yaml["commands"]:
                    command_name = command["name"]
                    if command_name in self.__commands:
                        self.__logger.warning(f"Command '{command_name}' already exists. Crashing the bot...")
                    self.__load_string_command(command_name, command["help"], command["return"])
        self.__logger.info(f"Commands loaded from {yaml_commands_directory}.")

    def __load_string_command(self, command_name: str, command_help: str, return_string: str):
        self.__commands[command_name] = StringCommand(command_name, command_help, return_string)

    def load_python_commands(self, python_commands_directory: str) -> None:
        """
        Given a commands directory, load up all commands specified in the py files. The python modules must have an
        attribute `COMMAND` define which is of type BasicCommand.
        :param python_commands_directory: Directory storing the yaml files specifying the commands.
        """
        self.__logger.info(f"Loading commands from {python_commands_directory}...")
        if not os.path.exists(python_commands_directory):
            self.__logger.warning(f"Commands directory '{python_commands_directory}' doesn't exist.")
            return

        for file_name in os.listdir(python_commands_directory):
            if not file_name.endswith(".py"):
                continue

            # Taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
            file_path = os.path.join(python_commands_directory, file_name)
            module_name = file_name.replace(".py", "")
            self.__logger.info(f"Loading commands file {file_path}...")

            spec = importlibutil.spec_from_file_location(module_name, file_path)
            module = importlibutil.module_from_spec(spec)
            spec.loader.exec_module(module)
            command: BasicCommand = module.COMMAND
            self.__commands[command.name] = command
            self.__logger.info(f"Commands file {file_path} loaded as '!{command.name}'")

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
