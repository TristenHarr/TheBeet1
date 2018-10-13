import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sqlite3
from passlib.hash import pbkdf2_sha256

# Run this file for initial setup. This file creates an Admin login, and builds the user database.
def make_password(password):
    """
    Takes a password upon account creation and hashed it and stores it in the database.
    All password hashing is done using SHA256 encryption with a 16-bit salt.

    :param password:
    :return hashed_password:
    """
    # TODO: Rewrite this, increase security, look into some kind of database-row rotations
    hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hashed

def check_password(password, hashed):
    """
    Takes a password and the accounts hash value and verifies password is valid
    :param password:
    :param hashed:
    :return bool:
    """
    return pbkdf2_sha256.verify(password, hashed)

def config():
    """
    :return: Path of config file
    """
    ABSOLUTE_PATH = dir_path+'/CONFIG.txt'
    return ABSOLUTE_PATH

def directory():
    """
    Gets the current working directory
    :return: CWD
    """
    ABSOLUTE_PATH = dir_path
    return ABSOLUTE_PATH

def go(Admin, Password):
    """
    Takes as inputs the Admin username and password and creates the users table in the database
    Creates the configuration file that specifies project paths
    :calls: setup.py
    :param Admin:
    :param Password:
    :return:
    """
    file = open('CONFIG.txt', 'a')
    file.close()
    from TheBeets.conf import Config
    manager = Config()
    manager.setup_main_db()
    manager.set_users_db()
    from TheBeets.conf import load_in
    settings = load_in()
    conn = sqlite3.connect(settings['MAIN_DB'])
    conn.execute("CREATE TABLE IF NOT EXISTS {tn} (id INTEGER,"
                 "email TEXT,"
                 "email_verified INTEGER,"
                 "username TEXT,"
                 "password TEXT,"
                 "logged_in INTEGER, "
                 "first_name TEXT,"
                 "last_name TEXT,"
                 "active INTEGER,"
                 "reset_request INTEGER,"
                 "is_authenticated INTEGER,"
                 "PRIMARY KEY (username))".format(tn='users'))
    conn.commit()
    conn.execute("""INSERT INTO users VALUES ('{id}',
                          '{email}',
                          '{email_verified}',
                          '{username}',
                          '{password}',
                           {logged_in},
                           '{first_name}',
                           '{last_name}',
                           {active},
                           {reset_request},
                           {is_authenticated})""".format(
        id=1,
        email='admin@admin.com',
        email_verified=1,
        username=Admin,
        password=make_password(Password),
        logged_in=1,
        first_name="",
        last_name="",
        active=1,
        reset_request=0,
        is_authenticated=0))
    conn.commit()
    conn.close()
    from TheBeets.Manager._FileController import FileController
    FileController().file_handler(Admin)


if __name__ == '__main__':
    admin = input("Admin Username: ")
    password = input("Admin Password: ")
    go(admin, password)