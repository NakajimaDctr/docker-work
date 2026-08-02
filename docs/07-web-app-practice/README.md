# 07. 総合実践: Webアプリ構築

## この章で学ぶこと

- これまで学んだ知識(Dockerfile、ボリューム、ネットワーク、Compose)を組み合わせ、実際に動くWebアプリを構築する
- Flask(Webアプリ)+ PostgreSQL(DB)という、実務でもよくある構成をDocker化する
- データがボリュームに永続化されていることを確認する

## 概念解説

ここまでの章で学んだ要素を1つに組み合わせます。

| これまで学んだこと | この章での使いどころ |
|---|---|
| Dockerfile(03章) | Flaskアプリをイメージ化する |
| ボリューム(04章) | PostgreSQLのデータを永続化する |
| ネットワーク(05章) | web ↔ db 間の通信 |
| Compose(06章) | 上記全部を1つの`docker-compose.yml`にまとめる |

構成イメージ:

```
┌─────────────────────────────────────────────┐
│               docker-compose.yml              │
│                                                 │
│   ┌───────────┐          ┌──────────────┐     │
│   │    web     │  SQL通信  │      db       │     │
│   │ (Flask)    │─────────▶│ (PostgreSQL)  │     │
│   │ :5000      │          │  :5432        │     │
│   └─────┬──────┘          └───────┬───────┘     │
│         │ -p 8080:5000            │              │
└─────────┼─────────────────────────┼──────────────┘
          ▼                          ▼
     ホストの8080番              named volume
     (ブラウザ/curl)             (db-data)
```

## ハンズオン手順

`exercises/07-web-app-practice/` に移動します。

```bash
cd exercises/07-web-app-practice
```

ファイル構成:

- `app.py`: メモを登録・一覧表示できる簡単なFlaskアプリ(PostgreSQLに保存)
- `requirements.txt`: Pythonの依存パッケージ
- `Dockerfile`: `web`サービス用のビルド設定
- `docker-compose.yml`: `web` + `db` の構成定義

### 1. ファイルを読んで構成を把握する

`docker-compose.yml`、`Dockerfile`、`app.py`の順に目を通し、以下を確認してください。

- `db`サービスの環境変数(`POSTGRES_USER`など)
- `web`サービスが`db`という名前でPostgreSQLに接続していること(`app.py`内の接続文字列)
- `db-data`という名前付きボリュームが定義されていること

### 2. 起動する

```bash
docker compose up --build
```

初回はPostgreSQLの起動に数秒かかります。ログに `database system is ready to accept connections` が表示されるまで待ちましょう。

### 3. アプリを操作する

別のターミナルから:

```bash
# メモを1件登録
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "Dockerを学習中"}' \
  http://localhost:8080/notes

# 登録したメモの一覧を取得
curl http://localhost:8080/notes
```

ブラウザで `http://localhost:8080/notes` を開いても一覧が見られます。

### 4. データが永続化されることを確認する

```bash
docker compose down
docker compose up -d
curl http://localhost:8080/notes
```

`docker compose down`(ボリューム削除なし)の後でも、以前登録したメモが残っていることを確認してください。これは `db-data` ボリュームにデータが保存されているためです。

### 5. 完全に初期化したい場合

```bash
docker compose down -v
```

`-v` をつけるとボリュームごと削除され、次回起動時はまっさらな状態から始まります。

## 確認問題・やってみよう

1. `app.py` を読んで、DB接続時のホスト名がなぜ `db` になっているのか(05章・06章の内容と関連づけて)説明してみましょう。
2. `docker compose down` と `docker compose down -v` の違いによる挙動の差を、実際に試して確認しましょう。
3. (発展)`/notes` に加えて、`/notes/<id>` でメモを1件だけ取得するエンドポイントを自分で追加し、再ビルドして動かしてみましょう。

## 詰まりやすいポイント・トラブルシューティング

- **起動直後に`web`がDB接続エラーで落ちる**: PostgreSQLの起動完了より先にFlaskが接続を試みることがあります。`docker compose up`をもう一度実行するか、09章で扱う`healthcheck`+`depends_on: condition: service_healthy`で解決できます。
- **`curl`で`Connection refused`**: `docker compose ps`で`web`サービスがちゃんと`Up`になっているか確認してください。
- **ポート`8080`が使用中でエラー**: 前章までのコンテナが起動したままの可能性があります。`docker ps`で確認し、不要なコンテナは`docker rm -f`してください。

---
前へ: [06. Docker Composeの基本](../06-docker-compose/README.md) | 次へ: [08. マルチステージビルド](../08-multi-stage-build/README.md)
