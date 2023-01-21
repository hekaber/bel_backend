import os
import sys
from dotenv import load_dotenv

def load_env():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(BASE_DIR, "../config/.env"))
    sys.path.append(BASE_DIR)

def config(key: str):
    if os.environ[key] is None:
        raise Exception("Key config does not exist")
    return os.environ[key]