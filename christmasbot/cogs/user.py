from constants.messages import HELP_MESSAGE
from daos.abstract_dao import AbstractDao
from daos.memory_dao import MemoryDao
from helpers.user import format_inventory
import discord
from discord.ext import commands


class User(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Commands
    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=HELP_MESSAGE)
      
    @commands.command()
    async def inventory(self, ctx, dao: MemoryDao):
      server_id = ctx.guild.id
      author_profile = dao.get_player(server_id, ctx.author.id).inventory
      detailed_inventory = dao.get_items(author_profile)
      if detailed_inventory is None:
        raise Exception('Items in player\'s inventory do not exist!')
      response = format_inventory(ctx.author, detailed_inventory)
      await ctx.channel.send(embed=response)

    @commands.command()
    async def leaderboard(self, ctx, dao: AbstractDao):
      response = 'leaderboard placeholder'
      await ctx.channel.send(response) 

    @commands.command()
    async def tree(self, ctx, dao: AbstractDao):
      response = 'tree placeholder'
      await ctx.channel.send(response) 

def setup(client):
    client.add_cog(User(client))