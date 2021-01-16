from datetime import timedelta
import re

TOKEN_LIFETIME = timedelta(minutes=10)

VALID_USERNAME_PATTERN = re.compile(r"([A-Za-z_0-9]){3,32}")