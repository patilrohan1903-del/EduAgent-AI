from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

# --- MongoDB Connection ---
# Default to local if not provided
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['edu_agent_db']

# Collections
users_collection = db['users']
knowledge_collection = db['knowledge']
history_collection = db['history']

# --- Knowledge Base Operations ---
def search_knowledge_base(topic):
    """
    Search for a topic in the knowledge base.
    Returns the content if found, else None.
    """
    # Create text index if not exists (handled by MongoDB automatically generally, but for regex search we use $regex)
    # Using regex for case-insensitive search
    result = knowledge_collection.find_one({"topic": {"$regex": f"^{topic}$", "$options": "i"}})
    if result:
        return result['content']
    return None

def save_to_knowledge_base(topic, content):
    """
    Save specific topic and content to the knowledge base.
    """
    # Avoid duplicates
    if not search_knowledge_base(topic):
        knowledge_collection.insert_one({
            'topic': topic,
            'content': content,
            'timestamp': datetime.datetime.now()
        })

# --- History Operations ---
def save_chat_history(username, topic, content):
    """
    Save chat history for a specific user.
    """
    # Create summary based on content type
    summary = ""
    if isinstance(content, dict):
        summary = content.get('article', '')[:100] + "..."
    else:
        summary = str(content)[:100] + "..."
        
    history_collection.insert_one({
        'username': username,
        'topic': topic,
        'summary': summary, 
        'full_content': content,
        'timestamp': datetime.datetime.now()
    })

def get_user_history(username):
    """
    Get all chat history for a specific user, sorted by timestamp desc.
    """
    cursor = history_collection.find({'username': username}).sort('timestamp', -1)
    return list(cursor)

# --- User Operations ---
def get_user(username):
    return users_collection.find_one({'username': username})

def create_user(username, email, password_hash):
    users_collection.insert_one({
        'username': username,
        'email': email,
        'password': password_hash,
        'join_date': datetime.datetime.now()
    })
    return True

def update_user_password(username, new_password_hash):
    result = users_collection.update_one(
        {'username': username},
        {'$set': {'password': new_password_hash}}
    )
    return result.modified_count > 0
