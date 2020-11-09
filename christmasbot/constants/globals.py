from enum import IntEnum
from dtos.creature import CreatureDto
from dtos.item import ItemDto

DISCORD_CLIENT_ID = '773308497538056222'
DISCORD_TOKEN = ':)notthistime'

DEFAULT_DESPAWN_TIME_SECONDS = 10
DEFAULT_SPAWN_RATE_PERCENT = 100

class ChristmasColor(IntEnum):
  RED = 0xBB2528
  GREEN = 0x146B3A
  GOLD = 0xF8B229
  WHITE = 0xFFFFFF
