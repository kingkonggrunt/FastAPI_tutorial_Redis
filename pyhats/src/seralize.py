import redis
import json

restaurant_484272 = {
    "name": "Ravagh",
    "type": "Persian",
    "address": {
        "street": {
            "line1": "11 E 30th St",
            "line2": "APT 1",
        },
        "city": "New York",
        "state": "NY",
        "zip": 10016,
    }
}

# By Design, Redis Hash doesn't support nested dictionaries
# Solution is to convert a python nested dictionary into a
# binary/string object

r = redis.Redis(db=4)
r.set(484272, json.dumps(restaurant_484272))
print(json.loads(r.get(484272)))  # PyYAML also works
