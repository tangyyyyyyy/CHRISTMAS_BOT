from abc import ABC, abstractmethod

class AbstractDao(ABC):

  # Admin Config

  @abstractmethod
  def enable_channel(self, server: int, channel: int):
    """ Enables a channel for the bot to spawn creaatures.

    TODO enable multiple channels

    Parameters:
    - server (int): the discord ID of the server
    - channel (int): the discord ID of the channel

    Returns channel if successfully enabled and None if it was already enabled.
    """
    pass

  @abstractmethod
  def disable_channel(self, server: int, channel: int):
    """ Enables a channel for the bot to spawn creaatures

    TODO disable multiple channels

    Parameters:
    - server (int): the discord ID of the server
    - channel (int): the discord ID of the channel

    Returns channel if successfully disabled and None if it is already disabled.
    """
    pass
  
  @abstractmethod
  def change_despawn_time(self, server: int, new_despawn_time: int):
    """ Enables a channel for the bot to spawn creaatures

    Parameters:
    - server (int): the discord ID of the server
    - new_despawn_time (int): the new despawn time in seconds

    Returns new_despawn_time if successfully changed and None new_desoawn_time <= 0.
    """
    pass

  @abstractmethod
  def change_spawn_rate(self, server: int, new_spawn_rate: int):
    """ Enables a channel for the bot to spawn creaatures

    Parameters:
    - server (int): the discord ID of the server
    - new_spawn_rate (int): the new despawn time in seconds

    Returns new_spawn_rate if successfully changed and None if not !(0 <= new_spawn_rate <= 100).
    """
    pass

  # User Interactions

  @abstractmethod
  def get_leaderboard(self, server: int, num_results: int, page: int):
    """ Gets a list of players for server sorted by score
    TODO add sorting by most recent acquired item time

    Parameters:
    - server (int): the discord ID of the server
    - num_results (int): the number of results to get
    - page (int): the page of results

    Returns sorted list of players if successful and None if num_results <= 0 or page <= 0.
    """
    pass

  @abstractmethod
  def get_player(self, server: int, player: int):
    """ Gets info for a player

    Parameters:
    - server (int): the discord ID of the server
    - player (int): the discord ID of the player

    Returns player dto if successful 
    """
    pass

  @abstractmethod
  def get_server(self, server: int):
    """ Gets the tree of a server

    Parameters:
    - server (int): the discord ID of the server

    Returns server dto if successful
    """
    pass

  # Spawn/Item Interactions

  @abstractmethod
  def add_item_to_player(self, server: int, player: int, item: str):
    """Adds an item to the user's inventory. If the user doesn't exist, creates it.

    Parameters:
    - server (int): the discord ID of the server
    - player (int): the discord ID of the player
    - item (str): the unique ID of an item

    Returns item if successful and None if player already has item
    """
    pass

  @abstractmethod
  def replace_player_item_with_coal(self, server: int, player: int):
    """ Replaces one of the player's items with coal randomly.
    If the user doesn't exist or has an empty inventory, no items are removed but 1 coal is added.
    TODO make this based on rarity of items

    Parameters:
    - server (int): the discord ID of the server
    - player (int): the discord ID of the player

    Returns the item if an item is removed, and None if no items were removed
    """
    pass


