import random

import discord

from constants.globals import ChristmasColor
from constants.messages import CREATURE_SPAWN_TITLE
from dtos.creature import CreatureDto
from dtos.item import ItemDto, ItemRarity
from helpers.response_formatter import (format_correct_nice_response, 
  format_incorrect_nice_response, format_correct_naughty_response,
  format_incorrect_naughty_response, format_spawn_description)


TEST_CREATURES = [ CreatureDto('jeff_bezos', 'Jeff Bezos', 'he', 'https://i.imgur.com/YZ6v1jw.png', 'nice', 
  ['extended_aws_trial']), CreatureDto('tangy', 'Tangy', 'he', 'https://i.imgur.com/YZ6v1jw.png', 'naughty', ['bug_in_code'])]


def get_creature():
  return random.choice(TEST_CREATURES)


def get_item(creature: CreatureDto):
  if creature.id == 'jeff_bezos':
    return ItemDto('extended_trial', 'extended AWS free trial', 'None', ItemRarity.COMMON)
  elif creature.id == 'tangy':
    return ItemDto('bug', 'bug in your code', 'None', ItemRarity.COMMON)
  else:
    raise Exception('creature responding was not tangy or jeff bezos, it was ' + str(creature.id))



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


def create_creature_message(creature: CreatureDto):
    return discord.Embed(
      title=CREATURE_SPAWN_TITLE,
      description=format_spawn_description(creature),
      color=discord.Colour(ChristmasColor.GOLD),
    ).set_author(
      name='Christmas Bot',
      icon_url='https://i.imgur.com/YZ6v1jw.png',
      url='https://github.com/tangyyyyyyy/CHRISTMAS_BOT'
    ).set_image(
      url=creature.img_url
    )


def check_if_command_correct(creature: CreatureDto, user_message):
  command = user_message.content
  if creature.status == 'nice':
    if command == 'x!nice':
      response = format_correct_nice_response(creature, get_item(creature))
    else:
      response = format_incorrect_nice_response(creature, get_item(creature))
    return response
  elif creature.status == 'naughty':
    if command == 'x!naughty':
      response = format_correct_naughty_response(creature, get_item(creature))
    else:
      response = format_incorrect_naughty_response(creature, get_item(creature))
    return response
  else:
    raise Exception('Creature was neither nice or naughty!')

