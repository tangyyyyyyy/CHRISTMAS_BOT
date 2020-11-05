class Item:
  def __init__(self, name, item_id, img_loc, rarity):
    self.name = name
    self.id = item_id
    self.img_loc = img_loc
    self.rarity = rarity #str


class helper: 
  def __init__(self, name, id):
    self.inventory = [] #list of items
    self.discordID = id
    self.name = name
    self.coal_count = 0
    self.score = 0

  def calc_score(self):
    self.score = len(self.inventory) - self.coal_count

  def found_item(self, item):
    self.inventory.append(item)

  def found_coal(self):
    #replace an item in inventory with coal
    pass

  def parse_inventory(self):
    #parse inventory for output of x!inventory (i.e. seperate by rarity)
    pass

class Creature:
  def __init__(self, name, pronoun, creature_id, img_loc, status):
    self.name = name
    self.id = creature_id
    self.img_loc = img_loc
    self.status = status #naughty, either, nice
    self.pronoun = pronoun

class leaderboard:
  def __init__(self, participants):
    self.helpers_list = participants
    self.leaderboard = {}
  
  def calc_lb(self):
    for helper in self.helpers_list:
      self.leaderboard[helper] = helper.calc_score()

  def parse_lb(self):
    #parse leaderboard dictionary for output of x!leaderboard
    pass
