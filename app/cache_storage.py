import hashlib
import json
from typing import Any, Protocol

from redis.asyncio import Redis
from datetime import datetime, timedelta


class CacheStorage(Protocol):
    async def get_cache(self, key: str) -> Any:
        pass

    async def set_cache(self, value: Any, key: str, ttl: int) -> None:
        pass

    def get_key(self, prefix: str, params: Any) -> str:
        pass


class RedisCacheStorage:
    def __init__(self, client: Redis):
        self.client = client

    async def get_cache(self, key: str) -> Any:
        data = await self.client.get(key)
        if data is None:
            return None
        return json.loads(data)
    
    async def set_cache(self, key: str, value: Any, ex: int) -> None:
        await self.client.set(key, value, ex=ex)

    def get_key(self, prefix: str, params: Any) -> str:
        raw = json.dumps(params, sort_keys=True)
        return f"{prefix}:{hashlib.md5(raw.encode()).hexdigest()}"



def get_date_for_prefix(date: dict[str:datetime]) -> str:
    start_date = date["start_date"].strftime("%Y.%m.%d.%H:%M")
    end_date = date["end_date"].strftime("%Y.%m.%d.%H:%M")

    return f"{start_date}-{end_date}"

def get_ttl() -> int:

    hour = 14
    minutes = 59

    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(hour=hour, minute=minutes)
    ttl = int((tomorrow - now).total_seconds())

    return ttl

