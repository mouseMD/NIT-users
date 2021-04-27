from sanic.response import json
from users.tables import users
from passlib.hash import sha256_crypt
from users.utils import generate_token
from sanic.exceptions import Unauthorized, InvalidUsage


def setup_routes(app):
    @app.post("/user/registry")
    async def register_user(request):
        payload = request.json
        try:
            username = payload['username']
            email = payload['email']
            password = payload['password']
        except KeyError:
            raise InvalidUsage("Invalid message format")

        query = users.insert().values(
            username=username,
            email=email,
            password=sha256_crypt.hash(password)
        )
        await request.app.ctx.db.execute(query)
        return json({}, status=201)

    @app.post("/user/auth")
    async def auth_user(request):
        payload = request.json
        try:
            username = payload['username']
            password = payload['password']
        except KeyError:
            raise InvalidUsage("Invalid message format")
        query = users.select([users.c.id, users.c.password]).where(users.c.username == username)
        row = await request.app.ctx.db.fetch_one(query)
        if row is None:
            raise Unauthorized("Invalid credentials")
        user_id, hash_pass = row[0], row[1]
        if sha256_crypt.verify(password, hash_pass):
            token = await generate_token(user_id)
        else:
            raise Unauthorized("Invalid credentials")
        return json({'user_id': user_id, 'token': token})

    # @app.route("/user/{user_id}")
    # async def get_user(request):
    #     query = users.select()
    #     rows = await request.app.ctx.db.fetch_all(query)
    #     return json({})

    @app.route("/")
    async def test(request):
        query = users.select()
        rows = await request.app.ctx.db.fetch_all(query)
        return json([{'id': row[0], 'username': row[1], 'email': row[2], 'password': row[3]} for row in rows])
