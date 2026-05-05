import sqlite3
import os
from config import DB_PATH, DATA_DIR


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS etf_info (
        code TEXT PRIMARY KEY,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS etf_nav (
        date TEXT,
        code TEXT,
        nav REAL,
        source TEXT,
        change_pct REAL,
        valid INTEGER,
        PRIMARY KEY(date, code)
    )
    """)

    conn.commit()
    conn.close()


def insert_etf_info(code, name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR IGNORE INTO etf_info (code, name)
    VALUES (?, ?)
    """, (code, name))

    conn.commit()
    conn.close()


def get_last_nav(code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT nav FROM etf_nav
    WHERE code=?
    ORDER BY date DESC LIMIT 1
    """, (code,))

    row = c.fetchone()
    conn.close()

    return row[0] if row else None


def insert_nav(date, code, nav, source, change_pct, valid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO etf_nav
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, code, nav, source, change_pct, int(valid)))

    conn.commit()
    conn.close()
