from constants.messages import HELP_MESSAGE
from daos.abstract_dao import AbstractDao

def handle_help(message, dao: AbstractDao, tokens: list[str]):
  return HELP_MESSAGE

def handle_inventory(message, dao: AbstractDao, tokens: list[str]):
  return 'inventory placeholder'

def handle_leaderboard(message, dao: AbstractDao, tokens: list[str]):
  return 'leaderboard placeholder'

def handle_tree(message, dao: AbstractDao, tokens: list[str]):
  return 'tree placeholder'


USER_COMMAND_LIST = {
  'x!help': handle_help,
  'x!inventory': handle_inventory,
  'x!leaderboard': handle_leaderboard,
  'x!tree': handle_tree
}
