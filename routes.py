import views
from starlette.routing import Route


# URL Configuration
routes = [
    Route('/.well-known/webfinger', views.webfinger),
    Route('/users/{username}/inbox', views.user_inbox),
    Route('/users/{username}/outbox', views.user_outbox),
    Route('/users/{username}', views.users),
    Route('/inbox', views.shared_inbox),
    Route('/outbox', views.shared_inbox),
]
