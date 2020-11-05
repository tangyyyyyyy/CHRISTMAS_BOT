from constants.messages import NAUGHTY_CORRECT

def get_item_pronoun(item):
  if item.name[0] in 'AEIOUaeiou':
    return 'an'
  else:
    return 'a'

def format_naughty_correct(creature, item):
  return NAUGHTY_CORRECT.format(creature_name=creature.name, 
    creature_pronoun=creature.pronoun, item_pronoun=get_item_pronoun(item), 
    item_name=item.name, item_rarity=item.rarity)