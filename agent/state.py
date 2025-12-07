"""
State definition for the log analysis agent.
"""

from typing import TypedDict, List, Dict, Optional, Annotated
import operator

class AgentState(TypedDict):
    """State that is passed between nodes in the graph"""
    logs: str
    github_repo: Optional[str]
    parsed_errors: List[Dict]
    search_results: Annotated[List[Dict], operator.add]
    code_analysis: Optional[str]
    solutions: List[Dict]
    final_report: str
    error_count: int
    status: str
