from constants.messages import BAD_COMMAND_MESSAGE
from daos.abstract_dao import AbstractDao

def handle_enable_channel(message, dao: AbstractDao, tokens: list[str]):
  if len(tokens) > 1:
    return BAD_COMMAND_MESSAGE
  if dao.enable_channel(message.guild.id, message.channel.id) == None:
    return 'I\'m already enabled on this channel!'
  else:
    print('Enabled channel')
    return 'ChristmasBot is now enabled on this channel!'
  

def handle_disable_channel(message, dao: AbstractDao, tokens: list[str]):
  if len(tokens) > 1:
    return BAD_COMMAND_MESSAGE
  if dao.disable_channel(message.guild.id, message.channel.id) == None:
    return 'I\'m already disabled on this channel!'
  else:
    print('Disabled channel')
    return 'ChristmasBot is now disabled on this channel!'

def handle_change_despawn_time(message, dao, tokens):
  return 'Change despawn time placeholder'

def handle_change_spawn_rate(message, dao: AbstractDao, tokens: list[str]):
  if len(tokens) > 2:
    return BAD_COMMAND_MESSAGE
  try:
    new_spawn_rate = int(tokens[1])
  except ValueError as e:
    return BAD_COMMAND_MESSAGE
  if dao.change_spawn_rate(message.guild.id, new_spawn_rate) == None:
    return 
  print('Spawn rate changed to {}'.format(new_spawn_rate))
  return 'I changed the spawn rate to {}%!'.format(new_spawn_rate)

def handle_refresh_role(message, dao: AbstractDao, tokens: list[str]):
  return 'Refresh role placeholder'


ADMIN_COMMAND_LIST = {
  'x!enable': handle_enable_channel,
  'x!disable': handle_disable_channel,
  'x!time': handle_change_despawn_time,
  'x!role': handle_refresh_role,
  'x!setchance': handle_change_spawn_rate
}
