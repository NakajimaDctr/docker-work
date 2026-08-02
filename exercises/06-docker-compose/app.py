import time

import redis
from flask import Flask

app = Flask(__name__)

# サービス名 "redis" がそのままホスト名として名前解決される(docker-compose.ymlのservices名)
r = redis.Redis(host="redis", port=6379, decode_responses=True)


def get_redis_connection(retries=10, delay=1):
    for attempt in range(1, retries + 1):
        try:
            r.ping()
            return
        except redis.exceptions.ConnectionError:
            print(f"Redisへの接続待機中... ({attempt}/{retries})")
            time.sleep(delay)
    raise RuntimeError("Redisに接続できませんでした")


@app.route("/")
def index():
    get_redis_connection()
    count = r.incr("hits")
    return f"このページは合計 {count} 回アクセスされました。\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
