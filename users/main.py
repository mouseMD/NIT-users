from sanic import Sanic
from environs import Env
from users.settings import setup_config
from databases import Database
from users.routes import setup_routes
from aiohttp import ClientSession

app = Sanic(__name__)


@app.listener('before_server_start')
def init_connection(app, loop):
    app.ctx.users_session = ClientSession(loop=loop)


@app.listener('after_server_stop')
def close_connection(app, loop):
    loop.run_until_complete(app.ctx.users_session.close())
    loop.close()


def setup_database():
    app.ctx.db = Database(app.config.DB_URL)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await app.ctx.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.ctx.db.disconnect()


def init():
    env = Env()
    env.read_env()

    setup_config(app, env)
    setup_database()
    setup_routes(app)
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG
    )
