from constants.config import DEFAULT_DESPAWN_TIME_SECONDS, DEFAULT_SPAWN_RATE_PERCENT


class ServerConfigDto:
  def __init__(self, despawn_time_seconds: int=DEFAULT_DESPAWN_TIME_SECONDS, 
    spawn_rate_percent: int=DEFAULT_SPAWN_RATE_PERCENT, 
    enabled_channels: list[str]=[], tree: list[str]=[]):
    self.enabled_channels = enabled_channels
    self.tree = tree
    self.despawn_time = despawn_time_seconds
    self.spawn_rate_percent = spawn_rate_percent