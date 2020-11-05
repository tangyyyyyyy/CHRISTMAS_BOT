from api.admin import ADMIN_COMMAND_LIST
from api.spawn import SPAWN_COMMAND_LIST
from api.user import USER_COMMAND_LIST

DISCORD_CLIENT_ID = '773308497538056222'
DISCORD_TOKEN = 'NzczMzA4NDk3NTM4MDU2MjIy.X6HVqQ.LiAFUTHJh6PzMVKY7g0GrkRWYW8'

def load_command_list():
  command_list = {}
  command_list.update(ADMIN_COMMAND_LIST)
  command_list.update(SPAWN_COMMAND_LIST)
  command_list.update(USER_COMMAND_LIST)
  
  return command_list