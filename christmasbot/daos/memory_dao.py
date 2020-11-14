import random

from daos.abstract_dao import AbstractDao

from dtos.creature import CreatureDto
from dtos.item import ItemDto, ItemRarity
from dtos.player import PlayerDto
from dtos.server_config import ServerConfigDto

class MemoryDao(AbstractDao):
  def __init__(self):
    self.server_configs: dict[int, ServerConfigDto] = {}
    self.server_players: dict[int, dict[int, PlayerDto]] = {}
    self.creatures: dict[str, CreatureDto] = {
      'nice_gingy': CreatureDto('nice_gingy', 'Nice Gingy', 'she', 
        'https://i.imgur.com/MBmsrHG.png', 'nice', 
        ['gumdrop_ornament', 'iced_bowtie']),
      'naughty_gingy': CreatureDto('naughty_gingy', 'Naughty Gingy', 'he', 
        'https://i.imgur.com/1CnajlU.png', 'naughty', ['dash_of_cinnamon', 'iced_bowtie'])
    }
    self.items: dict[str, ItemDto] = {
      'gumdrop_ornament': ItemDto('gumdrop_ornament', 'Gumdrop Ornament', 
        'https://i.imgur.com/1CnajlU.png', ItemRarity.RARE),
      'iced_bowtie': ItemDto('iced_bowtie', 'Iced Bowtie', 
        'https://i.imgur.com/1CnajlU.png', ItemRarity.SPECIAL),
      'dash_of_cinnamon': ItemDto('dash_of_cinnamon', 'Dash of Cinnamon', 
        'https://i.imgur.com/1CnajlU.png', ItemRarity.COMMON)
    }

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
      self.server_players[server][player] = PlayerDto(player, inventory=[])


  # Admin Config

  async def enable_channel(self, server, channel):
    self.create_server_entry_if_nonexistent(server)
    if channel not in self.server_configs[server].enabled_channels:
      # not enabled yet
      self.server_configs[server].enabled_channels.append(channel)
      return channel
    else:
      # already enabled
      return None

  async def disable_channel(self, server, channel):
    self.create_server_entry_if_nonexistent(server)
    if channel in self.server_configs[server].enabled_channels:
      # enabled; remove
      self.server_configs[server].enabled_channels.remove(channel)
      return channel
    else:
      # already disabled
      return None

  async def change_despawn_time(self, server, new_despawn_time):
    self.create_server_entry_if_nonexistent(server)
    if new_despawn_time < 0:
      return None
    else:
      self.server_configs[server].despawn_time = new_despawn_time
      return new_despawn_time

  async def change_spawn_rate(self, server, new_spawn_rate):
    self.create_server_entry_if_nonexistent(server)
    if new_spawn_rate < 0 or new_spawn_rate > 100:
      return None
    else:
      self.server_configs[server].spawn_rate_percent = new_spawn_rate
      return new_spawn_rate


  # User Interactions

  async def get_leaderboard(self, server, num_results, page):
    self.create_server_entry_if_nonexistent(server)
    pass

  async def get_player(self, server, player):
    self.create_server_entry_if_nonexistent(server)
    self.create_player_entry_if_nonexistent(server, player)
    return self.server_players[server][player]

  async def get_server(self, server):
    self.create_server_entry_if_nonexistent(server)
    return self.server_configs[server]


  # Spawn/Item Interactions

  async def add_item_to_player(self, server, player, item):
    self.create_server_entry_if_nonexistent(server)
    self.create_player_entry_if_nonexistent(server, player)
    if item not in self.server_players[server][player].inventory:
      self.server_players[server][player].inventory.append(item)
      return item
    else:
      # player already has item
      return None


  async def replace_player_item_with_coal(self, server, player):
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


  async def get_creature(self, creature: str):
    if creature in self.creatures:
      return self.creatures[creature]
    else:
      raise Exception('Creature {} does not exist!'.format(creature))


  async def get_random_creature(self):
    if len(self.creatures) == 0:
      raise Exception('No creatures exist to choose from!')
    key_chosen = random.choice(list(self.creatures.keys()))
    return self.creatures.get(key_chosen)


  async def get_items(self, items: list[str]):
    results = []
    for item in items:
      if item in self.items.keys():
        results.append(self.items.get(item))
      else:
        raise Exception('Item {} does not exist!'.format(item))
    return results


  async def get_item(self, item: str):
    if item in self.items:
      return self.items[item]
    else:
      raise Exception('Item {} does not exist!'.format(item))
