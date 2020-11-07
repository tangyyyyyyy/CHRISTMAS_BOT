class ItemDto:
  def __init__(self, name: str, item_id: str, img_loc: str, rarity: str):
    self.name = name
    self.id = item_id
    self.img_loc = img_loc
    self.rarity = rarity #str