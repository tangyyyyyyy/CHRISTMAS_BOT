from helpers import response_formatter
from daos.abstract_dao import AbstractDao
from helpers.spawn import get_item, get_naughty_creature, get_nice_creature


async def handle_nice(message, dao: AbstractDao, tokens: list[str]):
  creature = get_nice_creature()
  item = get_item(creature)
  if creature.status == 'nice':
    response = response_formatter.format_correct_nice_response(creature, item)
  else:
    response = response_formatter.format_incorrect_naughty_response(creature, item)
  await message.channel.send(response) 


async def handle_naughty(message, dao: AbstractDao, tokens: list[str]):
  creature = get_naughty_creature()
  item = get_item(creature)
  if creature.status == 'naughty':
    response = response_formatter.format_correct_naughty_response(creature, item)
  else:
    response = response_formatter.format_incorrect_nice_response(creature, item)
  await message.channel.send(response) 


async def handle_spawn_chance(message, dao: AbstractDao, tokens: list[str]):
  # not implemented yet as we don't want the bot spamming anything
  response = 'Spawn placeholder'
  await message.channel.send(response) 


SPAWN_COMMAND_LIST = {
  'x!nice': handle_nice,
  'x!naughty': handle_naughty
}
