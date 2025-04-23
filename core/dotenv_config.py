from dotenv import load_dotenv
import os

_ = load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))
