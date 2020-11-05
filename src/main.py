import discord
from const import TOKEN
import message as msg

class ChristmasBot(discord.Client):
  async def on_ready(self):
    print('ONLINE')
  async def on_message(self, message):
    if message.content == 'x!naughty':
      await message.channel.send(msg.naughtyCorrect) 


def run():
  client = ChristmasBot()
  client.run(TOKEN)

if __name__ == "__main__":
    run()