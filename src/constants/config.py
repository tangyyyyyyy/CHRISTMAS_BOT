from api.admin import ADMIN_COMMAND_LIST
from api.spawn import SPAWN_COMMAND_LIST
from api.user import USER_COMMAND_LIST

DISCORD_CLIENT_ID = '773308497538056222'
DISCORD_TOKEN = 'your princess is in another castle'

def load_command_list():
  command_list = {}
  command_list.update(ADMIN_COMMAND_LIST)
  command_list.update(SPAWN_COMMAND_LIST)
  command_list.update(USER_COMMAND_LIST)
  
  return command_list