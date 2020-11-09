import random
from os import getcwd
import discord

from constants.globals import ChristmasColor
from constants.messages import CREATURE_SPAWN_TITLE
from daos.abstract_dao import AbstractDao
from dtos.creature import CreatureDto
from dtos.item import ItemDto, ItemRarity
from helpers.response_formatter import (format_correct_nice_response, 
  format_incorrect_nice_response, format_correct_naughty_response,
  format_incorrect_naughty_response, format_spawn_description)


TEST_CREATURES = [ CreatureDto('jeff_bezos', 'Jeff Bezos', 'he', 'https://i.imgur.com/YZ6v1jw.png', 'nice',
  ['extended_aws_trial']), CreatureDto('tangy', 'Tangy', 'he', 'https://i.imgur.com/YZ6v1jw.png', 'naughty', ['bug_in_code'])]


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


def check_if_command_correct(user_message, creature: CreatureDto):
  command = user_message.content
  if creature.status == 'nice':
    return command == 'x!nice'
  elif creature.status == 'naughty':
    return command == 'x!naughty'
  else:
    raise Exception('Creature was neither nice or naughty!')


def get_bot_response(is_correct_reply: bool, creature: CreatureDto, item: ItemDto):
  if creature.status == 'nice':
    if is_correct_reply:
      return format_correct_nice_response(creature, item)
    else:
      return format_incorrect_nice_response(creature, item)
  elif creature.status == 'naughty':
    if is_correct_reply:
      return format_correct_naughty_response(creature, item)
    else:
      return format_incorrect_naughty_response(creature, item)
  else:
    raise Exception('Creature was neither nice or naughty!')
