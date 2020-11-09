from constants.messages import HELP_MESSAGE
from daos.abstract_dao import AbstractDao
from daos.memory_dao import MemoryDao
from helpers.response_formatter import format_inventory


async def handle_help(message, dao: AbstractDao, tokens: list[str]):
  await message.channel.send(embed=HELP_MESSAGE)


async def handle_inventory(message, dao: MemoryDao, tokens: list[str]):
  server_id = message.guild.id
  author_profile = dao.get_player(server_id, message.author.id).inventory
  detailed_inventory = dao.get_items(author_profile)
  if detailed_inventory is None:
    raise Exception('Items in player\'s inventory do not exist!')
  response = format_inventory(detailed_inventory)
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
