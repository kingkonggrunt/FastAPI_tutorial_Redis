import redis

def main():
    r = redis.Redis()

    r.mset({"Croatia":"Zagreb", "Bahamas": "Nassau"})
    r.get("Bahamas")

    ## Allowed Key Types are bytes, str, int or float
    import datetime
    today = datetime.date.today().isoformat()  # date to string
    vistors = {"dan", "jon", "alex"}
    r.sadd(today, *vistors)
    r.smembers(today)
    r.scard(today)

def key_expiry():
        # Setting string:string key-value pairs with an expiration date
    from datetime import timedelta
    r = redis.Redis(db=1)
    r.setex("runner", timedelta(minutes=1), value="now you see me")

def push_ips():
    r = redis.Redis(db=5)
    r.lpush("ips", "51.218.112.236")
    r.lpush("ips", "90.213.45.98")
    r.lpush("ips", "115.215.230.176")
    r.lpush("ips", "51.218.112.236")

def bot_attack():
    r = redis.Redis(db=5)
    for _ in range(20):
        r.lpush("ips", "104.174.118.18")
