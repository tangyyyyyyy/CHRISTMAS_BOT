from constants.messages import HELP_MESSAGE
from daos import get_dao
from helpers.user import format_inventory


async def handle_help(message, tokens: list[str]):
  await message.channel.send(embed=HELP_MESSAGE)


async def handle_inventory(message, tokens: list[str]):
  dao = get_dao()
  server_id = message.guild.id
  author_profile = await dao.get_player(server_id, message.author.id)
  detailed_inventory = await dao.get_items(author_profile.inventory)
  if detailed_inventory is None:
    raise Exception('Items in player\'s inventory do not exist!')
  response = format_inventory(detailed_inventory)
  await message.channel.send(embed=response)


async def handle_leaderboard(message, tokens: list[str]):
  response = 'leaderboard placeholder'
  await message.channel.send(response) 


async def handle_tree(message, tokens: list[str]):
  response = 'tree placeholder'
  await message.channel.send(response) 

USER_COMMAND_LIST = {
  'x!help': handle_help,
  'x!inventory': handle_inventory,
  'x!leaderboard': handle_leaderboard,
  'x!tree': handle_tree
}
