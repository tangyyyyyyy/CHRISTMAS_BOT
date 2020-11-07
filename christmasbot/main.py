import asyncio
import random

import discord

from api.admin import ADMIN_COMMAND_LIST
from api.user import USER_COMMAND_LIST
from daos.memory_dao import MemoryDao
from constants.globals import DISCORD_TOKEN
from dtos.player import PlayerDto
from helpers.spawn import (check_if_command_correct, get_creature, get_item,
  add_ongoing_spawn, has_ongoing_spawn, remove_ongoing_spawn, create_creature_message)

def load_command_list():
  command_list = {}
  command_list.update(ADMIN_COMMAND_LIST)
  command_list.update(USER_COMMAND_LIST)
  
  return command_list

class ChristmasBot(discord.Client):

  async def on_ready(self):
    self.command_list = load_command_list()
    self.dao = MemoryDao()
    # ongoing_spawns is used to make sure spawns happen 1 at a time in a channel
    self.ongoing_spawns = {}
    self.player_dict = {}
    print('Christmas Bot is up! Let the festivities begin!')

  async def on_message(self, message):
    if message.author == self.user:
      print('Received message is from Christmas Bot... skipping')
      return

    tokens = message.content.split(' ')
    command = tokens[0].lower()

    server_id = message.guild.id
    channel_id = message.channel.id
    
    response = 'Placeholder message - you shouldn\'t be seeing this'
    if command in self.command_list.keys():
      print('Invoking command {}'.format(command))
      await self.command_list[command](message, self.dao, tokens)
      await message.delete(delay=10)
    elif command in ['x!nice', 'x!naughty'] and not has_ongoing_spawn(self.ongoing_spawns, server_id, channel_id):
      # prevents max from spamming x!nice/naughty
      return
    else:
      # General message - calculate if the bot should respond
      server_config = self.dao.get_server(server_id)
      if ((channel_id in server_config.enabled_channels) and
        (not has_ongoing_spawn(self.ongoing_spawns, server_id, channel_id))):
        # channel where message is in has enabled spawns, calculate chance %
        roll = random.randint(0, 100)
        if roll <= server_config.spawn_rate_percent:
          # roll was successful, respond with spawn message
          print('Spawning creature...')
          creature = get_creature()
          item = get_item(creature)
          # lock spawn so 2 spawns don't happen at the same time
          add_ongoing_spawn(self.ongoing_spawns, server_id, channel_id, creature)
          bot_message = await message.channel.send(embed=create_creature_message(creature, item))

          def message_is_nice_or_naughty(message):
            return (message.guild.id == server_id and message.channel.id == channel_id
              and (message.content == 'x!nice' or message.content == 'x!naughty'))
          
          try:
            reply = await self.wait_for('message', 
              check=message_is_nice_or_naughty, 
              timeout=server_config.despawn_time
            )
            bot_response, is_right = check_if_command_correct(creature, item, reply)
            #add user to player list if they aren't on it:
            self.dao.create_player_entry_if_nonexistent(server_id, message.author)
            if is_right and item not in self.dao.server_players[server_id][message.author].inventory:
              #give player the item
              self.dao.add_item_to_player(server_id, message.author, item)
              for item in self.dao.server_players[server_id][message.author].inventory:
                #debugging purposes, print items
                print(item.display_name)
            elif not is_right:
              # replace it with coal if you have an item
              if len(self.dao.server_players[server_id][message.author].inventory)>0:
                popped_item = self.dao.replace_player_item_with_coal(server_id, message.author)
                print('coal=', self.dao.server_players[server_id][message.author].coal_count)
                bot_response, temp = check_if_command_correct(creature, popped_item, reply)
              else:
                #update coal count even if they dont have any items
                self.dao.server_players[server_id][message.author].coal_count += 1
                print('coal=', self.dao.server_players[server_id][message.author].coal_count)
                bot_response = '{} tried to replace an item with coal, but your inventory is empty. ' \
                               'Maybe coal isn\'t so bad after all...'.format(creature.display_name)
            else:
              bot_response = 'You already had that item :('
            await reply.delete(delay=5)
          except asyncio.TimeoutError:
            bot_response = 'The creature left because you kept it waiting for too long!'
          finally:
            remove_ongoing_spawn(self.ongoing_spawns, server_id, channel_id)
            await message.channel.send(bot_response)


def run():
  client = ChristmasBot()
  client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run()
