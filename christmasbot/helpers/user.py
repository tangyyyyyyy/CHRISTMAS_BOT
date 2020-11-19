import discord

from dtos.item import ItemDto
from constants.globals import ChristmasColor
from dtos.player import PlayerDto


def format_inventory(inventory: list[ItemDto]):
  formatted_string = '\n'
  for item in inventory:
    add_to_formatted_string = item.display_name + '\n'
    formatted_string = formatted_string+add_to_formatted_string
  if len(inventory) == 0:
    formatted_string = '\nWait... You have nothing? That\'s so pathe-- I mean, sad...'
  return discord.Embed(title='Wow! Look at all your items:',
                       description=formatted_string,
                       color=discord.Colour(ChristmasColor.GOLD))

def format_leaderboard(leaderboard: list[tuple[str, PlayerDto]]):
  formatted_string = '```\nRank | Score | Coal | User\n======================================\n'
  if len(leaderboard) == 0:
    formatted_string = '```yaml\nWait... No one has got any items? Are you even trying? ' \
                        'Why\'d you even add me to this server?? Does my time and memory ' \
                        'mean nothing to you??? Well, thanks for nothing...'
  else:
    for rank, player_tuple in enumerate(leaderboard):
      player_name = player_tuple[0]
      player_dto = player_tuple[1]
      add_to_formatted_string = "{0:4.0f} | {1:5.0f} | {2:4.0f} | {3}\n".format(rank + 1, player_dto.score, player_dto.coal_count, player_name)
      formatted_string = formatted_string + add_to_formatted_string
      if rank >= 5:
          break
    formatted_string = formatted_string + '\n``` \n ```yaml\n' \
                                          'Not bad for a bunch of discount Santas! ' \
                                          'As for the rest of you... ' \
                                          'Well, cheer up, I\'m sure there ' \
                                          'is something you\'re good at!'

  return discord.Embed(title='Our top 5 gift hustlers are...',
                      description=formatted_string + '```\n',
                      color=discord.Colour(ChristmasColor.GOLD))


async def get_player_name(player: PlayerDto, bot):
  user = await bot.fetch_user(player.player_id)
  return '{}#{}'.format(user.name, user.discriminator)
