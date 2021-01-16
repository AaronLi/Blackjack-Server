import os
from datetime import datetime

import pymodm
import pyotp
import qrcode
import sys

from blackjack.blackjackgamestate import dispatcher, state
from db import user, game


def connect():
    connection_address = os.getenv("MONGO_CONNECTION")
    pymodm.connect(connection_address)


if __name__ == '__main__':
    username = input("Log in as?\n>>> ")
    try:
        active_user = user.User.get_user_by_username(username)
        otp_obj = pyotp.TOTP(active_user.totp_base)
    except user.User.DoesNotExist:
        print("dne")
        should_register = input("Register? (y/n)")
        if should_register == 'y':
            active_user = user.User.register_user(username)
            active_user.save()
            otp_obj = pyotp.TOTP(active_user.totp_base)
            auth_uri = otp_obj.provisioning_uri(name=active_user.username, issuer_name="MineLotto")
            qrcode.make(auth_uri).show()
        else:
            sys.exit(0)

    active_user.last_logon = datetime.now()
    active_user.save()

    if otp_obj.verify(input("Enter OTP: ")):
        # logged in
        if active_user.current_game is None:
            new_game = game.Game(player=active_user).save()
            active_user.current_game = new_game
            active_user.save()

        if active_user.balance > 0:

            while active_user.current_game.state != state.State.END:
                print(dispatcher.Dispatcher.poll(active_user.current_game))
                u_in = input("Move: ")
                new_game_state, response_string = dispatcher.Dispatcher.input(active_user.current_game, u_in)
                new_game_state.save()
            active_user.current_game.delete()
            active_user.save()
        else:
            print("Your balance is too low to play")
