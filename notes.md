1. Introduction & Overview of Redis
What is Redis?

Redis stands for Remote Dictionary Server. It is an open-source, in-memory NoSQL database.

Unlike relational databases (e.g., PostgreSQL, MySQL) or document-based NoSQL databases (e.g., MongoDB), Redis stores data entirely as key-value pairs. Think of Redis as a massive JSON object where every entry has a key and an associated value.

In-Memory vs. Disk Storage:

Standard databases save data to disk drives (HDDs/SSDs).

Redis holds data directly inside working memory (RAM). This makes read and write operations extremely fast (taking milliseconds instead of hundreds of milliseconds or seconds).

Trade-off: RAM is volatile. If the system crashes or loses power, data in RAM can be lost unless saved to disk or backed up regularly.

Primary Use Case:

Redis is primarily used for caching rather than long-term, primary data storage.

In a production app, Redis usually sits in front of a primary database (SQL or MongoDB). Frequently accessed or slow-to-compute data is saved in Redis so subsequent requests bypass the slower primary database.

2. Basic Redis Commands
Redis commands can be written in uppercase or lowercase (uppercase is standard convention).

SET key value

Stores a value under a specified key.

Standard string data type is used for basic key-value storage.

GET key

Retrieves the value stored at key.

DEL key

Deletes the specified key and its associated value.

EXISTS key

Checks if a key exists in the database. Returns 1 if true, 0 if false.

KEYS pattern

Lists all keys matching a pattern. Using KEYS * retrieves all stored keys in the database.

FLUSHALL

Deletes every key across all databases inside the Redis instance (clears the entire cache).

CLEAR

Clears the terminal screen output.

3. Handling Expirations (TTL)
Cache items often need to expire automatically after a set amount of time to ensure fresh data is fetched periodically.

TTL key

Stands for Time to Live. Checks how many seconds remain before a key expires.

Returns -1 if the key has no expiration set (lives forever).

Returns -2 if the key does not exist or has already expired.

EXPIRE key seconds

Sets a countdown timer (in seconds) on an existing key. Once the timer reaches zero, the key is automatically deleted.

SETEX key seconds value

Sets both the key's value and its expiration time (in seconds) in a single atomic command.

4. Lists
Lists in Redis are ordered collections of strings. They act like arrays and are suitable for building queues, stacks, or caching recent activity feeds.

LPUSH key value

Pushes a value onto the left (start/front) of the list.

RPUSH key value

Pushes a value onto the right (end/back) of the list.

LPOP key

Removes and returns the first element from the left side of the list.

RPOP key

Removes and returns the last element from the right side of the list.

LRANGE key start stop

Retrieves a range of elements from the list.

Example: LRANGE key 0 -1 retrieves all items from index 0 to the last item (-1).

5. Sets
Sets are collections of unique, unordered string elements. Duplicate values are automatically rejected.

SADD key value

Adds an element to the set. Returns 1 if the item was added, or 0 if the item was already present in the set.

SMEMBERS key

Returns an array of all members contained in the set.

SREM key value

Removes a specific element from the set.

6. Hashes
Hashes are key-value pairs stored within a key. They represent simple objects (like a user profile), but they cannot be nested deeper than one level.

HSET key field value

Sets the specified field to a given value inside a hash object.

HGET key field

Retrieves the value of a single field from a hash object.

HGETALL key

Retrieves all fields and values stored within the hash key.

HDEL key field

Deletes a specific field from the hash object.

HEXISTS key field

Checks if a field exists inside a hash object. Returns 1 if true, 0 if false.

## Redis — Storing JSON Data -->
Why JSON?
Redis mainly stores values as strings.
If we have a Python dictionary:
product = {
    "name": "Laptop",
    "price": 50000
}
We should convert it to JSON before storing it in Redis.
Python → JSON
Use json.dumps():
import json

json_data = json.dumps(product)
Flow:
Python Dictionary
       ↓
json.dumps()
       ↓
JSON String
       ↓
Redis
Store it:
r.set(
    "product:1",
    json.dumps(product),
    ex=60
)
ex=60 means the cache expires after 60 seconds.
JSON → Python
When getting the data from Redis:
cached_product = r.get("product:1")

product = json.loads(cached_product)
Flow:
Redis
  ↓
JSON String
  ↓
json.loads()
  ↓
Python Dictionary
dumps() vs loads()
Remember:
json.dumps() → Python → JSON
json.loads()  → JSON → Python
Example
import json

product = {
    "name": "Laptop",
    "price": 50000
}

# Python → JSON
data = json.dumps(product)

# JSON → Python
product_again = json.loads(data)
Redis Example
# Store
r.set(
    "product:1",
    json.dumps(product),
    ex=60
)

# Get
cached_product = r.get("product:1")

# Convert JSON back to Python
product = json.loads(cached_product)
Simple Mental Model
Python Dictionary
       ↓
  json.dumps()
       ↓
   Redis Cache
       ↓
   json.loads()
       ↓
Python Dictionary
Use JSON when storing structured Python data such as dictionaries or API responses in Redis.

# Redis Caching Patterns

## 1. Cache Invalidation

**Cache invalidation** means removing or updating old data from the cache when the original data changes.

### Why?
Redis may contain **stale (old) data**.

### Example

```text
Database → Laptop ₹55,000
Redis    → Laptop ₹50,000 ❌

## Cache-Aside Pattern

Cache-aside means the application checks Redis first. If the data is not there, it gets it from the database and stores it in Redis.
Flow
Request
   ↓
Check Redis
   ↓
 ┌──────┴──────┐
 ↓             ↓
HIT           MISS
 ↓             ↓
Return      Database
              ↓
            Redis
              ↓
            Return
Cache HIT
Data exists in Redis:
Request → Redis → Return ⚡
Cache MISS
Data doesn't exist:
Request → Redis ❌ → Database → Redis → Return
Remember
Check Redis → If missing, get from DB → Store in Redis → Return.

