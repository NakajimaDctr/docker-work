# 04. ボリュームとデータ永続化

## この章で学ぶこと

- コンテナを削除するとデータが消える、という性質を理解する
- `ボリューム`と`バインドマウント`という2種類のデータ永続化の方法を理解する
- 実際にファイルをコンテナの外に残す体験をする

## 概念解説

コンテナのファイルシステムは、コンテナを削除すると一緒に消えてしまいます(コンテナは「使い捨て」が基本の考え方です)。データベースのデータや、ユーザーがアップロードしたファイルなど、消えては困るデータは「コンテナの外」に保存する必要があります。そのための仕組みが2つあります。

- **ボリューム(Volume)**: Dockerが管理する専用の保存領域。Dockerに「このデータの置き場所は任せて」と管理を委ねる方式です。本番運用でも推奨される方法です。
- **バインドマウント(Bind Mount)**: ホスト(自分のPC)の特定のディレクトリを、そのままコンテナ内のディレクトリに繋ぎこむ方式です。開発中にコードを即座に反映させたい場合などに便利です。

いずれも「ホスト側の場所」と「コンテナ内の場所」を紐付ける(マウントする)という考え方は共通です。

```
[ホストPC]                      [コンテナ]
  ボリューム or                    /app/data  ←── ここに書き込むと
  ホストのディレクトリ  ←──────マウント──── 実体はホスト側/ボリュームに保存される
```

## ハンズオン手順

`exercises/04-volumes-and-data/` に移動します。

```bash
cd exercises/04-volumes-and-data
```

このディレクトリには、アクセスするたびにカウントアップした数字をファイルに書き込む簡単なPythonアプリ(`counter.py`)と `Dockerfile` があります。

### 1. まずはボリュームなしで実験(データが消えることを確認)

```bash
docker build -t counter-app .
docker run --rm counter-app
docker run --rm counter-app
docker run --rm counter-app
```

何度実行しても、カウンターが `1` から始まってしまうことを確認してください。`--rm` でコンテナごと消えるので、ファイルに書いた記録も一緒に消えています。

### 2. named volume(名前付きボリューム)を使う

```bash
docker volume create counter-data
docker run --rm -v counter-data:/data counter-app
docker run --rm -v counter-data:/data counter-app
docker run --rm -v counter-data:/data counter-app
```

- `-v counter-data:/data`: `counter-data`という名前のボリュームを、コンテナ内の`/data`にマウントする

今度はカウンターが `1, 2, 3...` と増え続けることを確認してください。コンテナ自体は毎回使い捨て(`--rm`)なのに、データだけは `counter-data` ボリュームに残り続けています。

### 3. ボリュームの中身を確認する

```bash
docker volume ls
docker volume inspect counter-data
```

### 4. バインドマウントを試す(ホストのディレクトリと直結)

```bash
mkdir -p ./local-data
docker run --rm -v "$(pwd)/local-data:/data" counter-app
ls ./local-data
cat ./local-data/count.txt
```

自分のPC上の `./local-data` ディレクトリの中に、コンテナが書き込んだ `count.txt` が直接見えることを確認しましょう。

### 5. 後片付け

```bash
docker volume rm counter-data
rm -rf ./local-data
```

## 確認問題・やってみよう

1. 「ボリューム」と「バインドマウント」の違いを自分の言葉で説明してみましょう。
2. なぜ手順1では毎回カウンターが `1` に戻り、手順2では増え続けたのか説明してみましょう。
3. `docker volume ls` で今使っているボリューム一覧を確認し、使われていないボリュームを `docker volume prune` で掃除してみましょう(実行前に本当に不要か確認する癖をつけましょう)。

## 詰まりやすいポイント・トラブルシューティング

- **`-v`のホスト側パスは絶対パスが必要**: バインドマウントで相対パスを書くとエラーになったり意図しない挙動になることがあります。`$(pwd)/...`のように絶対パスに展開して使うのが安全です。
- **ボリュームを削除しようとして`volume is in use`エラー**: そのボリュームを使っているコンテナが(停止中でも)残っていると削除できません。`docker ps -a`で該当コンテナを探し、`docker rm`してから削除してください。
- **Mac/Windowsでバインドマウントのファイル反映が遅い**: 裏側でLinux VMを介しているため、大量のファイル監視が絡む場合に若干の遅延が発生することがあります。基本的な学習では気にする必要はありません。

---
前へ: [03. Dockerfileの基本](../03-dockerfile-basics/README.md) | 次へ: [05. ネットワーキング](../05-networking/README.md)
