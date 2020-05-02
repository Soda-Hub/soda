from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings


config = Config('.env')
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
DATABASE_URL = config('DATABASE_URL')
DATABASE_TEST_URL = config('DATABASE_TEST_URL', default=None)
TESTING = config('TESTING', cast=bool, default=False)


if TESTING:
    DATABASE_URL = DATABASE_TEST_URL
