import hashlib
import json
from typing import Any, Protocol

from redis.asyncio import Redis


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
    
    async def set_cache(self, value: Any, key: str, ttl: int) -> None:
        data = json.dumps(value)
        await self.client.set(key, data, ex=ttl)

    def get_key(self, prefix: str, params: Any) -> str:
        raw = json.dumps(params, sort_keys=True)
        return f"{prefix}:{hashlib.md5(raw.encode()).hexdigest()}"



