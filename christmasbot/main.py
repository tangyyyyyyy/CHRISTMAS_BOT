import discord
import random

from api.spawn import handle_spawn_chance
from constants.config import DISCORD_TOKEN, load_command_list
from daos.memory_dao import MemoryDao

class ChristmasBot(discord.Client):    

  async def on_ready(self):
    self.command_list = load_command_list()
    self.dao = MemoryDao()
    print('Christmas Bot is up! Let the festivities begin!')

  async def on_message(self, message):
    if message.author == self.user:
      print('Received message is from Christmas Bot... skipping')
      return

    tokens = message.content.split(' ')
    command = tokens[0].lower()
    
    response = 'Placeholder message - you shouldn\'t be seeing this'
    if command in self.command_list.keys():
      print('Invoking command {}'.format(command))
      await self.command_list[command](message, self.dao, tokens)
    else:
      # General message - calculate if the bot should respond
      server_config = self.dao.get_server(message.guild.id)
      if message.channel.id in server_config.enabled_channels:
        # channel where message is in has enabled spawns, calculate chance %
        roll = random.randint(0, 100)
        if roll <= server_config.spawn_rate_percent:
          # roll was successful, respond with spawn message
          print('Spawning creature...')
          await handle_spawn_chance(message, self.dao, tokens)

def run():
  client = ChristmasBot()
  client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run()
