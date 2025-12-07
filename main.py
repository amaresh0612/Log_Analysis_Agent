"""
Main entry point for the log-analysis-agent application.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from agent.graph import create_workflow
from agent.state import AgentState
from datetime import datetime

def main():
    """Main execution function"""
    
    # Load environment variables
    load_dotenv()
    
    print("=" * 80)
    print("🤖 LOG ANALYSIS AGENT")
    print("=" * 80)
    print()
    
    # Get log file path
    log_file = input("Enter path to log file (or press Enter for sample): ").strip().strip('"')
    
    if not log_file:
        log_file = "logs/sample.log"
        print(f"Using sample log: {log_file}")
    
    # Read log file
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{log_file}' not found")
        print("\nCreating sample log file...")
        
        # Create sample log
        sample_log = """2024-12-07 10:15:23 INFO Application started
2024-12-07 10:15:30 ERROR Database connection failed: Connection timeout
2024-12-07 10:15:31 ERROR Exception in thread "main" java.sql.SQLException: Connection refused
    at DatabaseConnector.connect(DatabaseConnector.java:45)
    at Application.init(Application.java:12)
2024-12-07 10:16:00 WARNING Memory usage high: 85%
2024-12-07 10:16:15 ERROR NullPointerException at UserService.getUser()
    at UserService.getUser(UserService.java:78)
2024-12-07 10:17:00 CRITICAL Disk space low: 95% used"""
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/sample.log", 'w') as f:
            f.write(sample_log)
        
        logs = sample_log
    
    # Get GitHub repo (optional)
    github_repo = input("\nEnter GitHub repository URL (optional, press Enter to skip): ").strip()
    
    print("\n" + "=" * 80)
    print("Starting analysis...")
    print("=" * 80 + "\n")
    
    # Initialize state
    initial_state = AgentState(
        logs=logs,
        github_repo=github_repo if github_repo else None,
        parsed_errors=[],
        search_results=[],
        code_analysis=None,
        solutions=[],
        final_report="",
        error_count=0,
        status="Initializing"
    )
    
    # Create and run workflow
    app = create_workflow()
    final_state = app.invoke(initial_state)
    
    # Save report
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"log_analysis_report_{timestamp}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(final_state['final_report'])
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n📊 Total Issues Found: {final_state['error_count']}")
    print(f"📄 Report saved to: {report_file}")
    print("\n" + "=" * 80)
    
    # Display report preview
    print("\nREPORT PREVIEW:")
    print("-" * 80)
    print(final_state['final_report'][:1000])
    print("\n... (see full report in output file)")
    print("-" * 80)

if __name__ == "__main__":
    main()
