import streamlit as st
import streamlit.components.v1 as components
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

# ================= SPLINE BACKGROUND =================
def add_spline_background():
    # Inject CSS to make background transparent and handle the iframe
    st.markdown("""
        <style>
        /* Target all iframes that might be used for background */
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            z-index: -1 !important;
            margin: 0 !important;
            padding: 0 !important;
            pointer-events: none !important;
        }
        
        /* Aggressive transparency reset for all Streamlit containers */
        .stApp, .main, .block-container, 
        [data-testid="stHeader"], 
        [data-testid="stSidebar"], 
        [data-testid="stToolbar"],
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        [data-testid="stVerticalBlock"],
        [data-testid="stVerticalBlockBorderWrapper"],
        .st-emotion-cache-18ni7ap,
        .st-emotion-cache-zq5wmm,
        .st-emotion-cache-176l82e,
        .st-emotion-cache-1kyx60r {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* Glassmorphism for the main content area */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px);
            border-radius: 24px;
            margin-top: 5rem !important;
            margin-bottom: 10rem !important;
            padding: 3rem !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            max-width: 900px !important;
        }

        /* Glassmorphism for the Chat Input */
        [data-testid="stChatInput"] {
            background-color: rgba(255, 255, 255, 0.07) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            margin-bottom: 2rem !important;
        }
        
        /* Ensure the bottom container doesn't block background */
        [data-testid="stBottom"] > div {
            background: transparent !important;
        }
        
        /* Hide the specific component padding for background iframe */
        [data-testid="stVerticalBlock"] > div:has(iframe) {
            position: absolute !important;
            height: 0 !important;
            width: 0 !important;
            overflow: hidden !important;
        }
        
        /* Hide Streamlit elements */
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    spline_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.72/build/spline-viewer.js"></script>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: transparent;
        }
        spline-viewer {
            width: 100%;
            height: 100%;
        }
    </style>
    </head>
    <body style="background: transparent;">
    <spline-viewer url="https://prod.spline.design/lGNzD2DC0ijG1K2C/scene.splinecode"></spline-viewer>
    </body>
    </html>
    """
    # Use 1px height to ensure it's kept in DOM, CSS handles the rest
    components.html(spline_html, height=1)

# Add background immediately
add_spline_background()

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
                <h1 style="font-size: 3.5rem; font-weight: 800; background: -webkit-linear-gradient(#fff, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></h1>
                <p style="font-size: 1.2rem; color: #888;"></p>
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
