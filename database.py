from tinydb import TinyDB, Query
import datetime
import os

# Create DB folder if not exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize TinyDB
db = TinyDB('data/db.json')

# Tables
users_table = db.table('users')
knowledge_table = db.table('knowledge')
history_table = db.table('history')

User = Query()
Knowledge = Query()
History = Query()

# --- Knowledge Base Operations ---
def search_knowledge_base(topic):
    """
    Search for a topic in the knowledge base.
    Returns the content if found, else None.
    """
    # Simple case-insensitive search logic
    # TinyDB doesn't support regex natively in a simple way without custom test
    # We'll iterate or use a test function
    def match_topic(val):
        return val.lower() == topic.lower()

    result = knowledge_table.search(Knowledge.topic.test(match_topic))
    if result:
        return result[0]['content']
    return None

def save_to_knowledge_base(topic, content):
    """
    Save specific topic and content to the knowledge base.
    """
    if not search_knowledge_base(topic):
        knowledge_table.insert({
            'topic': topic,
            'content': content,
            'timestamp': str(datetime.datetime.now())
        })

# --- History Operations ---
def save_chat_history(username, topic, content):
    """
    Save chat history for a specific user.
    """
    summary = ""
    if isinstance(content, dict):
        summary = content.get('article', '')[:100] + "..."
    else:
        summary = str(content)[:100] + "..."
        
    history_table.insert({
        'username': username,
        'topic': topic,
        'summary': summary, 
        'full_content': content,
        'timestamp': str(datetime.datetime.now()) # Serialize date
    })

def get_user_history(username):
    """
    Get all chat history for a specific user, sorted by timestamp desc.
    """
    results = history_table.search(History.username == username)
    # Sort in memory
    results.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Needs _id for frontend keys? TinyDB uses doc_id
    for r in results:
        r['_id'] = r.doc_id
        
    return results

# --- User Operations ---
def get_user(username):
    result = users_table.search(User.username == username)
    return result[0] if result else None

def create_user(username, email, password_hash):
    if get_user(username):
        return False
        
    users_table.insert({
        'username': username,
        'email': email,
        'password': password_hash,
        'join_date': str(datetime.datetime.now())
    })
    return True

def update_user_password(username, new_password_hash):
    # Update documents where username matches
    updated = users_table.update({'password': new_password_hash}, User.username == username)
    return bool(updated)
