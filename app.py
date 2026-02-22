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

# ================= SPLINE BACKGROUND =================
def add_spline_background():
    # Embed Spline Viewer using HTML component
    # We use a script tag to load the viewer and the <spline-viewer> web component
    spline_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.72/build/spline-viewer.js"></script>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: transparent;
        }
        spline-viewer {
            width: 100%;
            height: 100%;
        }
    </style>
    </head>
    <body>
    <spline-viewer url="https://prod.spline.design/lGNzD2DC0ijG1K2C/scene.splinecode"></spline-viewer>
    </body>
    </html>
    """
    # Render with 1px height, CSS will handle full-screen expansion
    components.html(spline_html, height=100)

# Add background immediately
add_spline_background()

import uuid


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

# ================= CUSTOM CSS & JS INJECTION =================
def inject_custom_style():
    st.markdown(f"""
    <style>
    /* Hide Streamlit Default Elements (Footer, Menu, Header) */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stDecoration"] {{display: none;}}
    
    /* Hide specific deployment/github icons */
    .stDeployButton {{display: none;}}
    [data-testid="stToolbar"] {{
        visibility: visible !important;
        background-color: transparent !important;
    }}
    [data-testid="stHeader"] {{
        visibility: visible !important;
        background-color: transparent !important;
    }}
    .viewerBadge_container__1QSob {{display: none !important;}}

    /* FORCE VISIBILITY OF SIDEBAR TOGGLE - Natural Position */
    [data-testid="stSidebarCollapsedControl"] {{
        display: flex !important;
        visibility: visible !important;
        z-index: 1000000 !important;
        color: white !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        width: 44px !important;
        height: 44px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(5px) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        margin-top: 10px !important; 
        margin-left: 10px !important;
    }}
    
    [data-testid="stSidebarCollapsedControl"]:hover {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: white !important;
        transform: scale(1.05) !important;
    }}
    
    /* Ensure the icon inside is visible */
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: white !important;
        stroke: white !important;
        width: 24px !important;
        height: 24px !important;
    }}

    /* =========================================
       FORCE TRANSPARENCY ON ALL STREAMLIT LAYERS
       ========================================= */
    
    /* Force transparency on main containers */
    .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stAppViewBlockContainer"] {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    html, body {{
        background-color: #000000 !important;
    }}

    /* 3. Spline Background Iframe Styling */
    iframe {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: -1 !important; 
        border: none !important;
        pointer-events: none !important;
        display: block !important;
        transform: scale(1.4) !important;
        transform-origin: center center !important;
    }}
    
    /* 4. The inner content block (centering constraint) */
    .block-container {{
        background-color: transparent !important;
        padding-top: 2rem !important; /* Main content padding */
        max-width: 1100px;
    }}

    /* 5. Sidebar transparency & Positioning */
    /* 5. Sidebar transparency & Positioning */
    section[data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.1) !important; 
        background: rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(1px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 99999 !important;
    }}

    section[data-testid="stSidebar"] > div {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* Force text color in sidebar */
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    /* Move sidebar content up */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {{
        padding-top: 1rem !important;
        gap: 0.5rem !important;
    }}
    
    /* 6. Bottom Container - FORCE TRANSPARENCY */
    div[data-testid="stBottom"],
    div[data-testid="stBottom"] > div {{
        background-color: transparent !important;
        background: transparent !important;
        background-image: none !important;
        box-shadow: none !important;
        border: none !important;
    }}
    
    div[data-testid="stChatInputContainer"] {{
        background-color: transparent !important;
    }}
    
    div[data-testid="stChatInput"] {{
        background-color: transparent !important;
    }}
    
    .stChatInput {{
        background-color: transparent !important;
    }}
    
    .stChatInput textarea {{
        background-color: transparent !important;
        color: #eeeeee !important;
        caret-color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 24px !important;
        padding: 14px 20px !important;
        box-shadow: none !important;
    }}
    
    .stChatInput textarea:focus {{
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.1) !important;
    }}

    /* =========================================
       CHAT MESSAGE STYLING
       ========================================= */
    [data-testid="stChatMessage"] {{
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}
    
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }}

    /* =========================================
       LOGIN PAGE STYLING (Dark Glassmorphism)
       ========================================= */
    [data-testid="stForm"] {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 3rem 2rem !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    [data-testid="stForm"] input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    [data-testid="stForm"] button {{
        background-color: #ffffff !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }}
    
    [data-testid="stForm"] button:hover {{
        transform: scale(1.02) !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.3) !important;
    }}

    /* =========================================
       RESPONSIVE DESIGN ADAPTERS
       ========================================= */
    @media (max-width: 768px) {{
        .sidebar-title {{
            font-size: 1.5rem !important;
            margin-top: -10px !important;
        }}
        div[data-testid="stAppViewBlockContainer"] {{
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        .stChatInput {{
            bottom: 10px !important;
        }}
    }}
    
    @media (min-width: 769px) {{
        .sidebar-title {{
            font-size: 2.2rem !important;
            margin-top: -20px !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# Apply UI styles
inject_custom_style()

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
            st.markdown("### 📚 Course Material")
            st.markdown(content.get('article', ''))
            st.markdown("---")
            
            # 2. Videos
            videos = content.get('videos', [])
            if videos:
                st.markdown("### 🎥 Supplementary Videos")
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
