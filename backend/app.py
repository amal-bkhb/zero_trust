from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "database"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "studydb"),
    "user": os.getenv("DB_USER", "studyuser"),
    "password": os.getenv("DB_PASSWORD", "studypass"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def initialize_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL
                );
                """
            )
            cur.execute("SELECT COUNT(*) FROM notes;")
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute("INSERT INTO notes (content) VALUES (%s);", ("hello from database",))


@app.route("/api/data")
def get_data():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, content FROM notes ORDER BY id LIMIT 1;")
                row = cur.fetchone()
                if row is None:
                    return jsonify({"message": "No rows found"})
                return jsonify({"id": row[0], "content": row[1]})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    initialize_db()
    app.run(host="0.0.0.0", port=5001)
