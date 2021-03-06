import discord
from constants.messages import ADMIN_DISABLE_RESPONSE, ADMIN_ENABLE_RESPONSE, BAD_COMMAND_MESSAGE, ROLE_REFRESH_RESPONSE
from daos import get_dao
from helpers.admin import format_bad_command_response, format_no_permissions_response, is_user_admin


async def handle_enable_channel(message, tokens: list[str], bot):
  if len(tokens) > 1:
    response = format_bad_command_response(message.author)
  elif not is_user_admin(message.author, message.channel):
    response = format_no_permissions_response(message.author)
  else:
    dao = get_dao()
    print('Enabled channel')
    await dao.enable_channel(message.guild.id, message.channel.id)
    response = ADMIN_ENABLE_RESPONSE
  
  await message.channel.send(embed=response) 
  

async def handle_disable_channel(message, tokens: list[str], bot):
  if len(tokens) > 1:
    response = format_bad_command_response(message.author)
  elif not is_user_admin(message.author, message.channel):
    response = format_no_permissions_response(message.author)
  else:
    dao = get_dao()
    print('Disabled channel')
    await dao.disable_channel(message.guild.id, message.channel.id)
    response = ADMIN_DISABLE_RESPONSE
  
  await message.channel.send(embed=response) 


async def handle_change_despawn_time(message, tokens, bot):
  if len(tokens) > 2:
    return BAD_COMMAND_MESSAGE
  new_despawn_time = -1
  try:
    new_despawn_time = int(tokens[1])
  except:
    pass
  dao = get_dao()
  if await dao.change_despawn_time(message.guild.id, new_despawn_time) == None:
    response = BAD_COMMAND_MESSAGE
  else:
    print('Despawn time changed to {}'.format(new_despawn_time))
    response = 'I changed the despawn time to {} seconds!'.format(new_despawn_time)
  await message.channel.send(response) 


async def handle_change_spawn_rate(message, tokens: list[str], bot):
  if len(tokens) > 2:
    return BAD_COMMAND_MESSAGE
  new_spawn_rate = -1
  try:
    new_spawn_rate = int(tokens[1])
  except:
    pass
  dao = get_dao()
  if await dao.change_spawn_rate(message.guild.id, new_spawn_rate) == None:
    response = BAD_COMMAND_MESSAGE
  else:
    print('Spawn rate changed to {}'.format(new_spawn_rate))
    response = 'I changed the spawn rate to {}%!'.format(new_spawn_rate)
  await message.channel.send(response) 

async def handle_refresh_role(message, tokens: list[str], bot):
  guild = message.guild
  dao = get_dao()

  response = ROLE_REFRESH_RESPONSE

  if discord.utils.get(guild.roles, name='Champion of Christmas'):
    print('Role exists...')
    role = discord.utils.get(guild.roles, name='Champion of Christmas')
  else:
    role = await guild.create_role(reason='Refreshing Champion of Christmas role...', name="Champion of Christmas", hoist=True, mentionable=True)

  champ_id = await dao.get_champion(guild.id, message.author.id)
  print('champ id', champ_id)
  print('message.id', message.author.id)
  champ = await guild.fetch_member(champ_id)

  await champ.add_roles(role)
  await message.channel.send(embed=response)

ADMIN_COMMAND_LIST = {
  'x!enable': handle_enable_channel,
  'x!disable': handle_disable_channel,
  'x!time': handle_change_despawn_time,
  'x!role': handle_refresh_role,
  'x!setchance': handle_change_spawn_rate
}
