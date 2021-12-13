import redis
import json
from cryptography.fernet import Fernet

info = {
    "cardnum": 2211849528391929,
    "exp": [2020, 9],
    "cv2": 842,
}

encrypter = Fernet(Fernet.generate_key())

r = redis.Redis(db=3)

r.set("user:1000", encrypter.encrypt(json.dumps(info).encode("utf-8")))

print(r.get("user:1000"))
print(encrypter.decrypt(r.get("user:1000")))
print(json.loads(encrypter.decrypt(r.get("user:1000"))))
