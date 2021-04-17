# Credential access
import os

TOKEN = os.getenv("TOKEN")


TRANSMISSION = {
    "username": os.getenv("USER_TRANSMISSION"),
    "password": os.getenv("PASS_TRANSMISSION")
}
