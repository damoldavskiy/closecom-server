import sqlite3
import sys
from os.path import isfile

from constants import DATABASE_PATH


def migrate(path):
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()
    with open(path, 'r') as migration:
        cursor.executescript(migration.read())
    db.commit()
    db.close()


if __name__ == '__main__':
    if len(sys.argv) < 2 or not isfile(sys.argv[1]):
        print('Pass migration file as parameter')
    else:
        migrate(sys.argv[1])
