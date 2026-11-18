"""Thin MySQL helpers: one connection per call, dict rows."""
from contextlib import contextmanager

import mysql.connector

from config import DB


@contextmanager
def connection():
    conn = mysql.connector.connect(**DB)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def query(sql, params=(), one=False):
    """Run a SELECT; return list of dicts (or a single dict/None if one=True)."""
    with connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        rows = cur.fetchall()
    return (rows[0] if rows else None) if one else rows


def execute(sql, params=()):
    """Run INSERT/UPDATE/DELETE; return lastrowid."""
    with connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.lastrowid
