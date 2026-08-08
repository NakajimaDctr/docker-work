# 学習メモ・QA集

このファイルは、03章「Dockerfileの基本」を学習する中で出た疑問と回答をQA形式でまとめたメモです。

---

## Q. `COPY hello.py .` の `.` は何を指す?

**A.**
Dockerfile内の`COPY`/`ADD`/`RUN`/`CMD`/`ENTRYPOINT`などにおけるカレントディレクトリは、`WORKDIR`で指定した場所を指します。`WORKDIR`が指定されていなければデフォルトは`/`です。

```dockerfile
WORKDIR /app
COPY hello.py .   # → /app/hello.py としてコピーされる
```

---

## Q. `WORKDIR /app` を指定した時点でカレントディレクトリは`/app`に移動している?

**A.**
はい。`WORKDIR /app`以降のすべての命令(`RUN`, `COPY`, `ADD`, `CMD`, `ENTRYPOINT`など)は`/app`をカレントディレクトリとして実行されます。

- `/app`が存在しない場合は自動的に作成される(`mkdir -p`相当)。
- `WORKDIR`は複数回書くこともでき、その都度切り替わる(例: `WORKDIR /app` → `WORKDIR sub` で `/app/sub`になる)。
- `docker run`でコンテナを起動したときや`docker exec -it <container> bash`で入ったときも、この`WORKDIR`が初期カレントディレクトリになる。

---

## Q. `CMD ["python", "hello.py"]` は何をしている?

**A.**
コンテナ起動時に実行するデフォルトのコマンドを指定している。`WORKDIR /app`があるため、`/app`にある`hello.py`が`python`で実行される。

### exec形式とshell形式

```dockerfile
CMD ["python", "hello.py"]   # exec形式(推奨)
CMD python hello.py          # shell形式
```

- **exec形式**: シェルを介さず直接プロセスとして実行される。
- **shell形式**: `/bin/sh -c "python hello.py"`のようにシェル経由で実行される。

### CMDの性質

- Dockerfile内に`CMD`は基本的に1つだけ(複数書くと最後のものだけ有効)。
- `docker run <image>`のように引数を指定せず実行した場合のデフォルトであり、`docker run <image> echo hi`のように実行時引数を渡すと、その内容で丸ごと上書きされる。

---

## Q. exec形式(シェルを介さない)の利点は?

**A.**

### 1. シグナルが正しくプロセスに届く

shell形式では実際には`/bin/sh -c "python hello.py"`が実行され、PID 1は`sh`になり`python`はその子プロセスになる。

- `docker stop`はコンテナのPID 1に`SIGTERM`を送るが、`sh`が子プロセスに転送してくれるとは限らない。
- 結果として`python`側がシグナルを受け取れず、`SIGTERM`が無視されたまま一定時間後に強制`SIGKILL`される、という挙動になりがち。

exec形式なら`python`自体がPID 1になるため、シグナルを直接受け取れる(グレースフルシャットダウンが効きやすい)。

### 2. 余計なシェルプロセスが立たない

shell形式は`sh`というプロセスを一枚挟むため、リソース的にもプロセスツリー的にも無駄がある。exec形式は目的のプロセスだけが起動する。

### 3. シェル特有の落とし穴を避けられる

shell形式は文字列をシェルに渡すため、変数展開・グロブ展開・クォート処理などシェルの解釈が挟まる。意図しない展開や特殊文字の扱いでハマることがある(逆に環境変数展開が必要な場合はshell形式が便利、というトレードオフもある)。

---

## Q. ENTRYPOINTとCMDの違いは?

**A.**

### 基本的な役割

- **ENTRYPOINT**: コンテナの「本体となる実行コマンド」。通常は上書きさせたくないもの。
- **CMD**: ENTRYPOINTに渡す「デフォルト引数」、またはENTRYPOINTが無い場合の「デフォルトコマンド」。

### 組み合わせパターン

**1. CMDのみ**

```dockerfile
CMD ["python", "hello.py"]
```

- `docker run image` → `python hello.py`が実行される。
- `docker run image echo hi` → `CMD`全体が丸ごと`echo hi`に置き換わる。

**2. ENTRYPOINTのみ**

```dockerfile
ENTRYPOINT ["python", "hello.py"]
```

- `docker run image` → `python hello.py`が実行される。
- `docker run image --debug` → 実行時引数が末尾に追加され`python hello.py --debug`になる(置き換わらない)。

**3. ENTRYPOINT + CMD(よくある組み合わせ)**

```dockerfile
ENTRYPOINT ["python"]
CMD ["hello.py"]
```

- `docker run image` → `python hello.py`(CMDがENTRYPOINTへのデフォルト引数として渡る)。
- `docker run image other.py` → `python other.py`(CMD部分だけが上書きされる)。

### 使い分けの目安

- 「このイメージは常にこのプログラムを実行するもの」という用途(CLIツールのイメージなど) → `ENTRYPOINT`を使い、可変部分は`CMD`でデフォルト引数として渡す。
- 「用途が広く、コマンドごと差し替えられてもよい」場合(汎用のベースイメージなど) → `CMD`だけで十分。

### 補足: `docker run --entrypoint`

実行時に`--entrypoint`オプションを使えば`ENTRYPOINT`自体も上書き可能(例: デバッグ目的で`--entrypoint /bin/bash`)。

