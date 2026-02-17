from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime
import bcrypt

load_dotenv()

# Connect
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['edu_agent_db']

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("🌱 Seeding MongoDB...")

# 1. Create Test User
if not db.users.find_one({'username': 'test_user'}):
    db.users.insert_one({
        'username': 'test_user',
        'email': 'test@example.com',
        'password': hash_password('password123'),
        'join_date': datetime.datetime.now()
    })
    print("✅ Created 'test_user'.")
else:
    print("ℹ️ 'test_user' already exists.")

# 2. Add Knowledge
if not db.knowledge.find_one({'topic': 'MongoDB Basics'}):
    db.knowledge.insert_one({
        'topic': 'MongoDB Basics',
        'content': '# MongoDB Basics\nMongoDB is a NoSQL database...',
        'timestamp': datetime.datetime.now()
    })
    print("✅ Added 'MongoDB Basics' to knowledge base.")

# 3. Add History
if db.history.count_documents({'username': 'test_user'}) == 0:
    db.history.insert_one({
        'username': 'test_user',
        'topic': 'Introduction to AI',
        'summary': 'AI is the simulation of human intelligence...',
        'full_content': '# Introduction to AI\nArtificial Intelligence is...',
        'timestamp': datetime.datetime.now()
    })
    print("✅ Added sample history for 'test_user'.")

print("\nDONE! You can now refresh MongoDB Compass to see 'edu_agent_db'.")
