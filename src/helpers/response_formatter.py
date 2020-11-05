from constants.messages import NICE_CORRECT, NAUGHTY_CORRECT

def get_item_pronoun(item):
  if item.name[0] in 'AEIOUaeiou':
    return 'an'
  else:
    return 'a'

def format_correct_nice_response(creature, item):
  return NICE_CORRECT.format(creature_name=creature.name, 
    creature_pronoun=creature.pronoun, item_pronoun=get_item_pronoun(item), 
    item_name=item.name, item_rarity=item.rarity)

def format_correct_naughty_response(creature, item):
  return NAUGHTY_CORRECT.format(creature_name=creature.name, 
    creature_pronoun=creature.pronoun, item_pronoun=get_item_pronoun(item), 
    item_name=item.name, item_rarity=item.rarity)