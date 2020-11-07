from enum import IntEnum
from dtos.creature import CreatureDto
from dtos.item import ItemDto

DISCORD_CLIENT_ID = '773308497538056222'
DISCORD_TOKEN = 'not again'

DEFAULT_DESPAWN_TIME_SECONDS = 10
DEFAULT_SPAWN_RATE_PERCENT = 100

class ChristmasColor(IntEnum):
  RED = 0xBB2528
  GREEN = 0x146B3A
  GOLD = 0xF8B229
  WHITE = 0xFFFFFF


image_maindir = '/res/' #change this
image_chardir = image_maindir + 'CHARS/'
image_orndir = image_maindir + 'ORNAMENTS/'

###Item list:
##ORNAMENTS:
GUMDROP_ORN = ItemDto(None, 'Gumdrop Ornament', 'https://i.imgur.com/1CnajlU.png', 'rare')

##SPECIAL:
ICED_BOWTIE = ItemDto(None, 'Iced Bowtie', 'https://i.imgur.com/1CnajlU.png', 'special')

##COMMON:
DASH_OF_CINNAMON = ItemDto(None, 'Dash of Cinnamon', 'https://i.imgur.com/1CnajlU.png', 'common')

NICE_GINGY_ITEMS = [GUMDROP_ORN, ICED_BOWTIE]
NAUGHTY_GINGY_ITEMS = [DASH_OF_CINNAMON, ICED_BOWTIE]

###Creature list:

CREATURE_LIST = []

##NICE CREATURES
#NICE_GINGY
CREATURE_LIST.append(CreatureDto(None, 'Nice Gingy', 'she', 'https://i.imgur.com/MBmsrHG.png', 'nice', NICE_GINGY_ITEMS))

##NAUGHTY CREATURES
#NAUGHTY_GINGY
CREATURE_LIST.append(CreatureDto(None, 'Naughty Gingy', 'he', 'https://i.imgur.com/1CnajlU.png', 'naughty', NAUGHTY_GINGY_ITEMS))