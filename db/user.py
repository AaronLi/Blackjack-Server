from datetime import datetime

import pyotp
import random
import re
from pymodm import MongoModel, fields

from db import TOKEN_LIFETIME, VALID_USERNAME_PATTERN
from db.game import Game

class UserExistsException(Exception):
    pass

class User(MongoModel):
    username = fields.CharField(verbose_name="Username", min_length=3, max_length=16, primary_key=True)
    balance = fields.IntegerField(verbose_name="Balance", min_value=0)
    totp_base = fields.CharField(verbose_name="TOTP")
    auth_token = fields.CharField()
    auth_token_expiry = fields.DateTimeField()
    last_logon = fields.DateTimeField(default=datetime.now())
    current_game = fields.ReferenceField(Game, on_delete=fields.ReferenceField.NULLIFY, verbose_name="Current Game", blank=True)

    def __repr__(self) -> str:
        return f"<User(username={self.username}, balance={self.balance}, totp_base={self.totp_base}, current_game={self.current_game})>"

    @staticmethod
    def register_user(username):
        try:
            User.objects.get({"_id":username})
            raise UserExistsException(f"The username {username} is taken")
        except User.DoesNotExist:
            return User(username=username, balance=0, totp_base = pyotp.random_base32())

    @staticmethod
    def get_user_by_username(username):
        return User.objects.get({"_id":username})

    def try_login(self, totp):
        otp_obj = pyotp.TOTP(self.totp_base)
        if otp_obj.verify(totp):
            self.auth_token = hex(random.getrandbits(128))[2:]
            self.auth_token_expiry = datetime.now() + TOKEN_LIFETIME
            return True, self.auth_token
        return False, None

    def check_token(self, token):
        if self.auth_token == token:
            if datetime.now() < self.auth_token_expiry:
                return True
        return False

    @staticmethod
    def validate_username(username):
        return re.fullmatch(VALID_USERNAME_PATTERN, username)