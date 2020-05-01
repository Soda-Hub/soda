from starlette.responses import JSONResponse


async def home(request):
    return JSONResponse({'hello': 'world'})
