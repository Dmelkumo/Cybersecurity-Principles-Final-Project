"""
David Melkumov
CS 166 Summer 2021
Lab 8

Basic setup for database, creates a database and table for
accounts. Inserts a few predefined users with varying access levels.
"""

from helpers import hash_password
import sqlite3


def create_db():
    """
    Creates an account database and accounts table
    to hold user's information
    """

    try:
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE accounts
                    (
                    username text,
                    password text,
                    access_level int
                    )''')
        conn.commit()
        print("Successfully created database and table")
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def insert_users():
    """
    Inserts some predefined users into the database
    """

    data = [("Dave", hash_password("123"), 3),
            ("Jeff", hash_password("1234"), 2),
            ("Fred", hash_password("111"), 1)]
    try:
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.executemany("INSERT INTO accounts VALUES (?, ?, ?)", data)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Successfully entered records")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def print_db():
    """
    Print all the rows in the table
    """
    try:
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM accounts"):
            print(row)
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # Create database (Comment these out except print to view the database)
    create_db()
    # Add some users
    insert_users()
    # Display database
    print_db()