---

## Q. ビルドコンテキスト(Dockerfileがあるディレクトリ)には1つのDockerfileしか作成できない?

**A.**
いいえ、1つのディレクトリに複数のDockerfileを置くことは可能。

デフォルトでは`docker build .`を実行するとカレントディレクトリの`Dockerfile`という名前のファイルが自動的に使われるが、`-f`(`--file`)オプションでファイル名を明示的に指定すれば、同じディレクトリに複数のDockerfile相当のファイルを共存させられる。

```bash
docker build -f Dockerfile.dev -t myapp:dev .
docker build -f Dockerfile.prod -t myapp:prod .
```

`Dockerfile.dev` / `Dockerfile.prod` / `Dockerfile.test`のように名前を使い分けるのはよくあるパターン(開発用と本番用でベースイメージや依存関係を変えたい場合など)。

- **ビルドコンテキスト**(`docker build .`の`.`の部分) = どのディレクトリ以下のファイルをDockerビルドに送るか
- **Dockerfileの場所・名前**(`-f`オプション) = どの命令セットを使うか

この2つは別々に指定できるため、「1ディレクトリにつき1 Dockerfile」という制約はない。ただし`-f`を省略した場合はそのディレクトリ直下の`Dockerfile`という名前のファイルがデフォルトで使われる点は覚えておく。

---

## Q. `FROM`で指定するイメージはライブラリのようなもの? よく使われるベースイメージにはどんな種類があり、それぞれどんな場面で使う?

**A.**

### ライブラリとの違い

- **ライブラリ**: 自分のコード内で`import`して使う、コードの一部品。
- **ベースイメージ**: OS(のようなもの)+ミドルウェア/ランタイムが最初から入った、コンテナの出発点そのもの。`FROM python:3.12-slim`なら「Debianベースの最小限のLinux環境に、Pythonの実行環境一式が入っている」状態からDockerfileが始まる。

`FROM`はDockerfileの一番最初に必ず書く命令で、そこから`COPY`や`RUN`で自分のアプリのファイル・依存関係を積み重ねていく。

### よく使われるベースイメージの例

**言語ランタイム系**(特定の言語で書かれたアプリを起動するために使う)
- `python:3.12` / `python:3.12-slim` / `python:3.12-alpine`
- `node:20` / `node:20-slim` / `node:20-alpine`
- `golang:1.22`
- `openjdk:21-slim`
- `ruby:3.3`

**OSのみ(最小構成)**
- `ubuntu:22.04`
- `debian:bookworm-slim`
- `alpine:3.19`(非常に軽量、数MB程度)

**ミドルウェア系**
- `nginx:1.27`
- `postgres:16`
- `redis:7`
- `mysql:8`

**特殊なもの**
- `scratch`: 何も入っていない完全に空のイメージ(Goのような単一バイナリを配置するだけの超軽量イメージを作る時に使う)

タグ末尾の違い: 無印(例: `python:3.12`)はフル機能でサイズが大きい、`-slim`は最小限に削ったDebianベース、`-alpine`はAlpine Linuxベースでさらに軽量(muslベースのため稀に互換性問題が出ることがある)。

### 「OSのみ」イメージが使われる場面

- **言語ランタイムが用意されていない/複数の言語を組み合わせる場合**: 既製の言語イメージにはその言語向けの設定しか入っていないため、`ubuntu`や`debian-slim`をベースに`apt-get install`で必要なものを自分で組み立てる。
- **CLIツールやシステムコマンドを動かすコンテナ**: `ffmpeg`や`imagemagick`のように、OSのパッケージマネージャ(`apt`, `apk`)経由でインストールするツール自体が主役になる場合。
- **multi-stage buildの最終ステージ**: ビルドは`golang`イメージで行い、実行は依存関係のない軽量な`alpine`や`debian-slim`に成果物だけコピーする。

```dockerfile
FROM golang:1.22 AS builder
# ビルド処理...

FROM alpine:3.19
COPY --from=builder /app/mybinary /usr/local/bin/
CMD ["mybinary"]
```

### 「ミドルウェア系」イメージが使われる場面

`FROM`で「土台にして自分のコードを積む」というより、**そのイメージ自体を単独のコンテナとしてそのまま動かす**使い方が中心。

- **アプリと分離して1つのサービスとして起動する**: 自分のアプリとは別に`postgres:16`をDBサーバー用コンテナ、`redis:7`をキャッシュサーバー用コンテナとしてそのまま立てる。`docker-compose.yml`で複数コンテナを組み合わせる際によく登場する。

```yaml
services:
  app:
    build: .
  db:
    image: postgres:16
  cache:
    image: redis:7
```

- **リバースプロキシ/静的ファイル配信**: `nginx`イメージをそのまま(あるいは設定ファイルだけ`COPY`して)使い、複数のアプリコンテナの前段に置いてルーティングやSSL終端をさせる。

### まとめ

- 言語ランタイム系・OSのみ系 → 主に`FROM`で使い、**自分のアプリを積み上げていくための土台**
- ミドルウェア系 → 主に**それ単体を1つの独立したサービスコンテナとして動かす**(`FROM`で土台にすることは稀)

---

前へ: [README](README.md)
