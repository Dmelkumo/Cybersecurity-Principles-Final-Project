"""
David Melkumov
CS 166 Summer 2021
Lab 8

Contains helper functions relating to passwords (including hashing, authenticating,
and password generation/checking password strength) and database functions.
"""

import hashlib
import os
import sys
import random
import sqlite3

# Hashing functions:


def hash_password(plain_password) -> str:
    """
    Function to salt and hash the user's password

    :param plain_password: string password the user made
    :return: string the new hashed password with salt added
    """

    # Create a randomized salt to be added
    salt = os.urandom(20).hex()  # Needs 20 bytes for string to have 40 hex digits

    # Hash the password + randomly generated salt
    hashable = salt + plain_password
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()

    # Return the salt + hashed password
    return salt + this_hash


def authenticate(encrypted, attempt) -> bool:
    """
    Authenticate by hashing the password attempt

    :param encrypted: str encrypted salt and hash that belongs to that account
    :param attempt: str user's input
    :return: bool whether or not they match/login succeeded
    """

    # Constant for salt length
    SALT_LENGTH = 40

    # Get the salt from the encrypted password
    salt = encrypted[:SALT_LENGTH]

    # Get the password from the hashed part
    encrypted_pass = encrypted[SALT_LENGTH:]

    # Hash the password using the predefined salt
    hashable = salt + attempt
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()

    # Return bool if they match, meaning if they log in successfully
    return this_hash == encrypted_pass


# Password functions:


def test_password(password) -> bool:
    """
    Tests if the password satisfies the requirements and can be saved.

    :param password: str the user's password
    :return: bool whether or not it meets the requirements
    """

    # String of special characters to compare to
    SPECIAL_CHAR = "!@#$%^&*"

    # Ensure it is not all letters or only alphanumeric
    if password.isalnum() or password.isalpha():
        return False
    # Flags to determine if the password satisfies the requirements
    special_char_check = False
    has_upper = False
    has_lower = False
    has_digit = False
    # Iterate through to set the flags
    for ch in password:
        # Special characters check
        if ch in SPECIAL_CHAR:
            special_char_check = True
        # Uppercase letters check
        if ch.isupper():
            has_upper = True
        # Lowercase letters check
        if ch.islower():
            has_lower = True
        # Numbers check
        if ch.isdigit():
            has_digit = True
    # Return false if it doesnt satisfy all of them
    if not special_char_check or \
            not has_upper or \
            not has_lower or \
            not has_digit:
        return False
    # Otherwise return true
    else:
        return True


def generate_strong_pass():
    """
    Generates a strong password using random ints to select indices until
    they create a valid password

    :return: string strong password
    """

    # Constants for password requirements
    MIN_LEN = 8
    MAX_LEN = 25
    CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '@', '#', '$', '%', '^', '&', '*',
                  '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Initialize password
    password = ""
    while not test_password(password):
        # Reset password
        password = ""
        # Fill it with random characters
        for i in range(random.randint(MIN_LEN, MAX_LEN)):
            password += CHARACTERS[random.randint(0, len(CHARACTERS) - 1)]

    # Return the strong password
    return password


# Database functions:


def get_from_db(query, data):
    """
    Function to get info from database using the query and data

    :param query: string for the query to execute
    :param data: list of data to insert into query (parameterized)
    :return: list for row data
    """

    # Get data from database table
    try:
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute(query, data)
        row = c.fetchone()
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
        # Close the program if it fails
        sys.exit()
    else:
        # Return the data
        return row
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def write_to_db(query, data):
    """
    Function to write info to the database

    :param query: string for the query to execute
    :param data: list of data to insert into query (parameterized)
    """

    try:
        conn = sqlite3.connect('account.db')
        c = conn.cursor()
        c.execute(query, data)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()
