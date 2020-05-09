from starlette.responses import UJSONResponse


class ActivityJSONResponse(UJSONResponse):
    media_type = 'application/activity+json'
