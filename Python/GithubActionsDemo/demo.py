import os
from dotenv import load_dotenv

load_dotenv()

secret_val = os.getenv("SECRET")
print(secret_val)