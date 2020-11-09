import discord
from discord.ext import commands

from constants.globals import ChristmasColor
from constants.messages import ADMIN_DISABLE_RESPONSE, ADMIN_ENABLE_RESPONSE, BAD_COMMAND_MESSAGE
from daos.abstract_dao import AbstractDao
from helpers.admin import format_bad_command_response, format_no_permissions_response, is_user_admin


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Commands
    @commands.command()
    async def enable(self, ctx, dao:AbstractDao):
      if not is_user_admin(ctx.author, ctx.channel):
        response = format_no_permissions_response(ctx.author)
      else:
        print('Enabled channel')
        dao.enable_channel(ctx.guild.id, ctx.channel.id)
        response = ADMIN_ENABLE_RESPONSE

      await ctx.channel.send(embed=response) 
      
    @commands.command()
    async def disable(self, ctx, dao: AbstractDao):
      if not is_user_admin(ctx.author, ctx.channel):
        response = format_no_permissions_response(ctx.author)
      else:
        print('Disabled channel')
        dao.disable_channel(ctx.guild.id, ctx.channel.id)
        response = ADMIN_DISABLE_RESPONSE
      
      await ctx.channel.send(embed=response) 

    @commands.command()
    async def settime(self, ctx, dao: AbstractDao, arg):
      new_despawn_time = -1
      try:
        new_despawn_time = int(args)
      except:
        pass
      if dao.change_despawn_time(ctx.guild.id, new_despawn_time) == None:
        response = BAD_COMMAND_MESSAGE
      else:
        print('Despawn time changed to {}'.format(new_despawn_time))
        response = 'I changed the despawn time to {} seconds!'.format(new_despawn_time)
      await ctx.channel.send(response) 

    @commands.command()
    async def setchance(self, ctx, dao: AbstractDao, arg):
      new_spawn_rate = -1
      try:
        new_spawn_rate = int(arg)
      except:
        pass
      if dao.change_spawn_rate(ctx.guild.id, new_spawn_rate) == None:
        response = BAD_COMMAND_MESSAGE
      else:
        print('Spawn rate changed to {}'.format(new_spawn_rate))
        response = 'I changed the spawn rate to {}%!'.format(new_spawn_rate)
      await ctx.channel.send(response) 

    @commands.command()
    async def role(self, ctx, dao: AbstractDao):
      response = 'Refresh role placeholder'
      await ctx.channel.send(response) 

def setup(client):
    client.add_cog(Admin(client))
