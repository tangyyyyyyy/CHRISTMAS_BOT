from operator import and_
import random

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import func

from daos.abstract_dao import AbstractDao
from dtos.player import PlayerDto
from dtos.server_config import ServerConfigDto
from helpers.db import get_session, init_engine, servers_table, players_table, creatures_table, items_table


class DbDao(AbstractDao):
  def __init__(self):
    init_engine()
    

  def create_server_entry_if_nonexistent(self, session: Session, server_id: int) -> ServerConfigDto:
    server = session.query(servers_table).filter(servers_table.c.id == server_id).first()
    if server is None:
      # no server entry exists
      server = ServerConfigDto(server_id)
      session.add(server)
    return server


  # Create new player entry
  # Precondition: server entry exists
  def create_player_entry_if_nonexistent(self, session: Session, server_id: int, player_id: int) -> PlayerDto:
    player = session.query(players_table).filter(
      players_table.c.server_id == server_id,
      players_table.c.player_id == player_id
    ).first()
    if player is None:
      # no player entry exists
      player = PlayerDto(server_id, player_id)
      session.add(player)
    return player

  # Admin Config

  async def enable_channel(self, server_id, channel_id):
    session = get_session()
    server = self.create_server_entry_if_nonexistent(session, server_id)
    if channel_id not in server.enabled_channels:
      server.enabled_channels.append(channel_id)
      update_stmt = servers_table.update().where(servers_table.c.id == server_id).values(
        enabled_channels=server.enabled_channels
      )
      session.execute(update_stmt)
      session.commit()
      return channel_id
    else:
      return None

  async def disable_channel(self, server_id, channel_id):
    session = get_session()
    server = self.create_server_entry_if_nonexistent(session, server_id)
    if channel_id in server.enabled_channels:
      server.enabled_channels.remove(channel_id)
      update_stmt = servers_table.update().where(servers_table.c.id == server_id).values(
        enabled_channels=server.enabled_channels
      )
      session.execute(update_stmt)
      session.commit()
      return channel_id
    else:
      return None
   
   
  async def change_despawn_time(self, server_id: int, new_despawn_time: int):
    session = get_session()
    server = self.create_server_entry_if_nonexistent(session, server_id)
    if new_despawn_time < 0:
      return None
    else:
      update_stmt = servers_table.update().where(servers_table.c.id == server_id).values(
        despawn_time=new_despawn_time
      )
      session.execute(update_stmt)
      session.commit()
      return new_despawn_time


  async def change_spawn_rate(self, server_id: int, new_spawn_rate: int):
    session = get_session()
    server = self.create_server_entry_if_nonexistent(session, server_id)
    if new_spawn_rate < 0 or new_spawn_rate > 100:
      return None
    else:
      update_stmt = servers_table.update().where(servers_table.c.id == server_id).values(
        spawn_rate_percent=new_spawn_rate
      )
      session.execute(update_stmt)
      session.commit()
      return new_spawn_rate


  # User Interactions

  async def get_leaderboard(self, server_id: int, num_results: int, page: int):
    """ Gets a list of players for server sorted by score
    TODO add sorting by most recent acquired item time

    Parameters:
    - server_id (int): the discord ID of the server
    - num_results (int): the number of results to get
    - page (int): the page of results

    Returns sorted list of players if successful and None if num_results <= 0 or page <= 0.
    """
    pass


  async def get_player(self, server_id: int, player_id: int) -> PlayerDto:
    session = get_session()
    self.create_server_entry_if_nonexistent(session, server_id)
    player = self.create_player_entry_if_nonexistent(session, server_id, player_id)
    try:
      # in case a new player is added but not committed yet
      session.commit()
    except InvalidRequestError:
      # in case no new player is added, do nothing
      pass
    return player


  async def get_server(self, server_id: int) -> ServerConfigDto:
    session = get_session()
    server = self.create_server_entry_if_nonexistent(session, server_id)
    try:
      # in case a new server is added but not committed yet
      session.commit()
    except InvalidRequestError:
      # in case no new server is added, do nothing
      pass
    return server


  # Spawn/Item Interactions

  async def add_item_to_player(self, server_id: int, player_id: int, item_id: str):
    session = get_session()
    self.create_server_entry_if_nonexistent(session, server_id)
    player = self.create_player_entry_if_nonexistent(session, server_id, player_id)
    if item_id not in player.inventory:
      player.inventory.append(item_id)
      update_stmt = players_table.update().where(and_(
        players_table.c.server_id == server_id,
        players_table.c.player_id == player_id
      )).values(
        inventory=player.inventory,
        score=player.score + 1
      )
      session.execute(update_stmt)
      # A transaction is guaranteed because of the update statement, no needd
      # to account for exceptions
      session.commit()
      return item_id
    else:
      # we don't need to commit anything here because if a player already has an
      # item, then it cannot be just created and thus there's nothing to commit
      return None


  async def replace_player_item_with_coal(self, server_id: int, player_id: int):
    session = get_session()
    self.create_server_entry_if_nonexistent(session, server_id)
    player = self.create_player_entry_if_nonexistent(session, server_id, player_id)
    if len(player.inventory) > 0:
      # player's inventory is not empty, replace an item
      # TODO make this based on rarity
      inventory_size = len(player.inventory)
      index_to_remove = random.randrange(inventory_size)
      removed_item = player.inventory.pop(index_to_remove)
      update_stmt = players_table.update().where(
        players_table.c.server_id == server_id
      ).where(
        players_table.c.player_id == player_id
      ).values(
        inventory=player.inventory,
        coal_count=player.coal_count + 1,
        score=player.score - 1
      )
      session.execute(update_stmt)
      session.commit()
      return removed_item
    else:
      # player's inventory is empty
      # there's a chance that player was just created so we need to commit
      try:
        # in case a new server is added but not committed yet
        session.commit()
      except InvalidRequestError:
        # in case no new server is added, do nothing
        pass
      finally:
        return None


  # Bot specific DAO calls

  async def get_creature(self, creature_id: str):
    session = get_session()
    creature = session.query(creatures_table).filter(creatures_table.c.id == creature_id).first()
    if creature is None:
      raise Exception('Creature {} does not exist!'.format(creature_id))
    else:
      return creature


  async def get_random_creature(self):
    session = get_session()
    creature = session.query(creatures_table).order_by(func.random()).first()
    if creature is None:
      raise Exception('No creatures exist to choose from!')
    return creature

    

  async def get_item(self, item_id: str):
    session = get_session()
    item = session.query(items_table).filter(items_table.c.id == item_id).first()
    if item is None:
      raise Exception('Creature {} does not exist!'.format(item_id))
    else:
      return item

  async def get_items(self, item_ids: list[str]):
    session = get_session()
    items = session.query(items_table).filter(items_table.c.id.in_(item_ids)).all()
    if len(items) != len(item_ids):
      raise Exception('An item within {} does not exist!'.format(str(item_ids)))
    else:
      return items
  