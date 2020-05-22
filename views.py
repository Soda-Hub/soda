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
        resp = schema.dump({'subject': 'acct:' + acct,
                            'links': 'https://' + ALLOWED_HOSTS[0] +
                                     '/users/' + user.username})

        return JSONResponse(resp)


async def users(request):
    if request.method == 'GET':
        username = request.path_params['username']
        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        domain = 'https://' + ALLOWED_HOSTS[0]
        user_url = domain + '/users/' + user.username

        media_schema = MediaSchema()
        pk_schema = PublicKeySchema()
        user_schema = UserSchema()

        icon = media_schema.dump({
            'mediaType': 'image/jpg', 'type': 'icon',
            'url': domain + '/static/images/profile_small.jpg'})

        pk = pk_schema.dump({
                'id': user_url + '#main-key',
                'owner': user_url,
                'publicKeyPem': user.pub_key})

        resp = user_schema.dump({
            'id': user_url,
            'preferredUsername': user.username,
            'inbox': user_url + '/inbox',
            'outbox': user_url + '/outbox',
            'followers': user_url + '/followers',
            'endpoints': {
                'sharedInbox': domain + '/inbox'
            },
            'name': user.username,
            'icon': icon,
            'publicKey': pk
        })

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
