import redis
import logging
from pyhats.src import pyhats, redis_test

def main():
    redis_test.main()
    pyhats.initialise_stock()
    pyhats.test_purchase()
    pyhats.test_purchase_all()
    # pyhats.test_purchase_another()
    redis_test.key_expiry()

    #
    r = redis.Redis(db=5)
    watcher = pyhats.IPWatcher(r)
    watcher.watch()

if __name__ == "__main__":
    main()
