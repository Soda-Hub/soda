from json import JSONDecodeError
from starlette.responses import Response, UJSONResponse as JSONResponse
from responses import ActivityJSONResponse
from settings import ALLOWED_HOSTS
from models.users import user_manager, follow_manager
from serializers.actpub.users import MediaSchema, PublicKeySchema, UserSchema
from serializers.actpub.follows import (
        FollowSchema, FollowerSummarySchema, FollowerSchema)
from .activities import ActivityType, get_activity_type


async def users(request):
    if request.method == 'GET':
        username = request.path_params['username']
        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        user_schema = UserSchema()
        resp = user_schema.dump(user)

        return ActivityJSONResponse(resp)


async def user_followers(request):
    # Handle Follow requests
    username = request.path_params['username']
    page = int(request.query_params.get('page', 0))
    user = await user_manager.get_user(username)

    if user is None:
        return Response('', status_code=404)

    follower_count = await follow_manager.get_follower_count(user.id)

    if page <= 0:
        schema = FollowerSummarySchema()
        first = username + '/followers?page=1'
        resp = schema.dump({'totalItems': follower_count, 'first': first})
    elif page >= 1:
        followers = await follow_manager.get_followers(user.id, page)
        schema = FollowerSchema()
        url = username + '/followers'
        print(followers)
        resp = schema.dump({'url': url, 'followers': [f[0] for f in followers],
            'page': page, 'totalItems': follower_count})

    return ActivityJSONResponse(resp)


async def user_inbox(request):
    # Handle Follow requests
    username = request.path_params['username']

    user = await user_manager.get_user(username)
    if user is None:
        return Response('', status_code=404)

    if request.method == 'GET':
        return Response('')

    try:
        req = await request.json()
    except JSONDecodeError:
        return Response('', status_code=400)

    act_type = get_activity_type(req)

    if act_type == ActivityType.FOLLOW:
        schema = FollowSchema()
        follow = schema.load(req)
        actor = req['actor']
        followee = req['object']
        remote_user = await user_manager.get_or_add_remote_user(actor)
        await follow_manager.add_following(remote_user.id, user.id)
    elif act_type == ActivityType.UNDO:
        act_type = get_activity_type(req['object'])
        if act_type == ActivityType.FOLLOW:
            schema = FollowSchema()
            follow = schema.load(req['object'])
            actor = req['object']['actor']
            followee = req['object']['object']

            remote_user = await user_manager.get_or_add_remote_user(actor)
            await follow_manager.remove_following(remote_user.id, user.id)

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
