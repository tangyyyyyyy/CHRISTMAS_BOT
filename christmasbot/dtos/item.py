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
    self.rarity = ItemRarity(rarity) # can be converted to int if needed

  @classmethod
  def new(cls, item: 'ItemDto'):
    return ItemDto(
      item_id=item.id,
      display_name=item.display_name,
      rarity=item.rarity,
      img_url=item.img_url
    )