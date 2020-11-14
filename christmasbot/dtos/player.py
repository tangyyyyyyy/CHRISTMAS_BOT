class PlayerDto: 
  def __init__(self, server_id: int, player_id: int, inventory: list[str]=[], 
    coal_count: int=0, score: int=0):
    self.server_id = server_id
    self.player_id = player_id
    self.inventory = inventory #list of items
    self.coal_count = coal_count
    self.score = len(inventory)