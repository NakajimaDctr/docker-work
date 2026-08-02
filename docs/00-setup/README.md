# 00. 環境セットアップ

## この章で学ぶこと

- Docker を動かすための環境(Docker Desktop)をインストールする
- Docker が正しく動作しているかを確認する
- この教材の実習ディレクトリの使い方を理解する

## 概念解説

Docker を使うには、まず「Docker Engine」と呼ばれる本体が必要です。Mac や Windows では、これをGUI付きでまとめた **Docker Desktop** をインストールするのが最も簡単です。

Docker Desktop をインストールすると、以下がまとめて使えるようになります。

- `docker` コマンド(CLI)
- `docker compose` コマンド(複数コンテナ管理、06章で扱います)
- コンテナを実際に動かすための実行環境(Linux VMがMac/Windowsの裏側で動きます)

## ハンズオン手順

### 1. Docker Desktop をインストールする

まだの場合は [Docker Desktop公式サイト](https://www.docker.com/products/docker-desktop/) からダウンロードしてインストールしてください。インストール後、アプリケーションを起動し、メニューバー(Mac)やシステムトレイ(Windows)にクジラのアイコンが表示されて安定するまで待ちます。

### 2. バージョンを確認する

ターミナルを開いて以下を実行します。

```bash
docker --version
docker compose version
```

バージョン番号が表示されれば正常にインストールされています。

### 3. 動作確認(hello-world)

Docker が正しく動くか、公式の確認用イメージを実行してみましょう。

```bash
docker run hello-world
```

初回はイメージのダウンロードが始まり、その後 `Hello from Docker!` という英語のメッセージが表示されれば成功です。このメッセージには「Dockerがどういう手順でこれを表示したか」の説明も書かれているので、一度読んでみてください。

### 4. 教材の実習ディレクトリを確認する

このリポジトリの `exercises/` 配下に、各章に対応する実習用ファイルが置かれています。次の章からは、`docs/` の解説を読みながら、対応する `exercises/XX-.../` に `cd` してコマンドを実行していきます。

```bash
cd exercises/01-hello-docker
```

## 確認問題・やってみよう

1. `docker --version` の出力結果を見て、自分がインストールしたDockerのバージョンをメモしておきましょう。
2. `docker run hello-world` を実行した際に表示された説明文を読み、「イメージをどこから取得したか」「どこでコンテナとして実行されたか」を自分の言葉で説明してみましょう。
3. `docker system info` を実行し、どんな情報が表示されるか眺めてみましょう(まだ意味が分からなくてOKです)。

## 詰まりやすいポイント・トラブルシューティング

- **`docker: command not found`**: Docker Desktopが起動していない、またはインストールが完了していない可能性があります。アプリを起動し、クジラアイコンが安定するまで待ってから再度試してください。
- **`Cannot connect to the Docker daemon`**: Docker Desktopアプリ自体が起動していないことが原因です。アプリを起動してから再実行してください。
- **ダウンロードが遅い/失敗する**: ネットワーク環境によっては初回のイメージ取得に時間がかかります。時間を置いて再実行してみてください。

---
次へ: [01. コンテナとイメージとは](../01-containers-and-images/README.md)
