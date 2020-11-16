import asyncio
import random

import discord

from api.admin import ADMIN_COMMAND_LIST
from api.user import USER_COMMAND_LIST
from constants.globals import DISCORD_TOKEN, BLOB_URL
from daos import get_dao
from helpers.spawn import (check_if_command_correct, create_bot_response, create_timeout_message, get_random_creature, get_random_item,
  add_ongoing_spawn, has_ongoing_spawn, remove_ongoing_spawn, create_creature_message, create_blob_message)

def load_command_list():
  command_list = {}
  command_list.update(ADMIN_COMMAND_LIST)
  command_list.update(USER_COMMAND_LIST)
  
  return command_list

class ChristmasBot(discord.Client):

  async def on_ready(self):
    self.command_list = load_command_list() 
    # ongoing_spawns is used to make sure spawns happen 1 at a time in a channel
    print('Christmas Bot is up! Let the festivities begin!')

  async def on_message(self, message):
    if message.author == self.user:
      print('Received message is from Christmas Bot... skipping')
      return

    tokens = message.content.split(' ')
    command = tokens[0].lower()

    server_id = message.guild.id
    channel_id = message.channel.id
    player_id = message.author.id
    
    response = 'Placeholder message - you shouldn\'t be seeing this'
    if command in self.command_list.keys():
      print('Invoking command {}'.format(command))
      await self.command_list[command](message, tokens, self)
    elif command in ['x!nice', 'x!naughty'] and not has_ongoing_spawn(server_id, channel_id):
      # prevents max from spamming x!nice/naughty
      return
    else:
      # General message - calculate if the bot should respond
      dao = get_dao()
      server_config = await dao.get_server(server_id)
      if ((channel_id in server_config.enabled_channels) and
        (not has_ongoing_spawn(server_id, channel_id))):
        # channel where message is in has enabled spawns, calculate chance %
        roll = random.randint(0, 100)
        if roll <= server_config.spawn_rate_percent:
          # roll was successful, respond with spawn message
          print('Spawning creature...')
          creature = await get_random_creature()
          # lock spawn so 2 spawns don't happen at the same time
          add_ongoing_spawn(server_id, channel_id, creature)
          bot_message = await message.channel.send(embed=create_blob_message(creature))

          def message_is_nice_or_naughty(message):
            return (message.guild.id == server_id and message.channel.id == channel_id
              and (message.content == 'x!nice' or message.content == 'x!naughty'))
          
          try:
            reply = await self.wait_for('message', 
              check=message_is_nice_or_naughty, 
              timeout=server_config.despawn_time
            )

            is_correct_reply = check_if_command_correct(reply, creature)
            bot_response = await create_bot_response(is_correct_reply, reply, creature)
            
            await reply.delete(delay=5)
          except asyncio.TimeoutError:
            bot_response = create_timeout_message()
          finally:
            remove_ongoing_spawn(server_id, channel_id)
            await bot_message.edit(embed=bot_response)


def run():
  client = ChristmasBot()
  client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run()
