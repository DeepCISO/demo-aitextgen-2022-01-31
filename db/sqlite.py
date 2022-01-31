import sqlite3
import time
from sqlite3 import Error
from pprint import pprint


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn


def get_all_tweets(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets")

    rows = [dict(row) for row in cursor.fetchall()]
    return rows


def postprocess_tweets_to_common_format(rows):
    common = []
    for row in rows:
        common_row = create_common_format_dict(
            "twitter",
            time.mktime(time.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S %Z")),
            row["screen_name"],
            (  # 10x weight for RTs, arbitrarily set
                (row["retweets_count"] * 10) + row["likes_count"]
            ),
            row["tweet"],
        )
        common.append(common_row)
    return common


def create_common_format_dict(source, epoch, author, score, content):
    return {
        "source": source,
        "epoch": epoch,
        "author": author,
        "score": score,
        "content": content,
    }


def get_sqlite_twint(db_file):
    print("Loading tweets from sqlite database")
    conn = create_connection(db_file)
    rows = get_all_tweets(conn)
    print("Got tweets from sqlite database, preprocessing")
    common = postprocess_tweets_to_common_format(rows)
    print("Returning common-format tweet data from sqlite")
    return common
