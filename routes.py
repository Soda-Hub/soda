import views
from starlette.routing import Route


# URL Configuration
routes = [
    Route('/', views.users),
]
