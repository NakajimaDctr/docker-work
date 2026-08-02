# 05. ネットワーキング - 実習メモ

[docs/05-networking/README.md](../../docs/05-networking/README.md) の手順に沿って、以下のコマンドを実際に実行してください。このディレクトリ自体にはコードはなく、コマンド操作の練習が中心です。

## 実行するコマンド一覧

```bash
# 1. ネットワークなしで失敗を体験する
docker run -d --name web nginx
docker run --rm alpine wget -qO- --timeout=3 http://web
# → Connection refused のエラーになるはず(docs/05のREADMEの補足も参照)

# 後片付け
docker rm -f web

# 2. ユーザー定義ネットワークを作成する
docker network create my-net
docker network ls

# 3. 同じネットワークで再実行する
docker run -d --name web --network my-net nginx
docker run --rm --network my-net alpine ping -c 3 web
# → 今度は成功するはず

# 4. HTTP通信も試す
docker run --rm --network my-net alpine wget -qO- http://web

# 5. ネットワーク詳細を確認する
docker network inspect my-net

# 6. 後片付け
docker rm -f web
docker network rm my-net
```

## メモ欄

- `ping`が失敗した理由 / 成功した理由:
- `docker network inspect my-net` で確認した `web` のIPアドレス:
- その他気づいたこと:
