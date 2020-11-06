class PlayerDto: 
  def __init__(self, discord_id: int, inventory: list=[], coal_count: int=0):
    self.discord_id = discord_id
    self.inventory = inventory #list of items
    self.coal_count = coal_count
