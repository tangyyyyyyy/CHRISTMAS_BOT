from daos.abstract_dao import AbstractDao
from daos.cached_db_dao import CachedDbDao
from daos.db_dao import DbDao
from daos.memory_dao import MemoryDao

dao = None


def get_dao() -> AbstractDao:
  global dao
  if dao is None:
    dao = CachedDbDao()
  return dao