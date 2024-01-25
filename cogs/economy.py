import random
import sqlite3
from functools import wraps
from typing import Tuple, List
import datetime


Entry = Tuple[int, int, str, int ,int] # id 0 , money 1 , pretty_name 2 , streak 3 , last_claim 4

class Economy:
    """A wrapper for the economy database"""
    def __init__(self):
        self.open()

    def open(self):
        """Initializes the database"""
        self.conn = sqlite3.connect('economy.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER NOT NULL PRIMARY KEY,
            money INTEGER NOT NULL DEFAULT 0,
            pretty_name TEXT NOT NULL DEFAULT doe,
            streak INTEGER NOT NULL DEFAULT 0,
            last_c INTEGER NOT NULL DEFAULT 0
        )""")

    def close(self):
        """Safely closes the database"""
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()

    def _commit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.conn.commit()
            return result
        return wrapper

    def get_entry(self, user_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM economy WHERE user_id=:user_id",
            {'user_id': user_id}
        )
        result = self.cur.fetchone()
        if result:
            return result
        return self.new_entry(user_id)

    @_commit
    def new_entry(self, user_id: int) -> Entry:
        try:
            self.cur.execute(
                "INSERT INTO economy(user_id, money, pretty_name, streak ,last_c) VALUES(?,?,?,?,?)",
                (user_id, 0, "none", 0, datetime.datetime.now().timestamp())
            )
            return self.get_entry(user_id)
        except sqlite3.IntegrityError:
            return self.get_entry(user_id)

    @_commit
    def remove_entry(self, user_id: int) -> None:
        self.cur.execute(
            "DELETE FROM economy WHERE user_id=:user_id",
            {'user_id': user_id}
        )

    @_commit
    def set_money(self, user_id: int, money: int) -> Entry:
        self.cur.execute(
            "UPDATE economy SET money=? WHERE user_id=?",
            (money, user_id)
        )
        return self.get_entry(user_id)

    @_commit
    def set_name(self, user_id: int, name: str) -> Entry:
        self.cur.execute(
            "UPDATE economy SET pretty_name=? WHERE user_id=?",
            (name, user_id)
        )
        return self.get_entry(user_id)

    @_commit
    def set_streak(self, user_id: int, streak: int) -> Entry:
        self.cur.execute(
            "UPDATE economy SET streak=? WHERE user_id=?",
            (streak, user_id)
        )
        return self.get_entry(user_id)

    @_commit
    def add_money(self, user_id: int, money_to_add: int) -> Entry:
        money = self.get_entry(user_id)[1]
        total = money + money_to_add
        if total < 0:
            total = 0
        self.set_money(user_id, total)
        return self.get_entry(user_id)

    @_commit
    def remove_money(self, user_id: int, money_to_remove: int) -> Entry:
        money = self.get_entry(user_id)[1]
        if money_to_remove > money:
            total = 0
        else:
            total = money - money_to_remove
        if total < 0:
            total = 0 #Final fail-safe 
        self.set_money(user_id, total)
        return self.get_entry(user_id)

    @_commit
    def add_streak(self, user_id: int, streak_to_add: int) -> Entry:
        streak = self.get_entry(user_id)[3]
        total = streak + streak_to_add
        if total < 0:
            total = 0
        self.set_streak(user_id, total)
        return self.get_entry(user_id)

    def random_entry(self) -> Entry:
        self.cur.execute("SELECT * FROM economy")
        return random.choice(self.cur.fetchall())

    def top_entries(self, n: int=0) -> List[Entry]:
        self.cur.execute("SELECT * FROM economy ORDER BY money DESC")
        return (self.cur.fetchmany(n) if n else self.cur.fetchall())

"""
eco = Economy()
uuid = random.randrange(1, 100)
eco.add_money(uuid, 100)
eco.set_name(uuid, "John")
print(eco.add_streak(uuid, 2))
"""