from starlette.responses import Response, UJSONResponse as JSONResponse
from responses import ActivityJSONResponse
from settings import ALLOWED_HOSTS
from models.users import user_manager


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

        resp = {
            'subject': 'acct:' + acct,
            'links': [{
                'rel': 'self',
                'type': 'application/activity+json',
                'href': 'https://' + ALLOWED_HOSTS[0] +
                        '/users/' + user.username
                }],
        }

        return JSONResponse(resp)


async def users(request):
    if request.method == 'GET':
        username = request.path_params['username']
        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        domain = 'https://' + ALLOWED_HOSTS[0]
        user_url = domain + '/users/' + user.username

        resp = {
            '@context': [
                'https://www.w3.org/ns/activitystreams',
                'https://w3id.org/security/v1'
            ],
            'id': user_url,
            'type': 'Person',
            'preferredUsername': user.username,
            'inbox': user_url + '/inbox',
            'outbox': user_url + '/outbox',
            'followers': user_url + '/followers',
            'endpoints': {
                'sharedInbox': domain + '/inbox'
            },
            'name': user.username,
            'icon': {'mediaType': 'image/jpg', 'type': 'icon',
                     'url': domain + '/static/images/profile_small.jpg'},
            'publicKey': {
                'id': user_url + '#main-key',
                'owner': user_url,
                'publicKeyPem': user.pub_key
            }
        }

        return ActivityJSONResponse(resp)


async def user_inbox(request):
    print(request.path_params['username'])
    resp = await request.body()
    print(resp.decode())
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
