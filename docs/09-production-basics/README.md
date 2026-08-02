# 09. 本番運用の基礎

## この章で学ぶこと

- コンテナが「本当に正常に動いているか」を判定する`healthcheck`を理解する
- 環境ごとに設定を切り替える(`.env`ファイル、環境変数)方法を学ぶ
- `.dockerignore`でビルドに不要なファイルを除外する方法を学ぶ
- 本番運用でよく問題になるポイント(ログ、再起動ポリシー)を知る

## 概念解説

### healthcheck(ヘルスチェック)

07章で「PostgreSQLの起動完了より先にFlaskが接続してエラーになる」という問題に触れました。これは、コンテナが`Up`状態であることと、その中のアプリが「リクエストを受け付けられる状態」であることが必ずしも一致しないために起きます。

`healthcheck`は、コンテナに対して定期的に「本当に正常か」を確認するコマンドを実行させる仕組みです。Composeでは`depends_on`と組み合わせることで、「dbが本当に使える状態になってからwebを起動する」という制御ができます。

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 5
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy   # dbがhealthyになるまでwebを起動しない
```

### 環境変数と`.env`ファイル

パスワードや接続先など、環境(開発/本番)によって変わる値をコードに直接書き込む(ハードコーディングする)のは望ましくありません。Composeでは`.env`ファイルに変数をまとめ、`docker-compose.yml`側で`${変数名}`として参照できます。

```
# .env
DB_PASSWORD=supersecret
```

```yaml
environment:
  - POSTGRES_PASSWORD=${DB_PASSWORD}
```

`.env`ファイルは、実際のパスワード等の秘密情報を含むため **通常はgit管理に含めません**(`.gitignore`に追加します)。教材やチームで共有する際は、実際の値を空にした`.env.example`を用意し、各自コピーして使うのが一般的です。

### `.dockerignore`

`.dockerignore`は、`docker build`時に「ビルドコンテキストに含めないファイル」を指定するものです(`.gitignore`と似た書き方)。`node_modules`や`.git`、ローカルの`.env`などをここで除外することで、ビルドが速くなり、意図しない秘密情報の混入も防げます。

## ハンズオン手順

`exercises/09-production-basics/` に移動します。

```bash
cd exercises/09-production-basics
```

このディレクトリは07章のWebアプリ構成をベースに、`healthcheck`・`.env`・`.dockerignore`を追加したものです。

### 1. `.env.example`をコピーして`.env`を作る

```bash
cp .env.example .env
cat .env
```

今回は学習用なので簡単な値が入っていますが、実務ではここに実際のパスワード等を設定します。

### 2. `docker-compose.yml`のhealthcheck設定を確認する

```bash
cat docker-compose.yml
```

`db`サービスに`healthcheck`が、`web`サービスの`depends_on`に`condition: service_healthy`が設定されていることを確認してください。

### 3. 起動して、healthcheckの状態を観察する

```bash
docker compose up -d --build
docker compose ps
```

`db`サービスのSTATUSに`(healthy)`と表示されるまで少し待ってから`web`が起動することを確認しましょう。`watch`コマンドが使える場合は以下でリアルタイムに変化を追えます。

```bash
watch -n 1 docker compose ps
```

(`watch`がない場合は、`docker compose ps`を数秒おきに手動で再実行してください)

### 4. `.dockerignore`の効果を確認する

```bash
cat .dockerignore
```

`__pycache__`や`.env`などが除外対象になっていることを確認してください。試しに`.dockerignore`の中身を空にしてビルドし直し、ビルドログの`Sending build context to Docker daemon`のサイズが変化するか比べてみるのも良い実験です。

### 5. ログを確認し、後片付けする

```bash
docker compose logs
docker compose down -v
```

## 確認問題・やってみよう

1. `healthcheck`がない場合(07章の構成)と、ある場合(この章の構成)で、`web`コンテナの起動タイミングにどんな違いが生まれるか説明してみましょう。
2. `.env`ファイルをgit管理に含めない理由を説明してみましょう。
3. `.dockerignore`に何も書かなかった場合、どんなファイルが誤ってイメージに含まれてしまう可能性があるか考えてみましょう(例: ローカルの仮想環境フォルダ、`.git`ディレクトリなど)。

## 詰まりやすいポイント・トラブルシューティング

- **healthcheckが`unhealthy`のままになる**: `test`に指定したコマンドがコンテナ内に存在するか確認してください(例: `pg_isready`は postgres イメージには標準で入っていますが、自作イメージでは別途インストールが必要な場合があります)。
- **`.env`の値が反映されない**: `docker-compose.yml`と同じディレクトリに`.env`があるか、変数名のスペルが一致しているか確認してください。値を変更した場合は`docker compose up`を再実行する必要があります。
- **`.env`をコミットしてしまった**: すぐに`.gitignore`に追加し、既にコミットされている場合はリポジトリの履歴から削除する対応が必要です(このリポジトリでは学習用のダミー値のみなので実害はありませんが、実務では要注意です)。

---
前へ: [08. マルチステージビルド](../08-multi-stage-build/README.md) | 次へ: [10. 次のステップ](../10-next-steps/README.md)
