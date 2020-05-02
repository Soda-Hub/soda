from starlette.responses import Response, UJSONResponse as JSONResponse
from settings import ALLOWED_HOSTS
from models.users import user_manager


async def webfinger(request):
    if request.method == 'GET':
        acct = request.query_params.get('resource', None)
        if not acct:
            return Response('', status_code=400)

        parts = acct.split('@')
        username = parts[0]
        domain = parts[1]

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

        headers = {'content-type': 'application/activity+json'}
        return JSONResponse(resp, headers=headers)


async def users(request):
    if request.method == 'GET':
        username = request.path_params['username']
        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        domain = ALLOWED_HOSTS[0]
        url = 'https://' + domain + '/users/'+ user.username

        resp = {
            '@context': [
                'https://www.w3.org/ns/activitystreams',
                'https://w3id.org/security/v1'
            ],
            'id': url,
            'type': 'Service',
            'preferredUsername': user.username,
            'inbox': 'https://'+ domain + '/inbox',
            'followers': url + '/followers',
            'name': user.username,
            'publicKey': {
                'id': url + '#main-key',
                'owner': url,
                'publicKeyPem': user.pub_key
            }
        }

        headers = {'content-type': 'application/activity+json'}
        return JSONResponse(resp, headers=headers)
