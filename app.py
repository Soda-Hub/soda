from starlette.applications import Starlette
from starlette.routing import Route
from starlette.config import Config
from views import home


config = Config('.env')
DEBUG = config('DEBUG', cast=bool, default=False)


app = Starlette(debug=DEBUG, routes=[
    Route('/', home),
])

