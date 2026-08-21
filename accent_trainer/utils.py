import sqlite3
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2",os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_words(db, user_id):
    with open(resource_path("2words.txt"), encoding="utf-8") as f:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        try:
            i = cur.execute("SELECT id FROM words").fetchall()[-1][0]
        except:
            i = 0
        try:
            j = cur.execute("SELECT id FROM word_stats").fetchall()[-1][0]
        except:
            j = 0

        for line in f:
            i += 1
            j += 1
            line = [line.strip() for line in line.split(",")]
            print(line)
            word = line[0]
            correct = line[1]
            wrong = line[2]
            id = i

            print(id, word, correct, wrong, user_id)
            cur.execute('INSERT INTO words (id, word, correct_accent, wrong_accent, user_id) VALUES (?, ?, ?, ?, ?)', (id, word, correct, wrong, user_id))
            print(1)
            print(j, user_id, id, 0, 0)
            cur.execute('INSERT INTO word_stats (id, user_id, word_id, correct_count, wrong_count) VALUES (?, ?, ?, ?, ?)', (j, user_id, id, 0, 0))
            conn.commit()

