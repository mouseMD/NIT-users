from sanic.response import json
from users.tables import users_table
from passlib.hash import sha256_crypt
from users.utils import generate_token
from sanic.exceptions import Unauthorized, InvalidUsage
from asyncpg.exceptions import UniqueViolationError


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

        query = users_table.insert().values(
            username=username,
            email=email,
            password=sha256_crypt.hash(password)
        )
        try:
            await request.app.ctx.db.execute(query)
        except UniqueViolationError:
            raise InvalidUsage("User already exists")   # or 409?
        return json({}, status=201)

    @app.post("/user/auth")
    async def auth_user(request):
        payload = request.json
        try:
            username = payload['username']
            password = payload['password']
        except KeyError:
            raise InvalidUsage("Invalid message format")
        #query = users.select([users.c.id, users.c.password]) #.where(users.c.username == 'user')
        query = users_table.select().where(users_table.c.username == username)
        row = await request.app.ctx.db.fetch_one(query)
        if row is None:
            raise Unauthorized("Invalid credentials")
        user_id, hash_pass = row[0], row[3]
        if sha256_crypt.verify(password, hash_pass):
            token = await generate_token(user_id)
        else:
            raise Unauthorized("Invalid credentials")
        return json({'user_id': user_id, 'token': token})

    @app.get("/user/<user_id:int>")
    async def get_user(request, user_id):
        query = users_table.select().where(users_table.c.id == user_id)
        row = await request.app.ctx.db.fetch_one(query)
        if row is None:
            raise InvalidUsage("Invalid user_id")

        # request to offers
        offers_url = request.app.config.OFFERS_URL
        payload = json({"user_id": user_id})
        headers = {'content-type': 'application/json'}
        offers = []
        async with request.app.ctx.offers_session.post(offers_url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                offers = await resp.json()
        return json({"user_info": {"username": row[1], "email": row[2]}, "offers": offers})
