class item:
  def __init__(self, name, ID, imgLoc, rarity):
    self.name = name
    self.itemID = ID
    self.imgLoc = imgLoc
    self.rarity = rarity #str


class helper: 
  def __init__(self, name, ID):
    self.inventory = [] #list of items
    self.discordID = ID
    self.name = name
    self.coalCount = 0
    self.score = 0

  def calcScore(self):
    self.score = len(self.inventory) - self.coalCount

  def foundItem(self, item):
    self.inventory.append(item)

  def foundCoal(self):
    #replace an item in inventory with coal
    pass

  def parseInventory(self):
    #parse inventory for output of x!inventory (i.e. seperate by rarity)
    pass

class creature:
  def __init__(self, name, ID, imgLoc, status):
    self.name = name
    self.creatureID = ID
    self.imgLoc = imgLoc
    self.status = status #naughty, either, nice

class leaderboard:
  def __init__(self, participants):
    self.helpers_list = participants
    self.leaderboard = {}
  
  def calcLeaderBoard(self):
    for helper in self.helpers_list:
      self.leaderboard[helper] = helper.calcScore

  def parseLeaderBoard(self):
    #parse leaderboard dictionary for output of x!leaderboard
    pass
