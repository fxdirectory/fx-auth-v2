import pymysql
from conf.config import Config

def get_connection(database=None):
    cfg = Config.db_config(database)
    return pymysql.connect(**cfg)

def query(sql, params=None, fetch_one=False, fetch_all=False, database=None):
    conn = get_connection(database)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            if fetch_one:
                return cur.fetchone()
            if fetch_all:
                return cur.fetchall()
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()


def insert(sql, params=None, database=None):
    conn = get_connection(database)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()
