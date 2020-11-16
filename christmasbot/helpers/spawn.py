from os import getcwd
import random

import discord
from discord.colour import Colour

from constants.globals import ChristmasColor, get_ongoing_spawns
from constants.messages import (CREATURE_IDENTIFIED_TITLE, CREATURE_MISIDENTIFIED_TITLE, CREATURE_SPAWN_TITLE, CREATURE_SPAWN_DESCRIPTION, CREATURE_TIMEOUT_DESCRIPTION, CREATURE_TIMEOUT_TITLE, 
  NICE_CORRECT, NAUGHTY_CORRECT, NICE_INCORRECT, NAUGHTY_INCORRECT)
from daos import get_dao
from daos.abstract_dao import AbstractDao
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


async def get_random_creature():
  dao = get_dao()
  return await dao.get_random_creature()


async def get_random_item(creature: CreatureDto) -> ItemDto:
  dao = get_dao()
  item_pool = creature.items
  if item_pool == []:
    raise Exception('There were no items for creature {}!'.format(creature.id))
  item = await dao.get_item(random.choice(item_pool))
  if item is None:
    raise Exception('Creature {} has an item that is invalid'.format(creature.id))
  return item


def has_ongoing_spawn(server_id: int, channel_id: int):
  spawn_dict = get_ongoing_spawns()
  return server_id in spawn_dict and channel_id in spawn_dict[server_id]


def add_ongoing_spawn(server_id: int, channel_id: int, creature: CreatureDto):
  spawn_dict = get_ongoing_spawns()
  if server_id not in spawn_dict:
    spawn_dict[server_id] = {}    
  spawn_dict[server_id][channel_id] = creature


def remove_ongoing_spawn(server_id: int, channel_id: int):
  spawn_dict = get_ongoing_spawns()
  spawn_dict[server_id].pop(channel_id)


def create_creature_message(creature: CreatureDto):
    print('current dir=', getcwd())
    return discord.Embed(
      title=CREATURE_SPAWN_TITLE,
      description=format_spawn_description(creature),
      color=discord.Colour(ChristmasColor.GOLD),
    ).set_image(
      url=creature.img_url
    )


def create_timeout_message(creature: CreatureDto):
  return discord.Embed(
    title=CREATURE_TIMEOUT_TITLE,
    description=CREATURE_TIMEOUT_DESCRIPTION,
    color=discord.Colour(ChristmasColor.RED),
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


async def create_bot_response(is_correct_reply: bool, user_message, creature: CreatureDto):
  server_id = user_message.guild.id
  player_id = user_message.author.id
  dao = get_dao()
  
  if is_correct_reply:
    title = CREATURE_IDENTIFIED_TITLE
    color = ChristmasColor.GREEN
    item = await get_random_item(creature)

    player = await dao.get_player(server_id, player_id)
    if item.id in player.inventory:
      description = 'You already had that item :('
    else:
      #give player the item
      await dao.add_item_to_player(server_id, player_id, item.id)
      if creature.status == 'nice':
        description = format_correct_nice_response(creature, item)
      elif creature.status == 'naughty':
        description = format_correct_naughty_response(creature, item)
      else:
        raise Exception('Creature was neither nice or naughty!')
  else:
    title = CREATURE_MISIDENTIFIED_TITLE
    color = ChristmasColor.RED
    # replace it with coal if you have an item
    popped_item_id = await dao.replace_player_item_with_coal(server_id, player_id)
    if popped_item_id is not None:      
      item = await dao.get_item(popped_item_id)
      if creature.status == 'nice': 
          description = format_incorrect_nice_response(creature, item)
      elif creature.status == 'naughty':
          description = format_incorrect_naughty_response(creature, item)
      else:
        raise Exception('Creature was neither nice or naughty!')
    else:
      description = '{} tried to replace one of your items with coal, but your inventory is empty. ' \
                      'Maybe coal isn\'t so bad after all...'.format(creature.display_name) 
  return discord.Embed(
    title=title,
    description=description,
    color=discord.Colour(color)
  ).set_image(
    url=creature.img_url
  )



