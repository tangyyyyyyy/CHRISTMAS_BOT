import random

from daos.abstract_dao import AbstractDao

from dtos.creature import CreatureDto
from dtos.item import ItemDto
from dtos.player import PlayerDto
from dtos.server_config import ServerConfigDto

class MemoryDao(AbstractDao):
  def __init__(self):
    self.server_configs: dict[int, ServerConfigDto] = {}
    self.server_players: dict[int, dict[int, PlayerDto]] = {}
    self.creatures: dict[str, CreatureDto] = {}
    self.items: dict[str, ItemDto] = {}

  # Helpers

  # Create new server entry
  def create_server_entry_if_nonexistent(self, server: int):
    if server not in self.server_configs.keys():
      self.server_configs[server] = ServerConfigDto(server)
      self.server_players[server] = {}

  # Create new player entry
  # Precondition: server entry exists
  def create_player_entry_if_nonexistent(self, server: int, player: int):
    if player not in self.server_players[server].keys():
      self.server_players[server][player] = PlayerDto(player)


  # Admin Config

  def enable_channel(self, server, channel):
    self.create_server_entry_if_nonexistent(server)
    if channel not in self.server_configs[server].enabled_channels:
      # not enabled yet
      self.server_configs[server].enabled_channels.append(channel)
      return channel
    else:
      # already enabled
      return None

  def disable_channel(self, server, channel):
    self.create_server_entry_if_nonexistent(server)
    if channel in self.server_configs[server].enabled_channels:
      # enabled; remove
      self.server_configs[server].enabled_channels.remove(channel)
      return channel
    else:
      # already disabled
      return None

  def change_despawn_time(self, server, new_despawn_time):
    self.create_server_entry_if_nonexistent(server)
    if new_despawn_time < 0:
      return None
    else:
      self.server_configs[server].despawn_time = new_despawn_time
      return new_despawn_time

  def change_spawn_rate(self, server, new_spawn_rate):
    self.create_server_entry_if_nonexistent(server)
    if new_spawn_rate < 0 or new_spawn_rate > 100:
      return None
    else:
      self.server_configs[server].spawn_rate_percent = new_spawn_rate
      return new_spawn_rate


  # User Interactions

  def get_leaderboard(self, server, num_results, page):
    self.create_server_entry_if_nonexistent(server)
    pass

  def get_player(self, server, player):
    self.create_server_entry_if_nonexistent(server)
    self.create_player_entry_if_nonexistent(server, player)
    return self.server_players[server][player]

  def get_server(self, server):
    self.create_server_entry_if_nonexistent(server)
    return self.server_configs[server]


  # Spawn/Item Interactions

  def add_item_to_player(self, server, player, item):
    self.create_server_entry_if_nonexistent(server)
    self.create_player_entry_if_nonexistent(server, player)
    if item not in self.server_players[server][player].inventory:
      self.server_players[server][player].inventory.append(item)
      return item
    else:
      # player already has item
      return None

  def replace_player_item_with_coal(self, server, player):
    self.create_server_entry_if_nonexistent(server)
    self.create_player_entry_if_nonexistent(server, player)
    self.server_players[server][player].coal_count += 1
    if len(self.server_players[server][player].inventory) > 0:
      # player has at least 1 item, replace it!
      inventory_size = len(self.server_players[server][player].inventory)
      index_to_remove = random.randrange(inventory_size)
      removed_item = self.server_players[server][player].inventory.pop(index_to_remove)
      return removed_item
    else:
      # player has no items
      return None
