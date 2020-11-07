from constants.messages import (NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, 
  NAUGHTY_INCORRECT, CREATURE_SPAWN_DESCRIPTION)
from dtos.creature import CreatureDto
from dtos.item import ItemDto

def get_item_pronoun(item):
  if item.display_name[0] in 'AEIOUaeiou':
    return 'an'
  else:
    return 'a'

def get_correct_command(creature: CreatureDto):
  if creature.status != 'nice' and creature.status != 'naughty':
    raise Exception('Creature was neither nice nor naughty! It was {}'.format(creature.status))
  return 'x!{}'.format(creature.status)

#creature_name, creature_pronoun, item_pronoun, item_name, item_rarity, creature_name
#creature_name, caps_creature_pronoun, creature_pronoun, item_pronoun, item_name, item_rarity
#creature_name, caps_creature_pronoun, creature_pronoun, replaced_item
#creature_name, caps_creature_pronoun, creature_pronoun, replaced_item


def format_correct_naughty_response(creature: CreatureDto, item: ItemDto):
  return NAUGHTY_CORRECT.format(creature_name=creature.display_name,
    creature_pronoun=creature.pronoun, item_pronoun=get_item_pronoun(item), 
    item_name=item.display_name, item_rarity=item.rarity)


def format_correct_nice_response(creature: CreatureDto, item: ItemDto):
  return NICE_CORRECT.format(creature_name=creature.display_name,
    caps_creature_pronoun=creature.pronoun.capitalize(), creature_pronoun=creature.pronoun,
    item_pronoun=get_item_pronoun(item),
    item_name=item.display_name, item_rarity=item.rarity)


def format_incorrect_naughty_response(creature: CreatureDto, item: ItemDto):
  return NICE_INCORRECT.format(creature_name=creature.display_name,
    caps_creature_pronoun=creature.pronoun.capitalize(), creature_pronoun=creature.pronoun,
    replaced_item=item.display_name)


def format_incorrect_nice_response(creature: CreatureDto, item: ItemDto):
  return NAUGHTY_INCORRECT.format(creature_name=creature.display_name,
    caps_creature_pronoun=creature.pronoun.capitalize(), creature_pronoun=creature.pronoun,
    replaced_item=item.display_name)


def format_spawn_description(creature: CreatureDto):
  return CREATURE_SPAWN_DESCRIPTION.format(creature_command=get_correct_command(creature))

def format_inventory(inventory: [ItemDto]):
  formatted_string = 'Wow! Look at all your items:'
  for item in inventory:
    formatted_string = '\n' + formatted_string + item.display_name
  return formatted_string
