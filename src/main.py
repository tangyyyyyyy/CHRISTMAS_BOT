import discord
from constants.config import DISCORD_TOKEN
from helpers import formatter
from classes import Creature, Item

class ChristmasBot(discord.Client):
  async def on_ready(self):
    print('Christmas Bot is up! Let the festivities begin!')
  async def on_message(self, message):
    if message.content == 'x!naughty':
      creature = Creature('tangy', 'he', None, None, None)
      item = Item('bug in your code', None, None, 'rare')

      await message.channel.send(formatter.format_naughty_correct(creature, item)) 


def run():
  client = ChristmasBot()
  client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run()