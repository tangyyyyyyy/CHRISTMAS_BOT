from constants.messages import BAD_COMMAND_MESSAGE
from daos.abstract_dao import AbstractDao


async def handle_enable_channel(message, dao: AbstractDao, tokens: list[str]):
  if len(tokens) > 1:
    return BAD_COMMAND_MESSAGE
  if dao.enable_channel(message.guild.id, message.channel.id) == None:
    response = 'I\'m already enabled on this channel!'
  else:
    print('Enabled channel')
    response = 'ChristmasBot is now enabled on this channel!'
  await message.channel.send(response) 
  

async def handle_disable_channel(message, dao: AbstractDao, tokens: list[str]):
  if len(tokens) > 1:
    return BAD_COMMAND_MESSAGE
  if dao.disable_channel(message.guild.id, message.channel.id) == None:
    response = 'I\'m already disabled on this channel!'
  else:
    print('Disabled channel')
    response = 'ChristmasBot is now disabled on this channel!'
  await message.channel.send(response) 


async def handle_change_despawn_time(message, dao: AbstractDao, tokens):
  if len(tokens) > 2:
    return BAD_COMMAND_MESSAGE
  new_despawn_time = -1
  try:
    new_despawn_time = int(tokens[1])
  except:
    pass
  if dao.change_despawn_time(message.guild.id, new_despawn_time) == None:
    response = BAD_COMMAND_MESSAGE
  else:
    print('Despawn time changed to {}'.format(new_despawn_time))
    response = 'I changed the despawn time to {} seconds!'.format(new_despawn_time)
  await message.channel.send(response) 


async def handle_change_spawn_rate(message, dao: AbstractDao, tokens: list[str]):
  if len(tokens) > 2:
    return BAD_COMMAND_MESSAGE
  new_spawn_rate = -1
  try:
    new_spawn_rate = int(tokens[1])
  except:
    pass
  if dao.change_spawn_rate(message.guild.id, new_spawn_rate) == None:
    response = BAD_COMMAND_MESSAGE
  else:
    print('Spawn rate changed to {}'.format(new_spawn_rate))
    response = 'I changed the spawn rate to {}%!'.format(new_spawn_rate)
  await message.channel.send(response) 


async def handle_refresh_role(message, dao: AbstractDao, tokens: list[str]):
  response = 'Refresh role placeholder'
  await message.channel.send(response) 


ADMIN_COMMAND_LIST = {
  'x!enable': handle_enable_channel,
  'x!disable': handle_disable_channel,
  'x!time': handle_change_despawn_time,
  'x!role': handle_refresh_role,
  'x!setchance': handle_change_spawn_rate
}
