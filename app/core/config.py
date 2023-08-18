import os
import json
from pathlib import Path
from databases import DatabaseURL

ROOT_DIR = Path(__file__).parent.parent

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

MONGO_HOST = os.getenv('MONGO_HOST', '127.0.0.1')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USER = os.getenv('MONGO_USER', 'root')
MONGO_PASS = os.getenv('MONGO_PASSWORD', 'root')
MONGO_DB = os.getenv('MONGO_DB', 'flame-api')

MONGODB_URL = DatabaseURL(
    f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin'
)

database_name = MONGO_DB
users_collection_name = 'users'
users_details_collection_name = 'users_details'
foods_collection_name = 'foods'
foods_types_collection_name = 'foods_types'
meals_collection_name = 'meals'
dishes_collection_name = 'dishes'

FIREBASE_CONFIG_PATH = ROOT_DIR / 'static' / 'account.json'

with open(FIREBASE_CONFIG_PATH) as json_file:
    FIREBASE_CONFIG = json.load(json_file)
