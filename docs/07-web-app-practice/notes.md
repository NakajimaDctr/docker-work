# 学習メモ・QA集

このファイルは、07章「総合実践: Webアプリ構築」を学習する中で出た疑問と回答をQA形式でまとめたメモです。

---

## Q. `docker-compose.yml`の`volumes: db-data:`は、Dockerにvolumeがマウントされている?

**A.**
`volumes:`セクションには役割が2ヶ所あり、それぞれ意味が異なります。

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data   # ← ここで「マウント」している

volumes:
  db-data:   # ← ここは「db-dataという名前付きボリュームを使う」という宣言
```

- **トップレベルの`volumes: db-data:`**: named volume(名前付きボリューム)`db-data`を定義・登録する部分。マウント処理そのものではなく、「このComposeプロジェクトで`db-data`という名前のボリュームを使う」という宣言。
- **`db`サービス内の`volumes: - db-data:/var/lib/postgresql/data`**: 実際のマウント指定。「`db-data`ボリュームをコンテナ内の`/var/lib/postgresql/data`にマウントする」という意味で、ここで初めてコンテナに接続される。

両方揃って初めてPostgreSQLのデータが`db-data`ボリュームに永続化される。README.mdの確認手順(`docker compose down`後もデータが残ることの確認)がこの挙動そのもの。

---

## Q. `volumes:`の部分は、`docker volume create db-data`と同義?

**A.**
概念としては近いが、実際に作られるボリューム名が異なるため厳密には別物。

**同じ点**:

- named volumeをDockerに登録するという点は同じ
- ドライバは既定で`local`
- 既に同名のボリュームが存在する場合は新規作成せず既存のものを使う
- コンテナのライフサイクルとは独立して残る(`docker compose down`だけでは消えない)

**異なる点(ボリューム名にプロジェクト名の接頭辞がつく)**:

```yaml
volumes:
  db-data:
```

このように書いても、実際に作られるボリューム名は`db-data`単体ではなく`<プロジェクト名>_db-data`(この場合は`07-web-app-practice_db-data`のような名前)になる。`docker volume ls`で確認できる。

完全に同じ名前にしたい場合は`name`を明示する。

```yaml
volumes:
  db-data:
    name: db-data
```

**タイミングの違い**:

- `docker volume create db-data`: コマンド実行時に即座に作られる
- Composeの`volumes: db-data:`: `docker compose up`実行時に、まだ存在していなければ遅延作成される(ファイルに書いただけでは作られない)

---

前へ: [README](README.md)
