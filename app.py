import streamlit as st
import os
import time
import auth
import auth_ui
import database
import ast
from dotenv import load_dotenv
from education_agent.agents.orchestrator import Orchestrator

# Load environment variables
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="EduAgent AI",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "guest_chat_count" not in st.session_state:
    st.session_state.guest_chat_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login" # Login, Signup, Forgot

# --- Custom CSS for Premium Black Design ---
st.markdown("""
<style>
    /* 1. Global Background - Pure Black */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Georgia', serif;
    }

    /* 2. Glassmorphism Containers */
    .glass-card {
        background: rgba(20, 20, 20, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 2rem;
    }

    /* 3. Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }
    
    p, li, .stMarkdown {
        color: #cbd5e1;
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    /* 4. Chat Input Styling - Constrained Width */
    .stChatInput {
        max-width: 700px;
        margin: 0 auto;
        left: 0;
        right: 0;
        bottom: 2rem !important; /* Move up slightly */
    }
    
    /* 5. Center Content */
    .main-content {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 100px; /* Space for chat input */
    }

    /* 6. Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #1a1a1a;
    }
    
    /* 7. Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }

    /* Remove extra top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem;
    }
    
    /* Auth Modal Styling */
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border: 1px solid #333;
        border-radius: 10px;
        background: #111;
    }

    /* 8. Mobile Responsiveness */
    @media (max-width: 768px) {
        .glass-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .main-content {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .stChatInput {
            max-width: 95%;
            bottom: 1rem !important;
        }
        
        h1 { font-size: 2rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📚</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: -20px;'>EduAgent AI</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_profile = False
        st.rerun()

    # Profile Dropdown
    if st.session_state.logged_in:
        with st.expander(f"👤 {st.session_state.username}"):
            if st.button("My Profile"):
                st.session_state.show_profile = True
                st.rerun()
                
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = "Guest"
                st.session_state.messages = []
                st.session_state.show_profile = False
                st.rerun()
    else:
        st.info("👤 Guest Mode (Limited)")
        if st.session_state.guest_chat_count >= 5:
            st.error(f"Limit Reached: {st.session_state.guest_chat_count}/5")
        else:
            st.caption(f"Free Chats: {5 - st.session_state.guest_chat_count} remaining")
        
        if st.button("Login / Signup"):
             # We rely on LIMIT_REACHED logic or manual force
             st.session_state.force_login = True 
             st.rerun()

    st.markdown("---")
    
    # History Section
    if st.session_state.logged_in:
        st.markdown("### 🕒 History")
        history = database.get_user_history(st.session_state.username)
        if history:
            for item in history:
                # Use a unique key for each button
                if st.button(f"📄 {item['topic']}", key=str(item['_id'])):
                    # Load into chat
                    st.session_state.messages = [{"role": "user", "content": item['topic']}, 
                                                 {"role": "assistant", "content": item['full_content']}]
                    st.session_state.show_profile = False
                    st.rerun()
        else:
            st.caption("No history yet.")
    
    st.markdown("---")
    


# --- Auth Logic (If Limit Reached or Manual Login) ---
if "force_login" not in st.session_state:
    st.session_state.force_login = False
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

LIMIT_REACHED = (not st.session_state.logged_in) and (st.session_state.guest_chat_count >= 5)

if LIMIT_REACHED or st.session_state.force_login:
    # Render the new premium Auth UI
    auth_ui.render_auth_page()
    
    if st.button("Back to Guest Mode", use_container_width=False):
        st.session_state.force_login = False
        st.rerun()
        
    st.stop() # Stop execution if limit reached or manual login requested


# --- Profile View ---
if st.session_state.show_profile and st.session_state.logged_in:
    user_data = database.get_user(st.session_state.username)
    if user_data:
        st.markdown(f"""
        <div class="glass-card">
            <h1>👤 User Profile</h1>
            <p><strong>Username:</strong> {user_data['username']}</p>
            <p><strong>Email:</strong> {user_data.get('email', 'N/A')}</p>
            <p><strong>Member Since:</strong> {user_data.get('join_date', 'Unknown')}</p>
            <hr style="border-color: #333;">
            <p><em>Use the sidebar to view your learning history.</em></p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- Main Interface ---
# Using a container for the scrollable content area
main_container = st.container()

with main_container:
    # Header (Only show if no content generated yet)
    if not st.session_state.messages:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 3rem; margin-top: 5rem;">
                <h1 style="font-size: 3.5rem; font-weight: 800; background: -webkit-linear-gradient(#fff, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Knowledge Portal</h1>
                <p style="font-size: 1.2rem; color: #888;">Ask anything. Get a full course.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Helper: Render Content ---
    def render_content(content):
        # ATTEMPT TO PARSE STRINGIFIED DICT (Recovery for old data)
        if isinstance(content, str) and content.strip().startswith("{") and "'article':" in content:
            try:
                content = ast.literal_eval(content)
            except:
                pass

        if isinstance(content, dict):
            # 1. Article
            st.markdown(content.get('article', ''))
            
            # 2. Videos
            videos = content.get('videos', [])
            if videos:
                st.markdown("### 🎥 Related Videos")
                cols = st.columns(min(3, len(videos)))
                for i, vid in enumerate(videos):
                    with cols[i]:
                        st.video(vid['link'])
                        st.caption(vid['title'])
            
            # 3. Quiz
            quiz = content.get('quiz')
            if quiz and 'questions' in quiz:
                st.markdown("### 🧠 Knowledge Check")
                with st.expander("Take Quiz", expanded=False):
                    for idx, q in enumerate(quiz['questions']):
                        st.markdown(f"**{idx+1}. {q['question']}**")
                        
                        # Use a unique key for each question (based on hash or partial content to avoid dupes)
                        # We use a simplified key strategy here
                        key = f"quiz_{str(q['question'])[:10]}_{idx}"
                        answer = st.radio("Select an option:", q['options'], key=key)
                        
                        if st.button(f"Submit Answer {idx+1}", key=f"btn_{key}"):
                            if answer == q['correct_answer']:
                                st.success("✅ Correct! " + q['explanation'])
                            else:
                                st.error("❌ Incorrect. Try again!")
                st.markdown("---")
        else:
            # Fallback for simple string messages
            st.markdown(content)

    # Display Chat
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            render_content(message["content"])

# --- Chat Input at Bottom ---
if prompt := st.chat_input("What do you want to learn today?"):
    # Guest Limit Check
    if not st.session_state.logged_in and st.session_state.guest_chat_count >= 5:
        st.rerun() # Will hit the LIMIT_REACHED block above

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Check API Key
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ Groq API Key is missing.")
    else:
        # User Message
        with main_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                status_placeholder = st.empty()
                
                try:
                    # 1. Check Knowledge Base
                    status_placeholder.markdown("🧠 *Checking Knowledge Base...*")
                    cached_content = database.search_knowledge_base(prompt)
                    
                    if cached_content:
                        final_content = cached_content
                        status_placeholder.empty()
                    else:
                        # 2. Run Orchestrator
                        status_placeholder.markdown("🕵️ *Researching topic...*")
                        orchestrator = Orchestrator()
                        final_content = orchestrator.run(prompt)
                        
                        # 3. Save to KB (MongoDB handles dicts natively)
                        database.save_to_knowledge_base(prompt, final_content)
                    
                    # 4. Update State (Append to messages)
                    status_placeholder.empty()
                    st.session_state.messages.append({"role": "assistant", "content": final_content})
                    
                    # 5. Save History (User)
                    if st.session_state.logged_in:
                        database.save_chat_history(st.session_state.username, prompt, final_content)
                    else:
                        st.session_state.guest_chat_count += 1
                        
                    st.rerun()
                        
                except Exception as e:
                    status_placeholder.empty()
                    st.error(f"An error occurred: {e}")

    # --- Display Chat Messages (Outside the input block to persist) ---
    # We actually display messages at the top, but for the NEW message we rely on rerun.
    # Wait, the structure in the previous file was:
    # 1. Display existing messages
    # 2. Input
    #    -> Generate
    #    -> Append
    #    -> Rerun
    # So we don't need to display here. We just rerun.
