import asyncio
import random

from daos.db_dao import DbDao
from dtos.creature import CreatureDto
from dtos.item import ItemDto
from dtos.player import PlayerDto
from dtos.server_config import ServerConfigDto
from helpers.db import get_session, servers_table, players_table, creatures_table, items_table


class CachedDbDao(DbDao):
  def __init__(self):
    super().__init__()
    self.server_cache: dict[int, ServerConfigDto] = {}
    self.player_cache: dict[int, dict[int, PlayerDto]] = {}
    self.creature_cache: dict[str, CreatureDto] = {}
    self.item_cache: dict[str, ItemDto] = {}
    self.get_creatures_from_db()
    self.get_items_from_db()
  
  def get_creatures_from_db(self):
    session = get_session()

    creature_query = session.query(creatures_table)

    if creature_query.count() != len(self.creature_cache.keys()):
      creatures = creature_query.all()
      self.creature_cache = {}
      for creature in creatures:
        self.creature_cache[creature.id] = creature

  def get_items_from_db(self):
    session = get_session()
    item_query = session.query(items_table)
    if item_query.count() != len(self.item_cache.keys()):
      items = item_query.all()
      self.item_cache = {}
      for item in items:
        self.item_cache[item.id] = item


  async def enable_channel(self, server_id, channel_id):
    if server_id in self.server_cache.keys():
      # already cached
      if channel_id in self.server_cache[server_id].enabled_channels:
        return None
      else:
        self.server_cache[server_id].enabled_channels.append(channel_id)
        asyncio.run_coroutine_threadsafe(
          DbDao.enable_channel(self, server_id, channel_id), 
          asyncio.get_event_loop()
        )
        return self.server_cache[server_id]
    else:
      server = await DbDao.enable_channel(self, server_id, channel_id)
      # this returns a server with the channel enabled
      if server is None:
        return None
      else:
        self.server_cache[server_id] = ServerConfigDto.new(server)
        return server

      

  async def disable_channel(self, server_id, channel_id):
    if server_id in self.server_cache.keys():
      # already cached
      if channel_id not in self.server_cache[server_id].enabled_channels:
        return None
      else:
        self.server_cache[server_id].enabled_channels.remove(channel_id)
        asyncio.run_coroutine_threadsafe(
          DbDao.disable_channel(self, server_id, channel_id), 
          asyncio.get_event_loop()
        )
        return self.server_cache[server_id]
    else:
      server = await DbDao.disable_channel(self, server_id, channel_id)
      if server is None:
        return None
      else:
        self.server_cache[server_id] = ServerConfigDto.new(server)
        return server
   
   
  async def change_despawn_time(self, server_id: int, new_despawn_time: int):
    if new_despawn_time < 0:
      return None
    if server_id in self.server_cache.keys():
      # already cached
      self.server_cache[server_id].despawn_time = new_despawn_time
      asyncio.run_coroutine_threadsafe(
        DbDao.change_despawn_time(self, server_id, new_despawn_time), 
        asyncio.get_event_loop()
      )
      return self.server_cache[server_id]
    else:
      server = await DbDao.change_despawn_time(self, server_id, new_despawn_time)
      if server is None:
        return None
      else:
        self.server_cache[server_id] = ServerConfigDto.new(server)
        return server


  async def change_spawn_rate(self, server_id: int, new_spawn_rate: int):
    if new_spawn_rate < 0 or new_spawn_rate > 100:
      return None
    if server_id in self.server_cache.keys():
      # already cached
      self.server_cache[server_id].spawn_rate_percent = new_spawn_rate
      asyncio.run_coroutine_threadsafe(
        DbDao.change_spawn_rate(self, server_id, new_spawn_rate), 
        asyncio.get_event_loop()
      )
      return self.server_cache[server_id]
    else:
      server = await DbDao.change_spawn_rate(self, server_id, new_spawn_rate)
      if server is None:
        return None
      else:
        self.server_cache[server_id] = ServerConfigDto.new(server)
        return server


  # User Interactions

  async def get_leaderboard(self, server_id: int, num_results: int, set_num: int) -> list[PlayerDto]:
    # we always defer to the DB for this method because there can always be players 
    # for a particular server that are present in DB but not in cache. this method
    # can return inaccurate results if run concurrently with add_item_to_player or
    # replace_player_item_with_coal but that's ok, dbdao would too.
    return await DbDao.get_leaderboard(self, server_id, num_results, set_num)


  async def get_player(self, server_id: int, player_id: int) -> PlayerDto:
    if server_id not in self.player_cache.keys():
      self.player_cache[server_id] = {}
    if player_id in self.player_cache[server_id]:
        return self.player_cache[server_id][player_id]
    else:
      player = await DbDao.get_player(self, server_id, player_id)
      self.player_cache[server_id][player_id] = PlayerDto.new(player)
      return player


  async def get_server(self, server_id: int) -> ServerConfigDto:
    if server_id in self.server_cache.keys():
      return self.server_cache[server_id]
    else:
      server = await DbDao.get_server(self, server_id)
      self.server_cache[server_id] = ServerConfigDto.new(server)
      return server


  # Spawn/Item Interactions

  async def add_item_to_player(self, server_id: int, player_id: int, item_id: str):
    if server_id not in self.player_cache.keys():
      self.player_cache[server_id] = {}
    if player_id in self.player_cache[server_id]:
      # cached
      if item_id not in self.player_cache[server_id][player_id].inventory:
        self.player_cache[server_id][player_id].inventory.append(item_id)
        self.player_cache[server_id][player_id].score = self.player_cache[server_id][player_id].score + 1
        asyncio.run_coroutine_threadsafe(
          DbDao.add_item_to_player(self, server_id, player_id, item_id),
          asyncio.get_event_loop()
        )
        return self.player_cache[server_id][player_id]
      else:
        # player already has the item
        return None
    else:
      # load from db
      player = await DbDao.add_item_to_player(self, server_id, player_id, item_id)
      if player is None:
        return None
      else:
        self.player_cache[server_id][player_id] = PlayerDto.new(player)
        return player



  async def replace_player_item_with_coal(self, server_id: int, player_id: int, item_id: str):
    if server_id not in self.player_cache.keys():
      self.player_cache[server_id] = {}
    if player_id in self.player_cache[server_id]:
      # cached, 
      self.player_cache[server_id][player_id].coal_count += 1
      if item_id in self.player_cache[server_id][player_id].inventory:
        # we can assume inv is not empty and remove it
        self.player_cache[server_id][player_id].inventory.remove(item_id)
        self.player_cache[server_id][player_id].score -= 1
        asyncio.run_coroutine_threadsafe(
          DbDao.replace_player_item_with_coal(self, server_id, player_id, item_id),
          asyncio.get_event_loop()
        )
        return self.player_cache[server_id][player_id]
      else:
        # kept as a failsafe
        return None
    else:
      # load from db
      player = await DbDao.replace_player_item_with_coal(self, server_id, player_id, item_id)
      if player is None:
        # since a new player is always created this should never happen, but 
        # kept as a failsafe
        return None
      else:
        self.player_cache[server_id][player_id] = PlayerDto.new(player)
        return player


  # Bot specific DAO calls

  async def get_creature(self, creature_id: str):
    if creature_id in self.creature_cache.keys():
      return self.creature_cache[creature_id]
    else:
      self.get_creatures_from_db()
      if creature_id not in self.creature_cache.keys():
        raise Exception('Creature {} does not exist!'.format(creature_id))
      else:
        return self.creature_cache[creature_id]



  async def get_random_creature(self):
    if len(self.creature_cache.keys()) == 0:
      raise Exception('No creatures exist to choose from!')
    key_chosen = random.choice(list(self.creature_cache.keys()))
    return self.creature_cache.get(key_chosen)

    

  async def get_item(self, item_id: str):
    if item_id in self.item_cache.keys():
      return self.item_cache[item_id]
    else:
      self.get_items_from_db()
      if item_id not in self.item_cache.keys():
        raise Exception('Item {} does not exist!'.format(item_id))
      else:
        return self.item_cache[item_id]

  async def get_items(self, item_ids: list[str]):
    res = []
    for item_id in item_ids:
      if item_id in self.item_cache.keys():
        res.append(self.item_cache[item_id])
      else:
        self.get_items_from_db()
        res = DbDao.get_items(self, item_ids)
        break
    return res


