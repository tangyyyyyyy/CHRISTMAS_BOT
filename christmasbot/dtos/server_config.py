from constants.globals import DEFAULT_DESPAWN_TIME_SECONDS, DEFAULT_SPAWN_RATE_PERCENT


class ServerConfigDto(object):
  def __init__(self, server_id: int, despawn_time_seconds: int=DEFAULT_DESPAWN_TIME_SECONDS, 
    spawn_rate_percent: int=DEFAULT_SPAWN_RATE_PERCENT, 
    enabled_channels: list[int]=[], items: list[str]=[]):
    self.id = server_id
    self.enabled_channels = enabled_channels
    self.items = items
    self.despawn_time = despawn_time_seconds
    self.spawn_rate_percent = spawn_rate_percent