from sanic.response import json
from users.tables import users


def setup_routes(app):
    @app.route("/user/registry")
    async def register_user(request):
        query = users.select()
        rows = await request.app.ctx.db.fetch_all(query)
        return json({})
    #
    # @app.route("/user/auth")
    # async def auth_user(request):
    #     query = users.select()
    #     rows = await request.app.ctx.db.fetch_all(query)
    #     return json({})
    #
    # @app.route("/user/{user_id}")
    # async def get_user(request):
    #     query = users.select()
    #     rows = await request.app.ctx.db.fetch_all(query)
    #     return json({})

    @app.route("/")
    async def test(request):
        query = users.select()
        rows = await request.app.ctx.db.fetch_all(query)
        return json({})
