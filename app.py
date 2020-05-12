from starlette.applications import Starlette

import settings


# Database initialization
import models


# Application views
import routes


# Initialise Starlette
app = Starlette(debug=settings.DEBUG, routes=routes.routes)
