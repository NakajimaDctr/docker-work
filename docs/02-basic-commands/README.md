# 02. 基本コマンド操作

## この章で学ぶこと

- コンテナのライフサイクル(作成・起動・停止・削除)を操作するコマンドを覚える
- 動いているコンテナの中に入って調査する方法を知る
- ログの確認方法を知る

## 概念解説

前章では `docker run` でコンテナを起動しました。この章では、コンテナを「操作」するための一連のコマンドを整理します。コンテナには次のようなライフサイクル(状態遷移)があります。

```
[イメージ] --run--> [Created/Running] --stop--> [Exited] --start--> [Running]
                                                     │
                                                     └--rm--> [削除済み]
```

`docker run` は実は「`docker create`(コンテナ作成) + `docker start`(起動)」をまとめて行うコマンドです。停止したコンテナは削除されるまでディスク上に残り続けるため、`docker start` で再開することもできます。

## ハンズオン手順

`exercises/02-basic-commands/CHEATSHEET.md` にコマンド一覧をまとめています。ここでは実際に手を動かしながら覚えていきましょう。

### 1. コンテナを起動する

```bash
docker run -d --name web -p 8080:80 nginx
```

### 2. 実行中のコンテナ一覧を見る

```bash
docker ps
```

### 3. コンテナの中に入る(exec)

コンテナは中でLinuxプロセスが動いています。シェルを起動してコンテナの中を覗いてみましょう。

```bash
docker exec -it web bash
```

- `-it`: 対話的(interactive)に、疑似端末(tty)を割り当ててシェルを使えるようにするオプション
- コンテナの中に入ったら `ls /usr/share/nginx/html` などを実行してファイルを覗いてみましょう
- `exit` でコンテナの中から抜けます(コンテナ自体は動き続けます)

### 4. ログを確認する

```bash
docker logs web
docker logs -f web   # -f でリアルタイムに追跡(tail -f的な動作)。Ctrl+Cで抜ける
```

別のターミナルで `curl http://localhost:8080` を実行しながら `docker logs -f web` を見ると、アクセスログがリアルタイムに流れるのが確認できます。

### 5. コンテナの詳細情報を見る

```bash
docker inspect web
```

IPアドレスや環境変数、マウント情報など、コンテナの詳細なJSON情報が表示されます。

### 6. 停止・再開・削除

```bash
docker stop web        # 停止
docker ps -a            # 停止していても一覧には残っていることを確認
docker start web        # 再開
docker stop web
docker rm web           # 完全に削除(停止済みでないと削除できない)
docker ps -a             # 一覧から消えたことを確認
```

### 7. 不要なイメージ・コンテナをまとめて掃除する

```bash
docker container prune   # 停止中のコンテナを一括削除
docker image prune       # 使われていないイメージを一括削除
```

## 確認問題・やってみよう

1. `docker run` と `docker start` の違いを説明してみましょう。
2. `nginx` コンテナを起動し、`docker exec -it <名前> bash` でコンテナの中に入り、`cat /etc/os-release` を実行してどんなOSがベースになっているか確認してみましょう。
3. コンテナを `docker stop` で止めた後、`docker rm` する前に `docker start` で復活させられることを確認してみましょう。

## 詰まりやすいポイント・トラブルシューティング

- **`docker exec` で `bash: executable file not found`**: ベースイメージによっては `bash` が入っておらず `sh` しかない場合があります(軽量イメージ`alpine`系など)。その場合は `docker exec -it <名前> sh` を試してください。
- **`docker rm` で `You cannot remove a running container`**: 先に `docker stop` してから `docker rm` する必要があります。実行中のコンテナを強制削除したい場合は `docker rm -f <名前>` も使えますが、まずは正しい手順(stop→rm)に慣れましょう。
- **コンテナ名が重複してrunできない**: `docker run --name web ...` で既に `web` という名前のコンテナが存在するとエラーになります。`docker rm web` で削除するか、別の名前を使ってください。

---
前へ: [01. コンテナとイメージとは](../01-containers-and-images/README.md) | 次へ: [03. Dockerfileの基本](../03-dockerfile-basics/README.md)
