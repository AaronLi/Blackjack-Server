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
    
    return "you're attempting to login but login isn't done yet :("
if __name__ == '__main__':
    app.run()