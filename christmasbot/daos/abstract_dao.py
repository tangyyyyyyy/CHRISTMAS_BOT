from abc import ABC, abstractmethod

from dtos.creature import CreatureDto
from dtos.item import ItemDto
from dtos.player import PlayerDto
from dtos.server_config import ServerConfigDto

class AbstractDao(ABC):

  # Admin Config

  @abstractmethod
  async def enable_channel(self, server_id: int, channel_id: int):
    """ Enables a channel for the bot to spawn creaatures.

    TODO enable multiple channels

    Parameters:
    - server_id (int): the discord ID of the server
    - channel_id (int): the discord ID of the channel

    Returns channel if successfully enabled and None if it was already enabled.
    """
    pass

  @abstractmethod
  async def disable_channel(self, server_id: int, channel_id: int):
    """ Enables a channel for the bot to spawn creaatures

    TODO disable multiple channels

    Parameters:
    - server_id (int): the discord ID of the server
    - channel_id (int): the discord ID of the channel

    Returns channel if successfully disabled and None if it is already disabled.
    """
    pass
  
  @abstractmethod
  async def change_despawn_time(self, server_id: int, new_despawn_time: int):
    """ Enables a channel for the bot to spawn creaatures

    Parameters:
    - server_id (int): the discord ID of the server
    - new_despawn_time (int): the new despawn time in seconds

    Returns new_despawn_time if successfully changed and None new_desoawn_time <= 0.
    """
    pass

  @abstractmethod
  async def change_spawn_rate(self, server_id: int, new_spawn_rate: int):
    """ Enables a channel for the bot to spawn creaatures

    Parameters:
    - server_id (int): the discord ID of the server
    - new_spawn_rate (int): the new despawn time in seconds

    Returns new_spawn_rate if successfully changed and None if not !(0 <= new_spawn_rate <= 100).
    """
    pass

  # User Interactions

  @abstractmethod
  async def get_leaderboard(self, server_id: int, num_results: int, set_num: int) -> list[PlayerDto]:
    """ Gets a list of players for server sorted by score
    TODO add sorting by most recent acquired item time

    Parameters:
    - server_id (int): the discord ID of the server
    - num_results (int): the number of results to get
    - set_num (int): the set number to pull from results (like page num, but 0 indexed)

    Returns sorted list of players if successful and an empty list if num_results <= 0 or set_num < 0.
    """
    pass

  @abstractmethod
  async def get_player(self, server_id: int, player_id: int) -> PlayerDto:
    """ Gets info for a player

    Parameters:
    - server_id (int): the discord ID of the server
    - player_id (int): the discord ID of the player

    Returns player dto if successful 
    """
    pass

  @abstractmethod
  async def get_server(self, server_id: int) -> ServerConfigDto:
    """ Gets a server config

    Parameters:
    - server_id (int): the discord ID of the server

    Returns server dto if successful
    """
    pass

  # Spawn/Item Interactions

  @abstractmethod
  async def add_item_to_player(self, server_id: int, player_id: int, item_id: str):
    """Adds an item to the user's inventory. If the user doesn't exist, creates it.

    Parameters:
    - server_id (int): the discord ID of the server
    - player_id (int): the discord ID of the player
    - item (str): the unique ID of an item

    Returns item if successful and None if player already has item
    """
    pass

  @abstractmethod
  async def replace_player_item_with_coal(self, server_id: int, player_id: int):
    """ Replaces one of the player's items with coal randomly.
    If the user doesn't exist or has an empty inventory, no items are removed but 1 coal is added.
    TODO make this based on rarity of items

    Parameters:
    - server_id (int): the discord ID of the server
    - player_id (int): the discord ID of the player

    Returns the item if an item is removed, and None if no items were removed
    """
    pass


  # Bot specific DAO calls

  @abstractmethod
  async def get_creature(self, creature_id: str) -> CreatureDto:
    """ Gets creature based on its ID.

    Parameters:
    - creature_id (str): unique creature id

    Returns the Creature dto or throws an exception if the creature doesn't exist.
    """
    pass

  @abstractmethod
  async def get_random_creature(self) -> CreatureDto:
    """ Gets a random creature dto

    Returns the creature dto, or throws an exception if there are no creatures available
    """
    pass

  @abstractmethod
  async def get_item(self, item_id: str) -> ItemDto:
    """ Gets item based on its ID.

    Parameters:
    - item_id (str): unique item ID

    Returns the item dto or throws an exception if the item doesn't exist.
    """
    pass

  @abstractmethod
  async def get_items(self, item_ids: list[str]) -> list[ItemDto]:
    """ List get_item but for multiple items

    Parameters:
    = item_ids (list[str]): unique item IDs

    Returns list[item dtos] or throws an exception if any item doesn't exist.
    """
    pass

  @abstractmethod
  async def get_champion(self, server_id: int, player_id: int) -> int:
    """ Gets player who should have champion of christmas tag

    Parameters:
    - server_id (int): the discord ID of the server
    - player_id (int): the discord ID of the player

    Returns player ID (int)
    """
    pass