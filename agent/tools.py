"""
Tool definitions for the log analysis agent.
"""

import os
import requests
from typing import List, Dict
from github import Github
import git
import tempfile
import shutil
from pathlib import Path

class ExternalTools:
    """Integrations with Wikipedia, Stack Overflow, and GitHub"""
    
    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
    
    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia for technical concepts"""
        try:
            import wikipedia
            wikipedia.set_lang("en")
            results = wikipedia.search(query, results=3)
            if results:
                summary = wikipedia.summary(results[0], sentences=3)
                return f"Wikipedia: {summary}"
            return "No Wikipedia results found."
        except Exception as e:
            return f"Wikipedia search error: {str(e)}"
    
    def search_stackoverflow(self, query: str) -> List[Dict]:
        """Search Stack Overflow using Tavily"""
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=self.tavily_api_key)
            
            response = client.search(
                query=f"{query} site:stackoverflow.com",
                max_results=5,
                search_depth="advanced"
            )
            
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('content', '')[:300]
                })
            return results
        except Exception as e:
            print(f"Stack Overflow search error: {e}")
            return []
    
    def analyze_github_repo(self, repo_url: str, error_keywords: List[str]) -> Dict:
        """Clone and analyze GitHub repository"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Clone repository
            print(f"Cloning repository: {repo_url}")
            repo = git.Repo.clone_from(repo_url, temp_dir)
            
            # Find relevant files
            code_files = []
            for ext in ['.py', '.js', '.java', '.cpp', '.go', '.ts']:
                code_files.extend(Path(temp_dir).rglob(f'*{ext}'))
            
            # Analyze files for error patterns
            relevant_code = []
            for file_path in code_files[:20]:  # Limit to 20 files
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check if file contains error keywords
                    for keyword in error_keywords:
                        if keyword.lower() in content.lower():
                            relevant_code.append({
                                'file': str(file_path.relative_to(temp_dir)),
                                'snippet': content[:500]
                            })
                            break
                except:
                    continue
            
            return {
                'repo_name': repo_url.split('/')[-1],
                'files_analyzed': len(code_files),
                'relevant_files': relevant_code[:5]  # Top 5 relevant files
            }
            
        except Exception as e:
            return {'error': str(e)}
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
