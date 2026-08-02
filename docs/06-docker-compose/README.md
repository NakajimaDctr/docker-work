# 06. Docker Composeの基本

## この章で学ぶこと

- `docker compose` を使い、複数のコンテナをまとめて起動・管理する方法を学ぶ
- `docker-compose.yml` の基本的な書き方を理解する
- これまで手作業でやっていた「ネットワーク作成」「ポート公開」「起動順」がComposeで自動化されることを体感する

## 概念解説

前章までは、コンテナを1つずつ `docker run` で起動し、ネットワークも手動で `docker network create` していました。複数コンテナで構成されるアプリでは、これを毎回手打ちするのは大変です。

**Docker Compose** は、複数のコンテナ構成を1つのYAMLファイル(`docker-compose.yml` または `compose.yml`)に定義し、`docker compose up` 一発でまとめて起動できる仕組みです。

Composeを使うと自動的に:

- プロジェクト専用のネットワークが作成され、サービス名(YAML内の名前)で名前解決できるようになる
- 定義した全サービスが一括で起動・停止される
- 設定がファイルとして残るので、チームメンバーとも共有・再現しやすい

`docker-compose.yml` の基本構造:

```yaml
services:
  web:              # サービス名(コンテナ名やホスト名として使われる)
    image: nginx    # 使用するイメージ
    ports:
      - "8080:80"   # ホスト:コンテナ のポートマッピング
  cache:
    image: redis
```

## ハンズオン手順

`exercises/06-docker-compose/` に移動します。

```bash
cd exercises/06-docker-compose
```

このディレクトリには、アクセスカウンターを提供するFlaskアプリ(`app.py`)と、それが使うRedis(データを保存するインメモリDB)を組み合わせた `docker-compose.yml` があります。

### 1. compose.ymlの中身を確認する

```bash
cat docker-compose.yml
```

`web`サービスと`redis`サービスの2つが定義されています。`web`はこのディレクトリの`Dockerfile`からビルドされ、`redis`は公式イメージをそのまま使います。

### 2. まとめて起動する

```bash
docker compose up --build
```

- `--build`: `Dockerfile`から`web`イメージを再ビルドしてから起動する
- ログが両方のサービス分、色分けされて流れてくるのを確認しましょう(`web  |` `redis |` のようなプレフィックス)

### 3. 動作確認する

別のターミナルを開いて:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

アクセスするたびにカウンターが増えていくレスポンスが返ってくれば成功です。裏側では `web` コンテナが `redis` というサービス名だけでRedisコンテナに接続できています(前章で手動でやっていたことが自動化されています)。

### 4. バックグラウンド起動と状態確認

一度 `Ctrl+C` で停止し、今度はバックグラウンドで起動してみましょう。

```bash
docker compose up -d
docker compose ps
```

### 5. ログを確認する

```bash
docker compose logs -f web
```

`Ctrl+C`で抜けられます。

### 6. 停止・削除

```bash
docker compose down
```

`docker compose down` は、起動した全コンテナとComposeが作成したネットワークをまとめて削除します。ボリュームも含めて削除したい場合は `docker compose down -v` を使います(データが消えるので注意)。

## 確認問題・やってみよう

1. `docker-compose.yml` 内で `web` サービスが Redis に接続する際、ホスト名としてどんな値を使っているか `app.py` を見て確認してみましょう(ヒント: サービス名がそのままホスト名になります)。
2. `docker compose up` と、これまで使っていた `docker run` を複数回実行する方法を比べて、どちらが管理しやすいか考えてみましょう。
3. `docker-compose.yml` の `redis` サービスにポートマッピングを追加し(`ports: ["6380:6379"]`など)、ホストから直接Redisに繋がることを試してみましょう(余裕があれば)。

## 詰まりやすいポイント・トラブルシューティング

- **`docker compose up`でweb側がRedis接続エラーになる**: Redisコンテナの起動がまだ完了していないタイミングでwebが接続を試みることがあります(`depends_on`はコンテナの起動順序は保証しますが、アプリの準備完了までは待ちません)。今回のサンプルアプリは簡単なリトライ処理を入れていますが、本格的なアプリでは`healthcheck`(09章で扱います)を使うのが望ましいです。
- **ポートが競合してupに失敗する**: 05章までで起動したコンテナが残っていないか `docker ps` で確認し、`docker rm -f` で片付けてから再実行してください。
- **`docker-compose`と`docker compose`どちらを使えばいい?**: 現在のDocker Desktopでは、ハイフンなしの `docker compose`(サブコマンド形式)が標準です。本教材でも一貫して `docker compose` を使用します。

---
前へ: [05. ネットワーキング](../05-networking/README.md) | 次へ: [07. 総合実践: Webアプリ構築](../07-web-app-practice/README.md)
