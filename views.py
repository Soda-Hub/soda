from starlette.responses import Response, UJSONResponse as JSONResponse
from models.users import user_manager


async def users(request):
    if request.method == 'GET':
        username = request.query_params.get('username')
        user = await user_manager.get_user(username)

        if user is None:
            return Response('', status_code=404)

        return JSONResponse({'username': user.username})
