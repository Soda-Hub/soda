import views
from starlette.routing import Route


# URL Configuration
routes = [
    Route('/.well-known/webfinger', views.webfinger),
    Route('/users/{username}', views.users),
]
