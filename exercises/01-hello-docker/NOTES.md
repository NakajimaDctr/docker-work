# 01. Hello Docker - 実習メモ

[docs/01-containers-and-images/README.md](../../docs/01-containers-and-images/README.md) の手順に沿って、以下のコマンドを実際に実行してください。このディレクトリ自体にはコードはなく、コマンド操作の練習が中心です。

## 実行するコマンド一覧

```bash
# イメージを取得する
docker pull nginx

# イメージ一覧を確認する
docker images

# コンテナを起動する
docker run -d --name my-nginx -p 8080:80 nginx

# 起動確認
docker ps

# ブラウザ or curl で確認
curl http://localhost:8080

# 同じイメージからもう1つ起動する
docker run -d --name my-nginx-2 -p 8081:80 nginx
docker ps

# 後片付け
docker stop my-nginx my-nginx-2
docker rm my-nginx my-nginx-2
```

## メモ欄

実行した結果や気づいたことを、ここに自分の言葉で書き残しておきましょう(例: イメージのサイズ、起動にかかった時間、エラーが出た場合はその内容など)。
