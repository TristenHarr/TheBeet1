import sqlite3

from TheBeets.Manager._FileController import FileController
from TheBeets.Manager._passwords import check_password
from TheBeets.conf import load_in
from cryptography.fernet import Fernet, MultiFernet
settings = load_in()


class User:

    def __init__(self, username):
        self.con = sqlite3.connect(settings['MAIN_DB'])
        self.c = self.con.cursor()
        self.user_items = None
        self.user_dict = None
        self.keys = None
        if self.user_exists(username):
            self.username = username
            self.password = self.c.execute("SELECT password FROM"
                                           " users WHERE username='{}'".format(username)).fetchone()[0]

    def load_user(self):
        self.user_items = self.c.execute("""SELECT id, email, email_verified, username, is_authenticated, 
                                            logged_in, first_name, last_name,
                                            active, reset_request 
                                            FROM users WHERE username='{}'""".format(self.username)).fetchall()[0]
        self.user_dict = {
                            'id': self.user_items[0],
                            'email': self.user_items[1],
                            'email_verified': self.user_items[2],
                            'username': self.user_items[3],
                            'is_authenticated': self.user_items[4],
                            'logged_in': self.user_items[5],
                            'first_name': self.user_items[6],
                            'last_name': self.user_items[7],
                            'active': self.user_items[8],
                            'reset_request': self.user_items[9]}
        return self.user_dict

    def user_exists(self, username):
        valid = self.c.execute("SELECT EXISTS(SELECT username "
                               "FROM users WHERE username = '{}')".format(username)).fetchone()[0]
        return valid

    def login_user(self, password):
        return check_password(password, self.password)

    def get_id(self):
        return self.user_dict['username']

    def is_authenticated(self):
        return self.user_dict['is_authenticated']

    def is_active(self):
        return self.user_dict['is_active']

    # def create_data_source(self, datasource):
    #     FileController().make_item(self.username, datasource, 'data_source')
    #
    # def delete_source(self, datasource):
    #     FileController().delete_item(self.username, datasource, 'data_source')


    # def fetch_models(self):
    #     return FileController().make_item(self.username, item=None, path_name='model', fetch=True)

    #
    # def load_in_keys(self):
    #     try:
    #         keys = self.c.execute("SELECT * FROM secrets WHERE username = '{}'".format(self.username)).fetchall()[0]
    #         ul = self.c.execute("SELECT * FROM secret_keys WHERE username = '{}'".format(self.username)).fetchall()[0]
    #         key1 = Fernet(ul[1])
    #         key2 = Fernet(ul[2])
    #         x = MultiFernet([key1, key2])
    #         access_token = x.decrypt(keys[1]).decode()
    #         access_token_secret = x.decrypt(keys[2]).decode()
    #         consumer_key = x.decrypt(keys[3]).decode()
    #         consumer_secret = x.decrypt(keys[4]).decode()
    #         token_dict = {"access_token": access_token, "access_token_secret": access_token_secret,
    #                       "consumer_key": consumer_key, "consumer_secret": consumer_secret}
    #         return token_dict
    #
    #         # return token_dict
    #     except AttributeError:
    #         return None
