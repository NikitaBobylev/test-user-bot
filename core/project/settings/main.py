from datetime import timedelta
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = environ.Env()

environ.Env.read_env(BASE_DIR / '.env')

api_id = env('api_id')
api_hash = env('api_hash')

db_username = env('db_username')
db_password = env('db_password')
db_host = env('db_host')
db_port = env('db_port')
db_name = env('db_name')


DELTA_FIRST_STAGE = timedelta(minutes=6)
DALTA_SECOND_STAGE = timedelta(minutes=39)
DALTA_LAST_STAGE = timedelta(days=1, hours=2)