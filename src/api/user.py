from constants.messages import HELP_MESSAGE

def handle_help(message, token):
  return HELP_MESSAGE

def handle_inventory(message_token):
  return 'inventory placeholder'

def handle_leaderboard(message, token):
  return 'leaderboard placeholder'

def handle_tree(message, token):
  return 'tree placeholder'


USER_COMMAND_LIST = {
  'x!help': handle_help,
  'x!inventory': handle_inventory,
  'x!leaderboard': handle_leaderboard,
  'x!tree': handle_tree
}
