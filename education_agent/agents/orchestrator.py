import os
from dotenv import load_dotenv
from education_agent.tools import video_search
from education_agent.agents import quiz_generator
from langchain_groq import ChatGroq
# Assuming we will use a simple synchronous orchestration for now
from .researcher import get_researcher_chain
from .writer import get_writer_chain

load_dotenv()

class Orchestrator:
    def __init__(self):
        # Ensure API Key is set
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found in environment variables.")
            
        self.llm = ChatGroq(model="llama-3.3-70b-versatile")
        self.researcher_chain = get_researcher_chain(self.llm)
        self.writer_chain = get_writer_chain(self.llm)

    def run(self, topic: str):
        print(f"--- [ORCHESTRATOR] Starting Process for Topic: {topic} ---")
        
        # Step 1: Research Phase
        print("--- [ORCHESTRATOR] Triggering Researcher Agent (with DuckDuckGo Search) ---")
        # The researcher chain now handles search internally based on the topic
        research_output = self.researcher_chain.invoke({"topic": topic})
        print("--- [RESEARCHER] Output Generated ---")
        # print(research_output) # Debugging

        # 3. Write Content
        print(f"--- [ORCHESTRATOR] Writing Content ---")
        article = self.writer_chain.invoke({"research_data": research_output})
        
        # 4. Fetch Multimedia (Videos)
        print(f"--- [ORCHESTRATOR] Fetching Videos ---")
        videos = video_search.get_youtube_links(topic)
        
        # 5. Generate Quiz
        print(f"--- [ORCHESTRATOR] Generating Quiz ---")
        try:
            quiz_chain = quiz_generator.get_quiz_chain(self.llm)
            quiz_data = quiz_chain.invoke({"topic": topic, "content": article})
        except Exception as e:
            print(f"Error generating quiz: {e}")
            quiz_data = None
            
        # --- LOGGING FORMATTED OUTPUT TO TERMINAL ---
        print("\n" + "="*60)
        print(f"📘 COURSE GENERATED: {topic.upper()}")
        print("="*60 + "\n")
        print(article)
        print("\n" + "-"*60)
        print(f"🎥 VIDEOS: {len(videos)} found")
        print("-"*60)
        for v in videos:
            print(f"▶ {v['title']} ({v['link']})")
        print("\n" + "-"*60)
        print("🧠 QUIZ")
        print("-"*60)
        if quiz_data and 'questions' in quiz_data:
            for idx, q in enumerate(quiz_data['questions'], 1):
                print(f"{idx}. {q['question']} (Ans: {q['correct_answer']})")
        print("="*60 + "\n")
        # --------------------------------------------

        return {
            "article": article,
            "research": research_output,
            "videos": videos,
            "quiz": quiz_data
        }
