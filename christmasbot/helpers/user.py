from constants.messages import (NAUGHTY_CORRECT, NICE_INCORRECT, 
  NAUGHTY_INCORRECT, CREATURE_SPAWN_DESCRIPTION)
from dtos.creature import CreatureDto
from dtos.item import ItemDto
import discord
from constants.globals import ChristmasColor
from api import user


def empty_inventory(user):
  formatted_string = '\nWait... You have nothing? That\'s so pathe-- I mean, sad...'
  return discord.Embed(
    description='**Wow,** ' + user.mention + 
                '**! Look at all your items:** \n \n'
                'You own' + ' 0 ' + 'common items \n' + formatted_string  + '\n',
    color=discord.Colour(ChristmasColor.GOLD)
).set_footer(
      text='Page x/x | Use the emotes to switch pages/rarity.'
)

def format_inventory(user, inventory: [ItemDto]):
  if len(inventory) == 0:
    return(empty_inventory(user))

  common_list = []
  special_list = []
  rare_list = []
  formatted_string = '\n'
  
  for item in inventory:
    add_to_formatted_string = item.display_name + '\n'
    formatted_string = formatted_string+add_to_formatted_string
    if (item.rarity.name=='COMMON'):
     common_list.append(item.display_name)
    elif (item.rarity.name=='SPECIAL'):
     special_list.append(item.display_name)
    else:
     rare_list.append(item.display_name)

  return discord.Embed(
    description='**Wow,** ' + user.mention + 
                '**! Look at all your items:** \n \n'
                'You own' + ' x ' + 'common items \n' + formatted_string  + '\n',
    color=discord.Colour(ChristmasColor.GOLD)
).set_footer(
      text='Page x/x | Use the emotes to switch pages/rarity.'
)