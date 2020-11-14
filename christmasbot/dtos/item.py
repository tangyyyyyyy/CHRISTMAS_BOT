from enum import IntEnum


class ItemRarity(IntEnum):
  def __str__(self):
    return self.name.lower()

  COMMON = 1
  SPECIAL = 2
  RARE = 3


class ItemDto:
  def __init__(self, item_id: str, display_name: str, rarity: ItemRarity, img_url: str=''):
    self.id = item_id
    self.display_name = display_name
    self.img_url = img_url
    self.rarity = rarity # can be converted to int if needed