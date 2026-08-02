import os
import time

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("POSTGRES_DB", "app")
DB_USER = os.environ.get("POSTGRES_USER", "app")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "app")


def get_connection(retries=10, delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
        except psycopg2.OperationalError as e:
            last_error = e
            print(f"DBへの接続待機中... ({attempt}/{retries})")
            time.sleep(delay)
    raise RuntimeError(f"DBに接続できませんでした: {last_error}")


def init_db():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
                """
            )
    conn.close()


@app.route("/notes", methods=["GET"])
def list_notes():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text, created_at FROM notes ORDER BY id")
            rows = cur.fetchall()
    conn.close()
    notes = [{"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows]
    return jsonify(notes)


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(force=True)
    text = data.get("text", "")
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (text) VALUES (%s) RETURNING id", (text,)
            )
            note_id = cur.fetchone()[0]
    conn.close()
    return jsonify({"id": note_id, "text": text}), 201


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
