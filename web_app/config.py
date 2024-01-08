import os
from dotenv import load_dotenv


ENV = os.getenv("ENV")

if ENV == 'TEST':
    load_dotenv('.env.test')
else:
    load_dotenv('.env')


PG_PASSW = os.getenv("PG_PASSW")
PG_USER = os.getenv("PG_USER")
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
ENGINE = os.getenv("ENGINE")
POSTGRESS_DB = os.getenv("POSTGRESS_DB")

BASE_URL = f'{ENGINE}://{PG_USER}:{PG_PASSW}@{HOST}:{PORT}'
POSTGRESS_DB = 'postgres'

ENGINE_OPTIONS = {'echo': True}
