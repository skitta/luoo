import sqlite3


class Base():

    def __init__(self, dbpath):
        self.database = sqlite3.connect(dbpath)
        self.cur = self.database.cursor()
        self.table = self.cur.execute('CREATE TABLE IF NOT EXISTS song ('
                                      'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                                      'vol VARCHAR(3),'
                                      'track VARCHAR(2),'
                                      'name VARCHAR(100))')
        self.database.commit()

    def insert(self, data):
        self.cur.execute(
            "INSERT INTO song(vol, track, name) VALUES(?, ?, ?)", data)
        self.database.commit()

    def update(self, name):
        self.cur.execute("UPDATE song SET is_download=1 WHERE name=?", (name,))
        self.database.commit()

    def scan(self):
        self.cur.execute("SELECT vol FROM song GROUP BY vol")
        vols = [i[0] for i in self.cur.fetchall()]
        return vols

    def search(self, name):
        self.cur.execute("SELECT vol, track FROM song WHERE name=?", (name,))
        records = self.cur.fetchone()
        return records

    def __del__(self):
        self.database.close()
