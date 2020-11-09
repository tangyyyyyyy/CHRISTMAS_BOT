import discord

from constants.globals import ChristmasColor
from constants.messages import ADMIN_NO_PERMISSIONS_DESCRIPTION, ADMIN_NO_PERMISSIONS_TITLE, BAD_COMMAND_MESSAGE_DESCRIPTION, BAD_COMMAND_MESSAGE_TITLE


def is_user_admin(user, channel):
  return user.permissions_in(channel).administrator


def format_no_permissions_response(user):
  return discord.Embed(
    title=ADMIN_NO_PERMISSIONS_TITLE,
    description=ADMIN_NO_PERMISSIONS_DESCRIPTION.format(user_mention=user.mention),
    color=discord.Colour(ChristmasColor.RED)
  ).set_author(
    name='Christmas Bot',
    icon_url='https://i.imgur.com/YZ6v1jw.png',
    url='https://github.com/tangyyyyyyy/CHRISTMAS_BOT'
  )


def format_bad_command_response(user):
  return discord.Embed(
    title=BAD_COMMAND_MESSAGE_TITLE,
    description=BAD_COMMAND_MESSAGE_DESCRIPTION.format(user_mention=user.mention),
    color=discord.Colour(ChristmasColor.RED)
  ).set_author(
    name='Christmas Bot',
    icon_url='https://i.imgur.com/YZ6v1jw.png',
    url='https://github.com/tangyyyyyyy/CHRISTMAS_BOT'
  )
