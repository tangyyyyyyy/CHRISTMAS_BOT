import discord
from constants.config import DISCORD_TOKEN, load_command_list
from api.spawn import handle_spawn_chance


class ChristmasBot(discord.Client):    

  async def on_ready(self):
    self.command_list = load_command_list()
    print('Christmas Bot is up! Let the festivities begin!')

  async def on_message(self, message):
    if message.author == self.user:
      print('Received message is from Christmas Bot... skipping')
      return

    tokens = message.content.split()
    command = tokens[0].lower()
    
    response = 'Placeholder message - you shouldn\'t be seeing this'
    if command in self.command_list.keys():
      response = self.command_list[command](message, tokens)
    else:
      response = handle_spawn_chance(message, tokens)

    print("Response: " + str(response) + ' with type ' + str(type(response)))
    await message.channel.send(response) 


def run():
  client = ChristmasBot()
  client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run()
