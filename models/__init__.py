from .meta import *
from .users import *


from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database


engine = create_engine(db_url)
create_database(db_url)
metadata.create_all(engine)
