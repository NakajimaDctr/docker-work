# docker-work

Docker を「実際に手を動かしながら」学ぶための学習用リポジトリです。
完全初心者から Docker の基礎を一通り体系的に押さえることを目標にしています。

## 使い方

1. まず [ROADMAP.md](./ROADMAP.md) で全体の学習の流れを確認してください。
2. `docs/00-setup/` から順番に `docs/10-next-steps/` まで読み進めます。
3. 各章の `docs/XX-.../README.md` には対応する実習ディレクトリ `exercises/XX-.../` が用意されています。解説を読みながら、実際にそのディレクトリでコマンドを実行して手を動かしてください。

## ディレクトリ構成

```
docker-work/
├── ROADMAP.md      # 学習ロードマップ(全体地図)
├── docs/           # 章ごとの解説(日本語Markdown)
└── exercises/      # 章ごとの実習用サンプルコード
```

## 前提

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (または Docker Engine + Docker Compose) がインストール済みであること
- ターミナル操作の基本(`cd`, `ls` 程度)ができること
- プログラミング経験は必須ではありませんが、サンプルコードには Python (Flask) を使用しています