from constants.messages import (NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, 
  NAUGHTY_INCORRECT, CREATURE_SPAWN_DESCRIPTION)
from dtos.creature import CreatureDto
from dtos.item import ItemDto
import discord
from constants.globals import ChristmasColor

def format_inventory(inventory: [ItemDto]):
  formatted_string = '\n'
  for item in inventory:
    add_to_formatted_string = item.display_name + '\n'
    formatted_string = formatted_string+add_to_formatted_string
  if len(inventory) == 0:
    formatted_string = '\nWait... You have nothing? That\'s so pathe-- I mean, sad...'
  return discord.Embed(title='Wow! Look at all your items:',
                       description=formatted_string,
                       color=discord.Colour(ChristmasColor.GOLD))