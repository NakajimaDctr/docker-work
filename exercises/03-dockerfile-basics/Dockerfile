# ベースになるイメージ
FROM python:3.12-slim

# コンテナ内の作業ディレクトリを指定（同時にカレントディレクトリになる）
# コンテナをdocker runで起動したときも、このWORKDIRがコンテナ内の初期カレントディレクトリになる
WORKDIR /app

# ホスト(自分のPC)のファイルをイメージにコピー
# hello.pyをコンテナ内のカレントディレクトリ（=WORKDIR）にコピーする
COPY hello.py .

# コンテナ起動時に実行するデフォルトのコマンド
# exec形式（JSON配列で書く方式）→shell形式だと`CMD python hello.py`
# shを介さないためdocker stopなどのシグナルが直接pythonに届く（無視されない）、
# 余計なシェルプロセスが立たないのような利点がある
CMD ["python", "hello.py"]
