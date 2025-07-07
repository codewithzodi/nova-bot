import sqlite3
from contextlib import closing

DB_PATH = "nova_bot.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS confessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            confession TEXT,
            group_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_id INTEGER,
            count INTEGER DEFAULT 0,
            last_warned TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_id INTEGER,
            score INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_id INTEGER,
            event TEXT,
            event_time TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            key TEXT,
            value TEXT
        )''')
        conn.commit()

# Example CRUD for users
def add_user(user_id, username, first_name, last_name):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)''',
                  (user_id, username, first_name, last_name))
        conn.commit()

def get_user(user_id):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return c.fetchone()

# Add similar CRUD functions for confessions, warnings, scores, events, settings as needed.

def add_warning(user_id, group_id):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('SELECT count FROM warnings WHERE user_id = ? AND group_id = ?', (user_id, group_id))
        row = c.fetchone()
        if row:
            count = row[0] + 1
            c.execute('UPDATE warnings SET count = ?, last_warned = CURRENT_TIMESTAMP WHERE user_id = ? AND group_id = ?', (count, user_id, group_id))
        else:
            count = 1
            c.execute('INSERT INTO warnings (user_id, group_id, count) VALUES (?, ?, ?)', (user_id, group_id, count))
        conn.commit()
        return count

def get_warning_count(user_id, group_id):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('SELECT count FROM warnings WHERE user_id = ? AND group_id = ?', (user_id, group_id))
        row = c.fetchone()
        return row[0] if row else 0

def set_custom_command(group_id, command, response):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO settings (group_id, key, value) VALUES (?, ?, ?)''',
                  (group_id, f'custom_command_{command}', response))
        conn.commit()

def remove_custom_command(group_id, command):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''DELETE FROM settings WHERE group_id = ? AND key = ?''',
                  (group_id, f'custom_command_{command}'))
        conn.commit()

def get_custom_command(group_id, command):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''SELECT value FROM settings WHERE group_id = ? AND key = ?''',
                  (group_id, f'custom_command_{command}'))
        row = c.fetchone()
        return row[0] if row else None

def add_confession(user_id, confession, group_id):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO confessions (user_id, confession, group_id) VALUES (?, ?, ?)''', (user_id, confession, group_id))
        conn.commit()
        return c.lastrowid

def add_score(user_id, group_id, points):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('SELECT score FROM scores WHERE user_id = ? AND group_id = ?', (user_id, group_id))
        row = c.fetchone()
        if row:
            score = row[0] + points
            c.execute('UPDATE scores SET score = ? WHERE user_id = ? AND group_id = ?', (score, user_id, group_id))
        else:
            score = points
            c.execute('INSERT INTO scores (user_id, group_id, score) VALUES (?, ?, ?)', (user_id, group_id, score))
        conn.commit()
        return score

def get_leaderboard(group_id, limit=10):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''SELECT users.username, scores.score FROM scores JOIN users ON scores.user_id = users.user_id WHERE scores.group_id = ? ORDER BY scores.score DESC LIMIT ?''', (group_id, limit))
        return c.fetchall()

def get_setting(group_id, key):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('SELECT value FROM settings WHERE group_id = ? AND key = ?', (group_id, key))
        row = c.fetchone()
        return row[0] if row else None

def set_setting(group_id, key, value):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO settings (group_id, key, value) VALUES (?, ?, ?)', (group_id, key, value))
        conn.commit()

def add_event(user_id, group_id, event, event_time):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO events (user_id, group_id, event, event_time) VALUES (?, ?, ?, ?)', (user_id, group_id, event, event_time))
        conn.commit() 