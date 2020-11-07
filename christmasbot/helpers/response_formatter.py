from constants.messages import NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, NAUGHTY_INCORRECT
from dtos.creature import CreatureDto
from dtos.item import ItemDto

def get_item_pronoun(item):
  if item.display_name[0] in 'AEIOUaeiou':
    return 'an'
  else:
    return 'a'

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
