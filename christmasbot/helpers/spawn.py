from dtos.creature import CreatureDto
from dtos.item import ItemDto, ItemRarity

def get_nice_creature():
  return CreatureDto('jeff_bezos', 'Jeff Bezos', 'he', 'https://i.imgur.com/YZ6v1jw.png', 'nice', 
  ['extended_aws_trial'])

def get_naughty_creature():
  return CreatureDto('tangy', 'Tangy', 'he', 'https://i.imgur.com/YZ6v1jw.png', 'naughty', ['bug_in_code'])

def get_item(creature: CreatureDto):
  if creature.id == 'jeff_bezos':
    return ItemDto('extended_trial', 'extended AWS free trial', 'None', ItemRarity.COMMON)
  elif creature.id == 'tangy':
    return ItemDto('bug', 'bug in your code', 'None', ItemRarity.COMMON)
  else:
    raise Exception('creature responding was not tangy or jeff bezos, it was ' + str(creature.id))
