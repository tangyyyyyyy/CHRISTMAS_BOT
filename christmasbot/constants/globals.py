from enum import IntEnum

from sqlalchemy.engine.url import URL

DISCORD_CLIENT_ID = '773308497538056222'
DISCORD_TOKEN = 'rawrxDhaha'

BLOB_URL = 'https://i.imgur.com/3SdgfhJ.png'

DEFAULT_DESPAWN_TIME_SECONDS = 10
DEFAULT_SPAWN_RATE_PERCENT = 100

DB_CONFIG = URL(
  drivername='postgres+psycopg2',
  username='zoo',
  password='wee',
  host='mama',
  port=5432,
  database='christmasbot'
)


class ChristmasColor(IntEnum):
  RED = 0xBB2528
  GREEN = 0x146B3A
  GOLD = 0xF8B229
  WHITE = 0xFFFFFF


ongoing_spawns = None

def get_ongoing_spawns():
  global ongoing_spawns
  if ongoing_spawns is None:
    ongoing_spawns = {}
  return ongoing_spawns