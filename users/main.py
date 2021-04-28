from sanic import Sanic
from environs import Env
from users.settings import setup_config
from databases import Database
from users.routes import setup_routes
from aiohttp import ClientSession

app = Sanic(__name__)


def setup_database():
    app.ctx.db = Database(app.config.DB_URL)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await app.ctx.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.ctx.db.disconnect()


def setup_offers_connection():
    app.ctx.offers_session = ClientSession()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.ctx.offers_session.close()


def init():
    env = Env()
    env.read_env()

    setup_config(app, env)
    setup_database()
    setup_offers_connection()
    setup_routes(app)
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG
    )
