# 02. 基本コマンド チートシート

[docs/02-basic-commands/README.md](../../docs/02-basic-commands/README.md) に沿って実際に手を動かしてみましょう。

## コンテナのライフサイクル

```bash
docker run -d --name web -p 8080:80 nginx   # 作成+起動
docker ps                                    # 実行中の一覧
docker ps -a                                 # 停止中も含めた一覧
docker stop web                              # 停止
docker start web                             # 再開
docker restart web                           # 再起動
docker rm web                                # 削除(停止済みのみ)
docker rm -f web                             # 強制削除(実行中でも)
```

## 中身を調べる

```bash
docker exec -it web bash      # コンテナ内でシェルを起動(bashがない場合はsh)
docker logs web               # ログ表示
docker logs -f web            # ログをリアルタイム追跡
docker inspect web            # 詳細情報(JSON)
docker top web                # コンテナ内で動いているプロセス一覧
docker stats                  # 全コンテナのCPU/メモリ使用状況(Ctrl+Cで終了)
```

## イメージ関連

```bash
docker images                 # イメージ一覧
docker rmi <イメージ名>        # イメージ削除
docker pull <イメージ名>       # イメージ取得のみ
```

## 掃除系コマンド

```bash
docker container prune   # 停止中コンテナを一括削除
docker image prune       # 未使用イメージを一括削除
docker volume prune       # 未使用ボリュームを一括削除
docker system prune       # 上記まとめて(確認プロンプトが出ます)
```

## 実習の流れ(例)

```bash
docker run -d --name web -p 8080:80 nginx
docker ps
docker exec -it web bash
# コンテナ内で: ls /usr/share/nginx/html && exit
docker logs web
docker stop web
docker ps -a
docker start web
docker stop web
docker rm web
docker ps -a
```
