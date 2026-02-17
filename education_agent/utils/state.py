from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    topic: str
    search_results: Optional[str]
    research_notes: Optional[str]
    final_content: Optional[str]
