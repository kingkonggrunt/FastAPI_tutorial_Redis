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
