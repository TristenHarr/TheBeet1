import sqlite3

from TheBeets.Manager._passwords import make_password
from TheBeets.conf import load_in

settings = load_in()


class CreateUser:

    def __init__(self, data):
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.user_active = 1
        self.user_password_reset_request = False
        self.user_id = None
        self.con = sqlite3.connect(settings['MAIN_DB'])
        self.c = self.con.cursor()

    def user_exists(self):
        valid = self.c.execute("SELECT COUNT(*) from users WHERE username = '{}'".format(self.username)).fetchone()[0]
        return valid

    def get_id(self):
        return self.c.execute("SELECT MAX(id) FROM users").fetchone()[0]+1

    def make_account(self):
        self.user_id = self.get_id()
        valid = self.user_exists()
        if valid:
            return False
        else:
            self.con.execute("""INSERT INTO users VALUES ('{id}',
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
                            id=self.user_id,
                            email=self.email,
                            email_verified=0,
                            username=self.username,
                            password=make_password(self.password),
                            logged_in=0,
                            first_name="",
                            last_name="",
                            active=1,
                            reset_request=0,
                            is_authenticated=0))
            self.con.commit()
            self.con.close()
            return True
