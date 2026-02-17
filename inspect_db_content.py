from pymongo import MongoClient
import os
from dotenv import load_dotenv
import pprint

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['edu_agent_db']

print("--- INSPECTING HISTORY COLLECTION ---")
history = list(db.history.find().sort('timestamp', -1).limit(3))

for item in history:
    print(f"\nUser: {item.get('username')}")
    print(f"Topic: {item.get('topic')}")
    content = item.get('full_content')
    print(f"Content Type: {type(content)}")
    print(f"Content Preview: {str(content)[:100]}...")
