"""
Node definitions for the log analysis agent graph.
"""

from langchain_openai import ChatOpenAI
from agent.state import AgentState
from agent.tools import ExternalTools
from utils.parsers import LogParser
import json

class AgentNodes:
    """Node implementations for the LangGraph workflow"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=4000
        )
        self.tools = ExternalTools()
        self.parser = LogParser()
    
    def parse_logs_node(self, state: AgentState) -> AgentState:
        """Node 1: Parse logs and extract errors"""
        print("[*] Parsing logs...")
        
        parsed_errors = self.parser.parse_logs(state['logs'])
        
        state['parsed_errors'] = parsed_errors
        state['error_count'] = len(parsed_errors)
        state['status'] = f"Found {len(parsed_errors)} issues"
        
        print(f"[+] Found {len(parsed_errors)} errors/warnings")
        return state
    
    def search_solutions_node(self, state: AgentState) -> AgentState:
        """Node 2: Search external sources for solutions"""
        print("[*] Searching for solutions...")
        
        search_results = []
        
        for error in state['parsed_errors'][:5]:  # Limit to top 5 errors
            error_query = error['message'][:100]  # Truncate long messages
            
            print(f"  [*] Searching for: {error_query[:50]}...")
            
            # Search Wikipedia
            wiki_result = self.tools.search_wikipedia(error_query)
            
            # Search Stack Overflow
            so_results = self.tools.search_stackoverflow(error_query)
            
            search_results.append({
                'error': error,
                'wikipedia': wiki_result,
                'stackoverflow': so_results[:3]
            })
        
        # Return updated state with search_results
        state['search_results'] = search_results
        print(f"[+] Completed external searches")
        return state
    
    def analyze_code_node(self, state: AgentState) -> AgentState:
        """Node 3: Analyze GitHub repository if provided"""
        if not state.get('github_repo'):
            print("[!] No GitHub repo provided, skipping code analysis")
            state['code_analysis'] = None
            return state
        
        print(f"[*] Analyzing GitHub repository: {state['github_repo']}")
        
        # Extract error keywords for searching
        error_keywords = [e['message'].split()[0] for e in state['parsed_errors'][:5]]
        
        # Analyze repository
        analysis = self.tools.analyze_github_repo(state['github_repo'], error_keywords)
        
        state['code_analysis'] = json.dumps(analysis, indent=2)
        print(f"[+] Code analysis complete")
        return state
    
    def generate_solutions_node(self, state: AgentState) -> AgentState:
        """Node 4: Generate comprehensive solutions using LLM"""
        print("[*] Generating solutions...")
        
        prompt = f"""You are an expert DevOps engineer analyzing application logs.

ERRORS FOUND ({len(state['parsed_errors'])}):
{json.dumps(state['parsed_errors'], indent=2)}

EXTERNAL RESEARCH:
{json.dumps(state['search_results'], indent=2)}

CODE ANALYSIS:
{state.get('code_analysis', 'No repository provided')}

For each error, provide:
1. Root cause analysis
2. Step-by-step solution
3. Code fix (if applicable)
4. Prevention strategy
5. Confidence score (1-10)

Return your analysis as a JSON array of solutions."""
        
        response = self.llm.invoke(prompt)
        
        try:
            # Try to parse JSON response
            solutions_text = response.content
            
            # Extract JSON if wrapped in markdown
            if '```json' in solutions_text:
                solutions_text = solutions_text.split('```json')[1].split('```')[0]
            elif '```' in solutions_text:
                solutions_text = solutions_text.split('```')[1].split('```')[0]
            
            solutions = json.loads(solutions_text)
        except:
            # If parsing fails, use raw response
            solutions = [{'analysis': response.content}]
        
        state['solutions'] = solutions
        print(f"[+] Generated {len(solutions)} solutions")
        return state
    
    def build_report_node(self, state: AgentState) -> AgentState:
        """Node 5: Build final report"""
        print("[*] Building final report...")
        
        prompt = f"""Create a professional log analysis report in Markdown format.

DATA:
- Total Errors: {state['error_count']}
- Parsed Errors: {json.dumps(state['parsed_errors'], indent=2)}
- Solutions: {json.dumps(state['solutions'], indent=2)}
- Repository: {state.get('github_repo', 'Not provided')}

Create a report with these sections:
# Log Analysis Report

## Executive Summary
- Provide key metrics and overview

## Critical Issues
- List errors by severity

## Detailed Analysis
For each error:
- Root cause
- Solution steps
- Code fixes
- External resources

## Priority Matrix
| Priority | Issue | Severity | Effort |
|----------|-------|----------|--------|

## Recommendations
- Prevention strategies
- Next steps

Keep it professional, actionable, and well-formatted."""
        
        response = self.llm.invoke(prompt)
        state['final_report'] = response.content
        
        print("[+] Report generated successfully")
        return state
