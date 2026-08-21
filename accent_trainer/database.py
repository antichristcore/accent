import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="accent_trainer.db"):
        self.conn = sqlite3.connect(db_path)
        self.db = db_path
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users
                       (
                           id   INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT UNIQUE NOT NULL,
                           best_score INTEGER
                       )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS words
                       (
                           id             INTEGER PRIMARY KEY AUTOINCREMENT,
                           word           TEXT NOT NULL,
                           correct_accent TEXT NOT NULL,
                           wrong_accent   TEXT NOT NULL, 
                           user_id        INTEGER DEFAULT NULL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS results
                       (
                           id        INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id   INTEGER NOT NULL,
                           test_date TEXT    NOT NULL,
                           score     INTEGER NOT NULL,
                           total     INTEGER NOT NULL,
                           FOREIGN KEY (user_id) REFERENCES users (id)
                       )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS word_stats
                       (
                           id            INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id       INTEGER NOT NULL,
                           word_id       INTEGER NOT NULL,
                           correct_count INTEGER DEFAULT 0,
                           wrong_count   INTEGER DEFAULT 0,
                           FOREIGN KEY (user_id) REFERENCES users (id),
                           FOREIGN KEY (word_id) REFERENCES words (id)
                       )''')

        self.conn.commit()

    def add_user(self, name):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO users (name) VALUES (?)', (name,))
        self.conn.commit()
        cur.execute('SELECT id FROM users WHERE name = ?', (name,))
        return cur.fetchone()[0]

    def get_user_id(self, name):
        cur = self.conn.cursor()
        cur.execute('SELECT id FROM users WHERE name = ?', (name,))
        row = cur.fetchone()
        return row[0] if row else None

    def add_word(self, word, correct, wrong, user_id):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO words (word, correct_accent, wrong_accent, user_id) VALUES (?, ?, ?, ?)',
                    (word, correct, wrong, user_id))
        self.conn.commit()

    def get_random_words(self, n, user_id):
        cur = self.conn.cursor()
        cur.execute('SELECT id, word, correct_accent, wrong_accent FROM words WHERE user_id = ?', (user_id,))
        rows = cur.fetchall()
        import random
        return random.sample(rows, min(n, len(rows)))

    def get_all_words(self, user_id):
        cur = self.conn.cursor()
        cur.execute('SELECT id, word, correct_accent, wrong_accent FROM words WHERE user_id = ?', (user_id,))
        return cur.fetchall()

    def save_result(self, user_id, score, total, percentage):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO results (user_id, test_date, score, total) VALUES (?, ?, ?, ?)',
                    (user_id, datetime.now().isoformat(), score, total))
        old_percent = cur.execute('SELECT best_score FROM users WHERE id = ?', (user_id,)).fetchone()[0]
        if old_percent is None or percentage > old_percent:
            cur.execute('UPDATE users SET best_score = ? WHERE id = ?', (percentage, user_id))
        self.conn.commit()

    def update_stat(self, user_id, word_id, is_correct):
        cur = self.conn.cursor()
        cur.execute('SELECT id FROM word_stats WHERE user_id = ? AND word_id = ?', (user_id, word_id))
        row = cur.fetchone()[0]
        print(row)
        if row:
            if is_correct:
                cur.execute('UPDATE word_stats SET correct_count = correct_count + 1 WHERE user_id = ? AND word_id = ?',
                            (user_id, word_id))
            else:
                cur.execute('UPDATE word_stats SET wrong_count = wrong_count + 1 WHERE user_id = ? AND word_id = ?',
                            (user_id, word_id))
        self.conn.commit()

    def get_stats_for_user(self, user_id):
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*), ROUND(AVG(score*1.0/total), 1) FROM results WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        row2 = cur.execute('SELECT best_score from users WHERE id = ?', (user_id,)).fetchone()
        if row[0] is None:
            tests = 0
        else:
            tests = row[0]
        if row[1] is None:
            avg = 0.0
        else:
            avg = row[1]
        if row2[0] is None:
            best = 0
        else:
            best = row2[0]
        return {'tests': tests, 'avg': avg, 'best': best}
