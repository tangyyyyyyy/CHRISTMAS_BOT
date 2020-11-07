class CreatureDto:
  def __init__(self, name: str, pronoun: str, creature_id: str, img_loc: str, 
    status: str):
    self.name = name
    self.id = creature_id
    self.img_loc = img_loc
    self.status = status #naughty, either, nice
    self.pronoun = pronoun