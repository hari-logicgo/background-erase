import os
from dotenv import load_dotenv

load_dotenv()

HF_SPACE = "LogicGoInfotechSpaces/background-remover" #changed to logicgoinfotech inference
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://harilogicgo_db_user:XPngX3FLb05C7wmR@bg-rem-db.vxixozn.mongodb.net/?retryWrites=true&w=majority&appName=bg-rem-db")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "logicgo@123")
