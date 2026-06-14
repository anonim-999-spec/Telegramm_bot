import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env.dev'))

API_TOKEN = env('API_TOKEN')
GROUP_ID = env('GROUP_ID')