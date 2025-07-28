from decouple import RepositoryEnv, Config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
config = Config(RepositoryEnv(env_path))

DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = config("DB_PORT")

SECRET_KEY = config("SECRET_KEY")
