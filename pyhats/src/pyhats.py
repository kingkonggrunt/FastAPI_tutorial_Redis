import redis
import logging
import random

# Redis tutorial @ https://realpython.com/python-redis

# PyHats.com Example
def initialise_stock():
    random.seed(444)
    hats = {
    f"hat:{random.getrandbits(32)}":{
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    f"hat:{random.getrandbits(32)}":{
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    f"hat:{random.getrandbits(32)}":{
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    },
    }

    r = redis.Redis(db=1)

    with r.pipeline() as pipe:
        for h_id, h_char in hats.items():
            pipe.hmset(h_id, h_char)
        pipe.execute()

    r.bgsave()

    print(r.hgetall("hat:56854717"))

    # Purchase hat:56854717
    r.hincrby("hat:56854717", "quantity", -1)
    r.hincrby("hat:56854717", "npurchased", 1)
    print(r.hget("hat:56854717", "quantity"))
    print(r.hget("hat:56854717", "npurchased"))

class OutofStockError(Exception):
    """Raised when PyHats.com is all out of stock"""

logging.basicConfig()
def buyitem(r: redis.Redis, itemid: int) -> None:
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                pipe.watch(itemid)  # optimistic locking
                nleft: bytes = r.hget(itemid, "quantity")
                if nleft > b"0":
                    pipe.multi()  # transaction block
                    pipe.hincrby(itemid, "quantity", -1)
                    pipe.hincrby(itemid, "npurchased", 1)
                    pipe.execute()  # execute trans.block
                    break
                else:
                    pipe.unwatch()
                    raise OutofStockError(
                    "Sorry, {} is out of stock".format(itemid)
                    )
            except redis.WatchError:
                error_count += 1
                logging.warning(
                "WatchError {}: {}; retyring".format(error_count, itemid)
                )
    return None

def test_purchase():
        r = redis.Redis(db=1)
        buyitem(r, "hat:56854717")
        buyitem(r, "hat:56854717")
        buyitem(r, "hat:56854717")
        print(r.hmget("hat:56854717", "quantity", "npurchased"))

def test_purchase_all():
    r = redis.Redis(db=1)
    for _ in range(196):
        buyitem(r, "hat:56854717")
        print(r.hmget("hat:56854717", "quantity", "npurchased"))

def test_purchase_another():
    r = redis.Redis(db=1)
    buyitem(r, "hat:56854717")
