from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.lru_cache import LRUCache

router = APIRouter()

# Single shared cache instance — lives for the lifetime of the process
cache = LRUCache()

class SetRequest(BaseModel):
    value: str
    ttl: Optional[int] = None   # seconds; None = never expires

@router.put('/{key}', status_code=200)
def set_key(key: str, body: SetRequest):
    cache.set(key, body.value, body.ttl)
    return {'key': key, 'status': 'ok'}

@router.get('/stats')
def get_stats():
    return cache.stats()

@router.get('/{key}')
def get_key(key: str):
    value = cache.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail='Key not found or expired')
    return {'key': key, 'value': value}

@router.delete('/{key}')
def delete_key(key: str):
    deleted = cache.delete(key)
    if not deleted:
        raise HTTPException(status_code=404, detail='Key not found')
    return {'key': key, 'status': 'deleted'}

@router.delete('/_flush', status_code=200)
def flush_cache():
    cache.map.clear()
    cache.dll.__init__()
    return {'status': 'cache cleared'}