from redis.asyncio import Redis

from app.config import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    # db=int(os.getenv("REDIS_DB", 0)),
    # password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)
