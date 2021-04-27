import jwt
from datetime import datetime, timedelta

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_SEC = 60


async def generate_token(user_id):
    expiration_time = (datetime.utcnow() + timedelta(JWT_EXPIRATION_SEC)).strftime("%d-%b-%Y (%H:%M:%S.%f)")
    token = jwt.encode({'user_id': user_id, 'exp_time': expiration_time}, JWT_SECRET)
    return token
