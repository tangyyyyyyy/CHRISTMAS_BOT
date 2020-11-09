import asyncio
import random
import os

import discord
from discord.ext import commands

from daos.memory_dao import MemoryDao
from constants.globals import DISCORD_TOKEN
from dtos.player import PlayerDto
from helpers.spawn import (check_if_command_correct, get_bot_response, get_random_creature, get_random_item,
  add_ongoing_spawn, has_ongoing_spawn, remove_ongoing_spawn, create_creature_message, create_post_spawn_message)

client = commands.Bot(command_prefix = 'x!')
client.remove_command('help')

@client.event
async def on_ready():
  self.dao = MemoryDao()
  # ongoing_spawns is used to make sure spawns happen 1 at a time in a channel
  self.ongoing_spawns = {}
  self.player_dict = {}
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('with Santa'))
  print('Christmas Bot is up! Let the festivities begin')

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')

@client.listen('on_message')
async def on_message(ctx):
  if ctx.author == client.user:
     print('Received message is from Christmas Bot... skipping')
     return

  server_id = ctx.guild.id
  channel_id = ctx.channel.id
  
  server_config = client.dao.get_server(server_id)
  if ((channel_id in server_config.enabled_channels) and
    (not has_ongoing_spawn(client.ongoing_spawns, server_id, channel_id))):
     # channel where message is in has enabled spawns, calculate chance %
    roll = random.randint(0, 100)
    if roll <= server_config.spawn_rate_percent:
      # roll was successful, respond with spawn message
      print('Spawning creature...')
      creature = get_random_creature(ctx.dao)
      item = get_random_item(ctx.dao, creature)
      # lock spawn so 2 spawns don't happen at the same time
      add_ongoing_spawn(ctx.ongoing_spawns, server_id, channel_id, creature)
      bot_message = await ctx.channel.send(embed=create_creature_message(creature, item))

      def message_is_nice_or_naughty(message):
        return (ctx.guild.id == server_id and ctx.channel.id == channel_id
          and (ctx.content == 'x!nice' or ctx.content == 'x!naughty'))
        
      try:
        reply = await ctx.wait_for('message', 
          check=message_is_nice_or_naughty, 
          timeout=server_config.despawn_time
        )

        is_correct_reply = check_if_command_correct(reply, creature)
        bot_response = get_bot_response(ctx.author, is_correct_reply, ctx.dao, reply, creature, item)
        await reply.delete(delay=0.5)
      except asyncio.TimeoutError:
        bot_response = 'The creature left because you kept it waiting for too long!'
      finally:
        remove_ongoing_spawn(ctx.ongoing_spawns, server_id, channel_id)
        await bot_message.edit(embed=create_post_spawn_message(creature,bot_response))


for filename in os.listdir('./cogs'):
    if (filename.endswith('.py')) and (filename!='__init__.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(DISCORD_TOKEN)
