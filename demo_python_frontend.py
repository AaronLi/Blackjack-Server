import requests
from data import image

key = None

server_ip = "http://127.0.0.1:5000"

if __name__ == '__main__':
    username = input("Username: ")
    register = input("Register? (y/n) ")
    if register.lower() == 'y':
        response = requests.post(f"{server_ip}/auth/register", {"username":username}).text.split("\n")
        image.OCSimpleImage().deserialize(response[1], scale=4).show()
    while True:
        poll_game = requests.post(f"{server_ip}/game/blackjack",
                                  {"username": username, "auth": key, "action": "poll"}).text
        response_data = poll_game.split("\n")
        success = response_data[0]
        response_info = '\n'.join(response_data[1:])
        if success == "success":
            print(poll_game)
            player_move = input("Move: ")
            move_attempt = requests.post(f"{server_ip}/game/blackjack", {"username": username, "auth": key, "action": "input", "move": player_move}).text
            #print(move_attempt)
        else:
            # login
            print(response_info)
            totp = input("totp: ")
            login_attempt = requests.post(f"{server_ip}/auth/login", {"username": username, "totp": totp}).text
            login_response = login_attempt.split("\n")
            print(login_response)
            login_response_code = login_response[0]
            if login_response_code == "success":
                key = login_response[1]
