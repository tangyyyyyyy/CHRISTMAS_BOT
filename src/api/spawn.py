from helpers import response_formatter
from daos.abstract_dao import AbstractDao
from dtos.creature import CreatureDto
from dtos.item import  ItemDto

def handle_nice(message, dao: AbstractDao, tokens: list[str]):
  creature = CreatureDto('Jeff Bezos', 'he', 'None', 'None', 'naughty')
  item = ItemDto('extended AWS free trial', 'None', 'None', 'common')
  if creature.status == 'nice':
    return response_formatter.format_correct_nice_response(creature, item)
  else:
    return response_formatter.format_incorrect_naughty_response(creature, item)

def handle_naughty(message, dao: AbstractDao, tokens: list[str]):
  creature = CreatureDto('Tangy', 'he', 'None', 'None', 'nice')
  item = ItemDto('bug in your code', 'None', 'None', 'rare')
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
