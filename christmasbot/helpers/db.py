from sqlalchemy import Table, Column, Integer, ARRAY, Text, MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey

from constants.globals import DB_CONFIG
from dtos.creature import CreatureDto
from dtos.item import ItemDto
from dtos.player import PlayerDto
from dtos.server_config import ServerConfigDto


engine = None
session_maker = None

meta = MetaData(schema='beta')

servers_table = Table('servers', meta, 
  Column('id', Integer, primary_key=True),
  Column('enabled_channels', ARRAY(Integer)),
  Column('items', ARRAY(Text)),
  Column('despawn_time', Integer),
  Column('spawn_rate_percent', Integer)
)

players_table = Table('players', meta,
  Column('server_id', Integer, ForeignKey('servers.id'), primary_key=True),
  Column('player_id', Integer, primary_key=True),
  Column('inventory', ARRAY(Text)),
  Column('coal_count', Integer),
  Column('score', Integer)
)

creatures_table = Table('creatures', meta,
  Column('id', Text, primary_key=True),
  Column('display_name', Text),
  Column('img_url', Text),
  Column('status', Text),
  Column('pronoun', Text),
  Column('items', ARRAY(Text))
)

items_table = Table('items', meta,
  Column('id', Text, primary_key=True),
  Column('display_name', Text),
  Column('img_url', Text),
  Column('rarity', Integer)
)

def init_engine():
  global engine, session_maker
  if engine is None:
    engine = create_engine(DB_CONFIG)
    session_maker = sessionmaker(bind=engine)
    meta.bind = engine
    mapper(ServerConfigDto, servers_table)
    mapper(PlayerDto, players_table),
    mapper(CreatureDto, creatures_table)
    mapper(ItemDto, items_table)

def get_session() -> Session:
  return session_maker()