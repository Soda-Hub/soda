from json import JSONDecodeError
from starlette.responses import Response, UJSONResponse as JSONResponse
from responses import ActivityJSONResponse
from settings import ALLOWED_HOSTS
from models.users import user_manager
from serializers.webfinger import WebFingerSchema
from serializers.actpub.users import MediaSchema, PublicKeySchema, UserSchema


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


async def users(request):
    if request.method == 'GET':
        username = request.path_params['username']
        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        user_schema = UserSchema()
        resp = user_schema.dump(user)

        return ActivityJSONResponse(resp)


async def user_inbox(request):
    # Handle Follow requests
    # {"@context":"https://www.w3.org/ns/activitystreams","id":"https://mastodon.social/99a04493-0cdd-4912-8831-322f87fc0ec0","type":"Follow","actor":"https://mastodon.social/users/victorneo","object":"https://sodahub.cheshire.io/users/victor6"}
    username = request.path_params['username']

    try:
        req = await request.json()
    except JSONDecodeError:
        return Response('', status_code=400)

    req_id = req['id']
    req_type = req['type']

    if req_type == 'Follow':
        actor = req['actor']
        followee = req['object']

    return Response('')


async def user_outbox(request):
    print(request.path_params['username'])
    resp = await request.body()
    print(resp.decode())
    return Response('')


async def shared_inbox(request):
    resp = await request.body()
    print(resp.decode())
    return Response('')
