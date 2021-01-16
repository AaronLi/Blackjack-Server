import pyotp
from flask import Flask
from flask import request
from db.user import User, UserExistsException
from db import entry
from data.image import OCSimpleImage
import qrcode, logging, datetime

entry.connect()

app = Flask(__name__)


@app.route("/auth/register", methods=["POST"])
def auth():
    """
    Registers a new user.
    :return: an error message, or a success and a totp qr code that you will use for future logins
    """
    try:
        new_user_username = request.form["username"]
        if new_user_username and User.validate_username(new_user_username):
            new_user = User.register_user(new_user_username)
            user_totp_obj = pyotp.totp.TOTP(new_user.totp_base)
            qr_code_data = user_totp_obj.provisioning_uri(new_user_username, "Dumfing's MineLotto") # todo: replace with a value from a constants file
            qr_code_obj = qrcode.make(qr_code_data, box_size=1, border=2)
            serialized_qr_code = OCSimpleImage(qr_code_obj).serialize()
            new_user.save()
            logging.info(f"{new_user_username} registered at {datetime.datetime.now()} from {request.environ['REMOTE_ADDR']}")
            return f"success\n{serialized_qr_code}"
        return "failed\ninvalid username"

    except KeyError:
        return "failed\ninvalid username"
    except UserExistsException:
        return "failed\nuser exists"

@app.route("/auth/login", methods=["POST"])
def login():
    """
    Used to get an auth key that you will use while playing your game
    Logins uses fields called "username" and "totp"
    :return: An error message, or your auth key on success
    """
    login_username = request.form.get("username")
    try:
        user_obj = User.objects.get({"_id":login_username})
        login_totp = request.form.get("totp")
        if login_totp:
            login_success, auth_key = user_obj.try_login(login_totp)
            if login_success:
                logging.info(f"{login_username} logged in successfully")
                return f"success\n{auth_key}"

        logging.info(f"{login_username} failed to log in")
        return f"failed"
    except User.DoesNotExist:
        logging.info(f"Unknown user login by name of {login_username} from IP {request.environ['REMOTE_ADDR']}")
        return "failed\nuser does not exist"

if __name__ == '__main__':
    app.run()