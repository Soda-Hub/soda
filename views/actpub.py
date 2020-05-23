from json import JSONDecodeError
from starlette.responses import Response, UJSONResponse as JSONResponse
from responses import ActivityJSONResponse
from settings import ALLOWED_HOSTS
from models.users import user_manager, follow_manager
from serializers.actpub.users import MediaSchema, PublicKeySchema, UserSchema
from serializers.actpub.follows import FollowSchema


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
    username = request.path_params['username']

    try:
        req = await request.json()
    except JSONDecodeError:
        return Response('', status_code=400)

    user = await user_manager.get_user(username)
    if user is None:
        return Response('', status_code=404)

    if req['type'] == 'Follow':
        schema = FollowSchema()
        follow = schema.load(req)
        actor = req['actor']
        followee = req['object']

        remote_user = await user_manager.get_or_add_remote_user(actor)

        await follow_manager.add_following(remote_user.id, user.id)

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
