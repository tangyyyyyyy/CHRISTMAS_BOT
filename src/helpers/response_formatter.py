from constants.messages import CORRECT_RESPONSE

def get_item_pronoun(item):
  if item.name[0] in 'AEIOUaeiou':
    return 'an'
  else:
    return 'a'

def format_correct_command(creature, item):
  return CORRECT_RESPONSE.format(creature_status=creature.status, 
    creature_name=creature.name, creature_pronoun=creature.pronoun, 
    item_pronoun=get_item_pronoun(item), item_name=item.name, 
    item_rarity=item.rarity)