# Kache

An in-memory key-value store with LRU eviction, configurable capacity,
per-key TTL, and a REST API.

## Architecture

Core: HashMap + Doubly Linked List — O(1) get, set, and eviction.
TTL expiry uses lazy deletion (checked on GET, not on a background thread).
Capacity is configurable via the MAX_KEYS environment variable.

## Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| PUT    | /cache/{key}      | Set a value, optional TTL (seconds)|
| GET    | /cache/{key}      | Get a value (404 if missing/expired)|
| DELETE | /cache/{key}      | Manually evict a key               |
| GET    | /cache/stats      | Hit rate, miss rate, eviction count|
| DELETE | /cache/_flush     | Clear the entire cache             |

## Complexity

| Operation | Time  | Reason                              |
|-----------|-------|-------------------------------------|
| get()     | O(1)  | HashMap lookup + DLL pointer move   |
| set()     | O(1)  | HashMap insert + DLL head insert    |
| evict()   | O(1)  | DLL tail removal + HashMap delete   |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload