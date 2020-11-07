from constants.messages import HELP_MESSAGE
from daos.abstract_dao import AbstractDao
from daos.memory_dao import MemoryDao
from helpers.response_formatter import format_inventory


async def handle_help(message, dao: AbstractDao, tokens: list[str]):
  await message.channel.send(embed=HELP_MESSAGE)


async def handle_inventory(message, dao: MemoryDao, tokens: list[str]):
  print('dao', dao)
  server_id = message.guild.id
  try:
    response = format_inventory(dao.server_players[server_id][message.author].inventory)
    #format(response)
  except KeyError:
    #author doesn't have inventory
    response = 'You\'re penniless...'
  await message.channel.send(response)


async def handle_leaderboard(message, dao: AbstractDao, tokens: list[str]):
  response = 'leaderboard placeholder'
  await message.channel.send(response) 


async def handle_tree(message, dao: AbstractDao, tokens: list[str]):
  response = 'tree placeholder'
  await message.channel.send(response) 

USER_COMMAND_LIST = {
  'x!help': handle_help,
  'x!inventory': handle_inventory,
  'x!leaderboard': handle_leaderboard,
  'x!tree': handle_tree
}
