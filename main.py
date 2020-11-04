import discord
from src.const import token
import src.message as msg

class christmasBot(discord.Client):
  async def on_ready(self):
    print('ONLINE')
  async def on_message(self, message):
    if message.content == 'x!naughty':
      await message.channel.send(msg.naughtyCorrect) 

client = christmasBot()
client.run(token)