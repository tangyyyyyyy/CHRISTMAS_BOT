from helpers import response_formatter
from classes import Creature, Item

def handle_nice(message, tokens):
  creature = Creature('Jeff Bezos', 'he', None, None, 'nice')
  item = Item('extended AWS free trial', None, None, 'common')
  return response_formatter.format_correct_command(creature, item)

def handle_naughty(message, tokens):
  creature = Creature('tangy', 'he', None, None, 'naughty')
  item = Item('bug in your code', None, None, 'rare')
  return response_formatter.format_correct_command(creature, item)

def handle_spawn_chance(message, tokens):
  # not implemented yet as we don't want the bot spamming anything
  return ''


SPAWN_COMMAND_LIST = {
  'x!nice': handle_nice,
  'x!naughty': handle_naughty
}
