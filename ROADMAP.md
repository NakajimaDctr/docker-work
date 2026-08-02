# Docker 学習ロードマップ

このロードマップは、Docker を完全に触ったことがない人が「基礎を一通り」体系的に身につけることを目的としています。各章は `docs/` の解説を読み、`exercises/` で実際に手を動かす、という流れで進めます。

## 進め方の目安

- 1章あたり 30分〜1.5時間 を目安に、1日1〜2章のペースで進めるのがおすすめです(全体で 2〜3週間程度)。
- 必ず `docs/XX-.../README.md` を読んでから、対応する `exercises/XX-.../` を実際に動かしてください。「読むだけ」で終わらせないことが上達の近道です。
- 各章末の「確認問題・やってみよう」は、次の章に進む前に自分で解けるか確認しましょう。

## 章一覧

| # | 章 | 目的 | 所要時間目安 | 前提知識 |
|---|---|---|---|---|
| 00 | [環境セットアップ](./docs/00-setup/README.md) | Docker Desktopのインストール確認・動作確認 | 30分 | なし |
| 01 | [コンテナとイメージとは](./docs/01-containers-and-images/README.md) | コンテナ/イメージの概念、仮想マシンとの違いを理解する | 45分 | 00完了 |
| 02 | [基本コマンド操作](./docs/02-basic-commands/README.md) | run/ps/images/exec/logs/rm 等の基本操作を覚える | 1時間 | 01完了 |
| 03 | [Dockerfileの基本](./docs/03-dockerfile-basics/README.md) | 自分でDockerfileを書き、独自イメージをビルドする | 1時間 | 02完了 |
| 04 | [ボリュームとデータ永続化](./docs/04-volumes-and-data/README.md) | コンテナ削除後もデータを残す方法を理解する | 1時間 | 03完了 |
| 05 | [ネットワーキング](./docs/05-networking/README.md) | コンテナ間通信・ポート公開の仕組みを理解する | 1時間 | 04完了 |
| 06 | [Docker Composeの基本](./docs/06-docker-compose/README.md) | 複数コンテナをまとめて管理する | 1.5時間 | 05完了 |
| 07 | [総合実践: Webアプリ構築](./docs/07-web-app-practice/README.md) | Flask + PostgreSQLをComposeで構築する総合演習 | 2時間 | 06完了 |
| 08 | [マルチステージビルド](./docs/08-multi-stage-build/README.md) | イメージを軽量化するビルド手法を学ぶ | 45分 | 07完了 |
| 09 | [本番運用の基礎](./docs/09-production-basics/README.md) | ヘルスチェック・環境変数管理・ログなど運用の基礎 | 1時間 | 08完了 |
| 10 | [次のステップ](./docs/10-next-steps/README.md) | 学習後に進むべき方向性(Kubernetes等)を知る | 15分 | 09完了 |

## 学習の全体像

```
セットアップ
    │
    ▼
コンテナ/イメージの概念 ─▶ 基本コマンド ─▶ Dockerfile
    │                                          │
    ▼                                          ▼
                                    ボリューム ─▶ ネットワーク
                                                     │
                                                     ▼
                                              Docker Compose
                                                     │
                                                     ▼
                                        総合実践(Webアプリ構築)
                                                     │
                                                     ▼
                                  マルチステージビルド ─▶ 本番運用の基礎
                                                     │
                                                     ▼
                                                次のステップ
```

## このロードマップで扱わないもの

以下は範囲外です。基礎を固めた後、[10-next-steps](./docs/10-next-steps/README.md) で次の学習先として紹介します。

- Kubernetes などのコンテナオーケストレーション
- CI/CDパイプラインへのDocker組み込み
- Docker Swarm
- セキュリティの高度なトピック(イメージスキャン、rootless運用など)
