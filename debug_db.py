from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['edu_agent_db']

print("\n--- 🗄️ MongoDB Dashboard ---")
print(f"Connected to: {MONGO_URI}")
print(f"Database: {db.name}\n")

# 1. Users
users_count = db.users.count_documents({})
print(f"👥 Users ({users_count}):")
for user in db.users.find():
    print(f"   - {user.get('username')} (Joined: {user.get('join_date')})")

# 2. Knowledge Base
kb_count = db.knowledge.count_documents({})
print(f"\n🧠 Knowledge Base Items ({kb_count}):")
for item in db.knowledge.find().limit(5):
    print(f"   - {item.get('topic')}")

# 3. Chat History
hist_count = db.history.count_documents({})
print(f"\n🕒 Chat History Records ({hist_count}):")
for record in db.history.find().limit(5):
    print(f"   - [{record.get('username')}] {record.get('topic')} ({record.get('timestamp')})")

print("\n------------------------------")
