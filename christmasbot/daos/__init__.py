from daos.abstract_dao import AbstractDao
from daos.memory_dao import MemoryDao

dao = None


def get_dao() -> AbstractDao:
  global dao
  if dao is None:
    dao = MemoryDao()
  return dao