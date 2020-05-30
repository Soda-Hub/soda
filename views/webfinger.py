from starlette.responses import Response, UJSONResponse as JSONResponse
from models.users import user_manager
from settings import ALLOWED_HOSTS
from serializers.webfinger import WebFingerSchema


async def webfinger(request):
    if request.method == 'GET':
        acct = request.query_params.get('resource', None)
        if not acct:
            return Response('', status_code=400)

        acct = acct.replace('acct:', '')
        username, domain = acct.split('@')

        if domain not in ALLOWED_HOSTS:
            return Response('', status_code=404)

        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        schema = WebFingerSchema()
        resp = schema.dump(user)

        return JSONResponse(resp)


