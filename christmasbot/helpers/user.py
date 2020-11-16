import discord

from constants.messages import (NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, 
  NAUGHTY_INCORRECT, CREATURE_SPAWN_DESCRIPTION)
from dtos.creature import CreatureDto
from dtos.item import ItemDto
from constants.globals import ChristmasColor


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

def format_leaderboard(leader_board: dict):
    formatted_string = '```\nRank | Items | User\n======================================\n'
    leaderboard_sorted_keys = sorted(leader_board, key=leader_board.get, reverse=True)
    if len(leader_board) == 0:
        formatted_string = '```yaml\nWait... No one has got any items? Are you even trying? ' \
                           'Why\'d you even add me to this server?? Does my time and memory ' \
                           'mean nothing to you??? Well, thanks for nothing...'
    else:
        for rank, player in enumerate(leaderboard_sorted_keys):
                add_to_formatted_string = "{0:4.0f} | {1:5.0f} | {2}\n".format(rank+1, leader_board[player], player)
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
