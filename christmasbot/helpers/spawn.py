import random
from os import getcwd
import discord
from cogs import user

from constants.globals import ChristmasColor
from constants.messages import (CREATURE_SPAWN_TITLE, CREATURE_SPAWN_DESCRIPTION, 
  NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, NAUGHTY_INCORRECT, POST_SPAWN_TITLE)
from daos.abstract_dao import AbstractDao
from dtos.creature import CreatureDto
from dtos.item import ItemDto
from dtos.player import PlayerDto

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


def format_correct_naughty_response(user, creature: CreatureDto, item: ItemDto):
  print('usermention=', user.mention)
  return NAUGHTY_CORRECT.format(creature_name=creature.display_name,
    creature_pronoun=creature.pronoun, item_pronoun=get_item_pronoun(item), 
    item_name=item.display_name, item_rarity=item.rarity, user_mention=user.mention)


def format_correct_nice_response(user, creature: CreatureDto, item: ItemDto):
  return NICE_CORRECT.format(creature_name=creature.display_name,
    caps_creature_pronoun=creature.pronoun.capitalize(), creature_pronoun=creature.pronoun,
    item_pronoun=get_item_pronoun(item),
    item_name=item.display_name, item_rarity=item.rarity, user_mention=user.mention)


def format_incorrect_naughty_response(user, creature: CreatureDto, item: ItemDto):
  return NICE_INCORRECT.format(creature_name=creature.display_name,
    caps_creature_pronoun=creature.pronoun.capitalize(), creature_pronoun=creature.pronoun,
    replaced_item=item.display_name, user_mention=user.mention)


def format_incorrect_nice_response(user, creature: CreatureDto, item: ItemDto):
  return NAUGHTY_INCORRECT.format(creature_name=creature.display_name,
    caps_creature_pronoun=creature.pronoun.capitalize(), creature_pronoun=creature.pronoun,
    replaced_item=item.display_name, user_mention=user.mention)


def format_spawn_description(creature: CreatureDto):
  return CREATURE_SPAWN_DESCRIPTION.format(creature_command=get_correct_command(creature))


def get_random_creature(dao: AbstractDao):
  return dao.get_random_creature()


def get_random_item(dao: AbstractDao, creature: CreatureDto) -> ItemDto:
  item_pool = creature.items
  if item_pool == []:
    raise Exception('There were no items for creature {}!'.format(creature.id))
  item = dao.get_item(random.choice(item_pool))
  if item is None:
    raise Exception('Creature {} has an item that is invalid'.format(creature.id))
  return item


def has_ongoing_spawn(spawn_dict: dict[int, dict[int, CreatureDto]], 
  server_id: int, channel_id: int):
  return server_id in spawn_dict and channel_id in spawn_dict[server_id]


def add_ongoing_spawn(spawn_dict: dict[int, dict[int, CreatureDto]], 
  server_id: int, channel_id: int, creature: CreatureDto):
  if server_id not in spawn_dict:
    spawn_dict[server_id] = {}    
  spawn_dict[server_id][channel_id] = creature


def remove_ongoing_spawn(spawn_dict: dict[int, dict[int, CreatureDto]], 
  server_id: int, channel_id: int):
  spawn_dict[server_id].pop(channel_id)


def create_creature_message(creature: CreatureDto, item: ItemDto):
    print('urls=', creature.img_url, ' ', item.img_url)
    print('current dir=', getcwd())
    return discord.Embed(
      title=CREATURE_SPAWN_TITLE,
      description=format_spawn_description(creature),
      color=discord.Colour(ChristmasColor.GOLD),
    ).set_image(
      url=creature.img_url
    )


def create_post_spawn_message(creature: CreatureDto, message: str):
  return discord.Embed(
    title=POST_SPAWN_TITLE,
    description=message,
    color=discord.Colour(ChristmasColor.GOLD),
  ).set_image(
    url=creature.img_url
  )

def check_if_command_correct(user_message, creature: CreatureDto):
  command = user_message.content
  if creature.status == 'nice':
    return command == 'x!nice'
  elif creature.status == 'naughty':
    return command == 'x!naughty'
  else:
    raise Exception('Creature was neither nice or naughty!')


def get_bot_response(user, is_correct_reply: bool, dao: AbstractDao, user_message, creature: CreatureDto, item: ItemDto):
  server_id = user_message.guild.id
  player_id = user_message.author.id
  
  if is_correct_reply:
    if item in dao.get_player(server_id, player_id).inventory:
      return 'You already had that item :('
    else:
      #give player the item
      dao.add_item_to_player(server_id, player_id, item.id)
      if creature.status == 'nice':
        return format_correct_nice_response(user, creature, item)
      elif creature.status == 'naughty':
        return format_correct_naughty_response(user, creature, item)
      else:
        raise Exception('Creature was neither nice or naughty!')
  else:
    # replace it with coal if you have an item
    popped_item = dao.replace_player_item_with_coal(server_id, player_id)
    if popped_item is not None:      
      if creature.status == 'nice': 
          return format_incorrect_nice_response(user, creature, item)
      elif creature.status == 'naughty':
          return format_incorrect_naughty_response(user, creature, item)
      else:
        raise Exception('Creature was neither nice or naughty!')
    else:
      return 'Wrong! {} tried to replace one of your items with coal, but your inventory is empty. ' \
                      'Maybe coal isn\'t so bad after all...'.format(creature.display_name) 



