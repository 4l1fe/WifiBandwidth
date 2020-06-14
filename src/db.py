from peewee import SqliteDatabase
from playhouse.dataset import DataSet


DATA_DIR = '../data'


db = DataSet(SqliteDatabase(DATA_DIR + '/bandwidth.sqlite'))
tresults = db['test-results']
