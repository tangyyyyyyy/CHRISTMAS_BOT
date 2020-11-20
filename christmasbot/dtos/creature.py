class CreatureDto:
  def __init__(self, creature_id: str, display_name: str, pronoun: str, img_url: str, 
    status: str, items: list[str]=[]):
    self.display_name = display_name
    self.id = creature_id
    self.img_url = img_url
    self.status = status #naughty, either, nice
    self.pronoun = pronoun
    self.items = items

  @classmethod
  def new(cls, creature: 'CreatureDto'):
    return CreatureDto(
      creature_id=creature.id,
      display_name=creature.display_name,
      pronoun=creature.pronoun,
      img_url=creature.img_url,
      status=creature.status,
      items=creature.items
    )