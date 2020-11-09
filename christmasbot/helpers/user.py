from constants.messages import (NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, 
  NAUGHTY_INCORRECT, CREATURE_SPAWN_DESCRIPTION)
from dtos.creature import CreatureDto
from dtos.item import ItemDto



def format_inventory(inventory: list[ItemDto]):
  if inventory == []:
    return 'You\'re penniless...'
  formatted_string = 'Wow! Look at all your items:\n'
  for item in inventory:
    add_to_formatted_string = item.display_name + '\n'
    formatted_string = formatted_string+add_to_formatted_string
  return formatted_string
