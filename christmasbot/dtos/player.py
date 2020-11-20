class PlayerDto: 
  def __init__(self, server_id: int, player_id: int, inventory: list[str]=[], 
    coal_count: int=0, score: int=0):
    self.server_id = server_id
    self.player_id = player_id
    self.inventory = inventory #list of items
    self.coal_count = coal_count
    self.score = len(inventory)

  @classmethod
  def new(cls, player: 'PlayerDto'):
    return PlayerDto(
      server_id=player.server_id,
      player_id=player.player_id,
      inventory=player.inventory,
      coal_count=player.coal_count,
      score=player.score
    )