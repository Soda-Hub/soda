from starlette.config import Config


config = Config('.env')
DEBUG = config('DEBUG', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL')
DATABASE_TEST_URL = config('DATABASE_TEST_URL', default=None)
TESTING = config('TESTING', cast=bool, default=False)


if TESTING:
    DATABASE_URL = DATABASE_TEST_URL
