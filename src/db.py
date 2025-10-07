import sqlite3
from typing import Dict, List, Any

DB_PATH = "database.db"

def connect_to_db():
    return sqlite3.connect(DB_PATH)

def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name    TEXT NOT NULL,
                email   TEXT NOT NULL,
                phone   TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
            """
        )
        conn.commit()
        print("User table ready.")
    finally:
        conn.close()

def _row_to_user(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "user_id": row["user_id"],
        "name": row["name"],
        "email": row["email"],
        "phone": row["phone"],
        "address": row["address"],
        "country": row["country"],
    }

def insert_user(user: Dict[str, Any]) -> Dict[str, Any]:
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user["name"], user["email"], user["phone"], user["address"], user["country"]),
        )
        conn.commit()
        return get_user_by_id(cur.lastrowid)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_users() -> List[Dict[str, Any]]:
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        return [_row_to_user(r) for r in rows]
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Dict[str, Any] | None:
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return _row_to_user(row) if row else None
    finally:
        conn.close()

def update_user(user: Dict[str, Any]) -> Dict[str, Any] | None:
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE users
            SET name = ?, email = ?, phone = ?, address = ?, country = ?
            WHERE user_id = ?
            """,
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"]),
        )
        conn.commit()
        return get_user_by_id(user["user_id"])
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def delete_user(user_id: int) -> Dict[str, str]:
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return {"status": "User deleted successfully"}
    except Exception:
        conn.rollback()
        return {"status": "Cannot delete user"}
    finally:
        conn.close()