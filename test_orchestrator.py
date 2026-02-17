from education_agent.agents.orchestrator import Orchestrator
import os
from dotenv import load_dotenv

import sys
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

try:
    print("--- 🧪 Testing Orchestrator ---")
    orchestrator = Orchestrator()
    topic = "Black Holes"
    result = orchestrator.run(topic)
    
    print("\n" + "="*60)
    print(f"📘 COURSE GENERATED: {topic.upper()}")
    print("="*60 + "\n")
    
    print(result.get('article', 'No article generated.'))
    
    print("\n" + "-"*60)
    print("🎥 RECOMMENDED VIDEOS")
    print("-"*60)
    videos = result.get('videos', [])
    if videos:
        for v in videos:
            print(f"▶ {v['title']}")
            print(f"  Link: {v['link']}\n")
    else:
        print("No videos found.")
        
    print("-"*60)
    print("🧠 KNOWLEDGE CHECK")
    print("-"*60)
    quiz = result.get('quiz', {})
    if quiz and 'questions' in quiz:
        for idx, q in enumerate(quiz['questions'], 1):
            print(f"{idx}. {q['question']}")
            for opt in q.get('options', []):
                print(f"   - {opt}")
            print(f"   ✔ Answer: {q['correct_answer']}")
            print(f"   ℹ Explain: {q['explanation']}\n")
    else:
        print("No quiz generated.")
        
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
