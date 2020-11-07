from helpers import response_formatter
from daos.abstract_dao import AbstractDao
from helpers.spawn import get_item, get_naughty_creature, get_nice_creature

def handle_nice(message, dao: AbstractDao, tokens: list[str]):
  creature = get_nice_creature()
  item = get_item(creature)
  if creature.status == 'nice':
    return response_formatter.format_correct_nice_response(creature, item)
  else:
    return response_formatter.format_incorrect_naughty_response(creature, item)

def handle_naughty(message, dao: AbstractDao, tokens: list[str]):
  creature = get_naughty_creature()
  item = get_item(creature)
  if creature.status == 'naughty':
    return response_formatter.format_correct_naughty_response(creature, item)
  else:
    return response_formatter.format_incorrect_nice_response(creature, item)

def handle_spawn_chance(message, dao: AbstractDao, tokens: list[str]):
  # not implemented yet as we don't want the bot spamming anything
  return 'Spawn placeholder'


SPAWN_COMMAND_LIST = {
  'x!nice': handle_nice,
  'x!naughty': handle_naughty
}
