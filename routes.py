from views import actpub, webfinger
from starlette.routing import Route


# URL Configuration
routes = [
    Route('/.well-known/webfinger', webfinger.webfinger),
    Route('/users/{username}/inbox', actpub.user_inbox, methods=['POST']),
    Route('/users/{username}/outbox', actpub.user_outbox),
    Route('/users/{username}/followers', actpub.user_followers, methods=['GET']),
    Route('/users/{username}', actpub.users),
    Route('/inbox', actpub.shared_inbox, methods=['POST']),
    Route('/outbox', actpub.shared_inbox),
]
