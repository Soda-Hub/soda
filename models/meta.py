from settings import DATABASE_URL
from databases import Database
import sqlalchemy


metadata = sqlalchemy.MetaData()
db_url = str(DATABASE_URL)
database = Database(db_url)
database.connect()
