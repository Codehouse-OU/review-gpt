import os
import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from webservice.chatgpt.chatgpt import ChatGptService as chat_gpt
from webservice.configuration.configuration import Configuration as config

routes = web.RouteTableDef()

router = routing.Router()


@router.register("pull_request", action="opened")
async def pr_opened_event(event, gh, *args, **kwargs):
    url = event.data["pull_request"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]
    diff_url = event.data["pull_request"]["diff_url"]
    code_diff = await gh.post(diff_url)
    chat_gpt.generate_response(code_diff=code_diff)

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})

@router.register("ping")
async def ping(event, gh, *args, **kwargs):
    res = 1 + 1



@routes.post("/")
async def main(request):
    body = await request.read()

    event = sansio.Event.from_http(request.headers, body, secret=config.secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, config.user, oauth_token=config.oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)