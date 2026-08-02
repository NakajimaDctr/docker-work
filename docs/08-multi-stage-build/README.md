# 08. マルチステージビルド

## この章で学ぶこと

- イメージサイズが大きくなる原因を理解する
- マルチステージビルドという手法でイメージを軽量化する方法を学ぶ
- ビルド前後でイメージサイズを比較して効果を体感する

## 概念解説

これまでのDockerfileでは、1つの`FROM`から始まる1ステージだけでビルドしてきました。しかし実際には、「ビルドに必要なツール」と「実行時に必要なもの」は異なることがよくあります。

例えば:

- コンパイル言語(Go, C++など)は、ビルド時にはコンパイラが必要ですが、実行時はコンパイル済みのバイナリだけあれば十分です。
- フロントエンドのビルド(`npm run build`など)は、ビルド時にはNode.jsやビルドツール一式が必要ですが、実行時は生成された静的ファイルだけで十分です。

これらをすべて実行用イメージに含めてしまうと、不要なツール類がイメージに残り、サイズが無駄に大きくなります。

**マルチステージビルド** は、Dockerfileの中に複数の`FROM`(ステージ)を書き、あるステージでビルドした成果物だけを次のステージにコピーする手法です。

```dockerfile
# ステージ1: ビルド用(重い、ツール一式入り)
FROM golang:1.22 AS builder
WORKDIR /src
COPY . .
RUN go build -o app .

# ステージ2: 実行用(軽量ベースイメージ)
FROM alpine:3.19
COPY --from=builder /src/app /app
CMD ["/app"]
```

最終的にできあがるイメージは「ステージ2」だけを元にしており、ビルドツール一式が入った「ステージ1」の中身は最終イメージには含まれません。

## ハンズオン手順

`exercises/08-multi-stage-build/` に移動します。

```bash
cd exercises/08-multi-stage-build
```

このディレクトリには、簡単なGo言語の「Hello, Docker!」を出力するプログラム(`main.go`)と、比較用に2つのDockerfileがあります。

- `Dockerfile.single`: シングルステージ(ビルド環境をそのまま使う)
- `Dockerfile.multi`: マルチステージ(ビルド用と実行用を分離)

### 1. シングルステージ版をビルドする

```bash
docker build -f Dockerfile.single -t app-single .
```

### 2. マルチステージ版をビルドする

```bash
docker build -f Dockerfile.multi -t app-multi .
```

### 3. イメージサイズを比較する

```bash
docker images | grep app-
```

`app-single`(Goのビルド環境ごと含む、数百MB〜1GB近く)に対して、`app-multi`(実行に必要な最小限、数十MB程度)と、大きな差が出ることを確認してください。

### 4. どちらも同じように動くことを確認する

```bash
docker run --rm app-single
docker run --rm app-multi
```

同じ `Hello, Docker!` のメッセージが出力され、動作自体は同じであることを確認しましょう。

## 確認問題・やってみよう

1. なぜ `app-multi` の方がサイズが小さくなったのか、`Dockerfile.multi` の中身を見ながら説明してみましょう。
2. `Dockerfile.multi` の `COPY --from=builder ...` の行が何をしているか説明してみましょう。
3. (発展)03章や07章で作ったPythonアプリのDockerfileに、マルチステージビルドを適用できないか考えてみましょう(ヒント: Pythonの依存パッケージを`pip install --user`でビルドステージに閉じ込め、実行ステージにコピーする方法があります)。

## 詰まりやすいポイント・トラブルシューティング

- **`docker build`で`-f`オプションを忘れる**: このディレクトリには複数のDockerfile(`Dockerfile.single`,`Dockerfile.multi`)があるため、必ず`-f`で使うファイルを明示してください。省略すると`Dockerfile`という名前のファイルを探しに行ってしまいます。
- **`COPY --from=builder`でファイルが見つからない**: ビルドステージ内でのファイルパス(`/src/app`など)と、実際に生成された場所が一致しているか確認してください。
- **イメージサイズが期待通り減らない**: 実行用ステージのベースイメージ自体が重い(例: `ubuntu`など)場合、`alpine`のような軽量イメージに変えることでさらに削減できます。

---
前へ: [07. 総合実践: Webアプリ構築](../07-web-app-practice/README.md) | 次へ: [09. 本番運用の基礎](../09-production-basics/README.md)
