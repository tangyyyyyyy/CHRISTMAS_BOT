import random

from operator import itemgetter
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
        'https://i.imgur.com/1CnajlU.png', 'naughty',
        ['dash_of_cinnamon', 'iced_bowtie'])
    }

    self.items: dict[str, ItemDto] = {
      'gumdrop_ornament': ItemDto('gumdrop_ornament', 'Gumdrop Ornament', 
        ItemRarity.RARE, 'https://i.imgur.com/1CnajlU.png'),
      'iced_bowtie': ItemDto('iced_bowtie', 'Iced Bowtie', 
        ItemRarity.SPECIAL, 'https://i.imgur.com/1CnajlU.png'),
      'dash_of_cinnamon': ItemDto('dash_of_cinnamon', 'Dash of Cinnamon', 
        ItemRarity.COMMON, 'https://i.imgur.com/1CnajlU.png')
    }

  # Helpers

  # Create new server entry
  def create_server_entry_if_nonexistent(self, server_id: int):
    if server_id not in self.server_configs.keys():
      self.server_configs[server_id] = ServerConfigDto(server_id, items=[], enabled_channels=[])
      self.server_players[server_id] = {}

  # Create new player entry
  # Precondition: server entry exists
  def create_player_entry_if_nonexistent(self, server_id: int, player_id: int):
    if player_id not in self.server_players[server_id].keys():
      self.server_players[server_id][player_id] = PlayerDto(server_id, player_id, inventory=[])


  # Admin Config

  async def enable_channel(self, server_id: int, channel_id: int):
    self.create_server_entry_if_nonexistent(server_id)
    if channel_id not in self.server_configs[server_id].enabled_channels:
      # not enabled yet
      self.server_configs[server_id].enabled_channels.append(channel_id)
      return channel_id
    else:
      # already enabled
      return None

  async def disable_channel(self, server: int, channel_id: int):
    self.create_server_entry_if_nonexistent(server)
    if channel_id in self.server_configs[server].enabled_channels:
      # enabled; remove
      self.server_configs[server].enabled_channels.remove(channel_id)
      return channel_id
    else:
      # already disabled
      return None

  async def change_despawn_time(self, server_id: int, new_despawn_time: int):
    self.create_server_entry_if_nonexistent(server_id)
    if new_despawn_time < 0:
      return None
    else:
      self.server_configs[server_id].despawn_time = new_despawn_time
      return new_despawn_time

  async def change_spawn_rate(self, server_id: int, new_spawn_rate: int):
    self.create_server_entry_if_nonexistent(server_id)
    if new_spawn_rate < 0 or new_spawn_rate > 100:
      return None
    else:
      self.server_configs[server_id].spawn_rate_percent = new_spawn_rate
      return new_spawn_rate


  # User Interactions

  async def get_leaderboard(self, server, num_results, page, bot):
    leader_board = {}
    self.create_server_entry_if_nonexistent(server)
    for player_id in self.server_players[server].keys():  # for player in dict
      usr = await bot.fetch_user(player_id)
      print('score', self.server_players[server][player_id].score)
      leader_board[usr.name] = len(self.server_players[server][player_id].inventory)
    return leader_board

  async def get_player(self, server_id, player_id):
    self.create_server_entry_if_nonexistent(server_id)
    self.create_player_entry_if_nonexistent(server_id, player_id)
    return self.server_players[server_id][player_id]

  async def get_server(self, server_id):
    self.create_server_entry_if_nonexistent(server_id)
    return self.server_configs[server_id]


  # Spawn/Item Interactions

  async def add_item_to_player(self, server_id: int, player_id: int, item_id: str):
    self.create_server_entry_if_nonexistent(server_id)
    self.create_player_entry_if_nonexistent(server_id, player_id)
    if item_id not in self.server_players[server_id][player_id].inventory:
      self.server_players[server_id][player_id].inventory.append(item_id)
      self.server_players[server_id][player_id].score += 1
      return item_id
    else:
      # player already has item
      return None


  async def replace_player_item_with_coal(self, server_id: int, player_id: int):
    self.create_server_entry_if_nonexistent(server_id)
    self.create_player_entry_if_nonexistent(server_id, player_id)
    self.server_players[server_id][player_id].coal_count += 1
    if len(self.server_players[server_id][player_id].inventory) > 0:
      # player has at least 1 item, replace it!
      inventory_size = len(self.server_players[server_id][player_id].inventory)
      index_to_remove = random.randrange(inventory_size)
      removed_item = self.server_players[server_id][player_id].inventory.pop(index_to_remove)
      self.server_players[server_id][player_id].score -= 1
      return removed_item
    else:
      # player has no items
      return None


  async def get_creature(self, creature_id: str):
    if creature_id in self.creatures:
      return self.creatures[creature_id]
    else:
      raise Exception('Creature {} does not exist!'.format(creature_id))


  async def get_random_creature(self):
    if len(self.creatures) == 0:
      raise Exception('No creatures exist to choose from!')
    key_chosen = random.choice(list(self.creatures.keys()))
    return self.creatures.get(key_chosen)


  async def get_items(self, item_ids: list[str]):
    results = []
    for item in item_ids:
      if item in self.items.keys():
        results.append(self.items.get(item))
      else:
        raise Exception('Item {} does not exist!'.format(item))
    return results


  async def get_item(self, item_id: str):
    if item_id in self.items:
      return self.items[item_id]
    else:
      raise Exception('Item {} does not exist!'.format(item_id))

  async def give_champion_role(self, server_id: int, player_id: int):
    self.create_server_entry_if_nonexistent(server_id)
    self.create_player_entry_if_nonexistent(server_id, player_id)
    player_list = self.server_players[server_id].values()
    champ = max(player_list, key=lambda item: item.score)
    return champ.player_id
