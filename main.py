import os
import argparse
from dotenv import load_dotenv
from education_agent.agents.orchestrator import Orchestrator

def main():
    load_dotenv()
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found. Please set it in your .env file.")
        return

    parser = argparse.ArgumentParser(description="Multi-Agent Education System (Powered by Groq & DuckDuckGo)")
    parser.add_argument("topic", type=str, help="The topic to research and write about.")
    # Removed manual search_results argument as we now have real search
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator()
        result = orchestrator.run(args.topic)
        
        print("\n" + "="*60)
        print(f"📘 COURSE GENERATED: {args.topic.upper()}")
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
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
