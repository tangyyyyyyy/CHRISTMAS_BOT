
def handle_enable_channel(message, tokens):
  return 'Channel enabled placeholder'

def handle_disable_channel(message, tokens):
  return 'Channel disabled placeholder'

def handle_change_despawn_time(message, tokens):
  return 'Change despawn time placeholder'

def handle_change_spawn_rate(message, tokens):
  return 'Change spawn rate placeholder'

def handle_refresh_role(message, tokens):
  return 'Refresh role placeholder'


ADMIN_COMMAND_LIST = {
  'x!enable': handle_enable_channel,
  'x!disable': handle_disable_channel,
  'x!time': handle_change_despawn_time,
  'x!role': handle_refresh_role,
  'x!setchance': handle_change_spawn_rate
}
