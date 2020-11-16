from daos.abstract_dao import AbstractDao
from daos.db_dao import DbDao

dao = None


def get_dao() -> AbstractDao:
  global dao
  if dao is None:
    dao = DbDao()
  return dao