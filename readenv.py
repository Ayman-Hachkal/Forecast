import os
from dotenv import load_dotenv

def load_env() -> str:
    load_dotenv()
    AOE_KEY = os.getenv("AOE_KEY")
    if AOE_KEY == None:
        AOE_KEY = "None"
    return AOE_KEY


