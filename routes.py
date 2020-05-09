import views
from starlette.routing import Route


# URL Configuration
routes = [
    Route('/.well-known/webfinger', views.webfinger),
    Route('/users/{username}/inbox', views.user_inbox),
    Route('/users/{username}/output', views.user_output),
    Route('/inbox', views.shared_inbox),
    Route('/users/{username}', views.users),
]
