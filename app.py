"""
Streamlit UI for Log Analysis Agent
"""

import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from agent.graph import create_workflow
from agent.state import AgentState
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Log Analysis Agent",
    page_icon="logs",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .error-badge {
        background-color: #ff6b6b;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .warning-badge {
        background-color: #ffa500;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .success-badge {
        background-color: #51cf66;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'final_state' not in st.session_state:
    st.session_state.final_state = None
if 'workflow_app' not in st.session_state:
    st.session_state.workflow_app = create_workflow()

# Header
st.markdown("<h1 class='main-header'>Log Analysis Agent</h1>", unsafe_allow_html=True)
st.markdown("Intelligent log analysis using OpenAI, Reddit, Stack Overflow, and GitHub integration")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    st.subheader("API Keys Status")
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("OpenAI", "[OK]" if openai_key else "[NOT SET]")
        st.metric("Tavily", "[OK]" if tavily_key else "[NOT SET]")
    with col2:
        st.metric("GitHub", "[OK]" if github_token else "[NOT SET]")
    
    st.divider()
    
    st.subheader("About")
    st.info("""
    This tool analyzes log files and provides:
    - Error and warning extraction
    - External research (Wikipedia, Stack Overflow)
    - GitHub repository analysis
    - AI-powered solutions
    - Professional reports
    """)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["Input", "Analysis", "Results", "Download"])

with tab1:
    st.header("Step 1: Provide Log File")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option A: Upload File")
        uploaded_file = st.file_uploader(
            "Choose a log file",
            type=["txt", "log", "csv"],
            help="Upload your log file (max 200MB)"
        )
        
        if uploaded_file is not None:
            logs = uploaded_file.read().decode('utf-8')
            st.success(f"[LOADED] {uploaded_file.name}")
            st.info(f"[INFO] Size: {len(logs)} characters")
        else:
            logs = None
    
    with col2:
        st.subheader("Option B: Paste Text")
        pasted_logs = st.text_area(
            "Or paste your log content here",
            height=200,
            help="Paste your log file content directly"
        )
        
        if pasted_logs and not uploaded_file:
            logs = pasted_logs
            st.success(f"[PASTED] {len(logs)} characters")
    
    if not logs:
        st.warning("[WARNING] Please upload a file or paste log content")
        
        if st.button("Use Sample Log File"):
            sample_log = """2024-12-07 10:15:23 INFO Application started
2024-12-07 10:15:30 ERROR Database connection failed: Connection timeout
2024-12-07 10:15:31 ERROR Exception in thread "main" java.sql.SQLException: Connection refused
    at DatabaseConnector.connect(DatabaseConnector.java:45)
    at Application.init(Application.java:12)
2024-12-07 10:16:00 WARNING Memory usage high: 85%
2024-12-07 10:16:15 ERROR NullPointerException at UserService.getUser()
    at UserService.getUser(UserService.java:78)
2024-12-07 10:17:00 CRITICAL Disk space low: 95% used"""
            logs = sample_log
            st.session_state.logs = logs
            st.success("[LOADED] Sample log loaded")
            st.rerun()
    
    st.divider()
    st.header("Step 2: Optional Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        github_repo = st.text_input(
            "GitHub Repository URL (optional)",
            placeholder="https://github.com/username/repo",
            help="Enter GitHub repo URL for code analysis"
        )
    
    with col2:
        enable_github = st.checkbox(
            "Enable GitHub Analysis",
            value=bool(github_repo),
            help="Analyze related code in the repository"
        )
    
    if not enable_github:
        github_repo = None
    
    st.divider()
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        run_analysis = st.button(
            "Start Analysis",
            type="primary",
            use_container_width=True,
            disabled=not logs
        )
    
    with col2:
        if st.button("Reset", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.final_state = None
            st.rerun()

with tab2:
    st.header("Analysis Progress")
    
    if run_analysis and logs:
        with st.spinner("Starting analysis..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
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
                
                # Run workflow
                status_text.info("[*] Parsing logs...")
                progress_bar.progress(20)
                
                status_text.info("[*] Searching for solutions...")
                progress_bar.progress(40)
                
                status_text.info("[*] Analyzing code...")
                progress_bar.progress(60)
                
                status_text.info("[*] Generating solutions...")
                progress_bar.progress(80)
                
                status_text.info("[*] Building report...")
                # Run async workflow using asyncio.run()
                import asyncio
                final_state = asyncio.run(st.session_state.workflow_app.ainvoke(initial_state))
                
                progress_bar.progress(100)
                status_text.success("[SUCCESS] Analysis complete!")
                
                st.session_state.analysis_complete = True
                st.session_state.final_state = final_state
                
                st.rerun()
                
            except Exception as e:
                import traceback
                st.error(f"[ERROR] Error during analysis: {str(e)}")
                with st.expander("Details"):
                    st.code(traceback.format_exc())
                st.error("Please check your API keys and log content")
    
    elif st.session_state.analysis_complete and st.session_state.final_state:
        st.success("[SUCCESS] Analysis completed successfully!")
        st.info("Check the 'Results' tab to view detailed findings")
    
    else:
        st.info("[INFO] Click 'Start Analysis' to begin")

with tab3:
    st.header("Analysis Results")
    
    if st.session_state.analysis_complete and st.session_state.final_state:
        final_state = st.session_state.final_state
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Issues Found", final_state['error_count'])
        
        with col2:
            errors = [e for e in final_state['parsed_errors'] if e['type'] == 'ERROR']
            st.metric("Errors", len(errors))
        
        with col3:
            warnings = [e for e in final_state['parsed_errors'] if e['type'] == 'WARNING']
            st.metric("Warnings", len(warnings))
        
        with col4:
            st.metric("Solutions Found", len(final_state['solutions']))
        
        st.divider()

        # Visualizations (Enhancement)
        import plotly.express as px
        import pandas as pd
        
        st.subheader("Visual Analysis")
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Severity Distribution
            severity_counts = {}
            for e in final_state['parsed_errors']:
                sev = e.get('severity', 'UNKNOWN')
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            if severity_counts:
                df_sev = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
                fig_pie = px.pie(
                    df_sev, 
                    values='Count', 
                    names='Severity', 
                    title='Issue Severity Distribution',
                    color='Severity',
                    color_discrete_map={'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green', 'CRITICAL': 'darkred', 'UNKNOWN': 'grey'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No severity data available to plot")
                
        with viz_col2:
            # Timeline Visualization (if timestamps exist)
            valid_dates = []
            for e in final_state['parsed_errors']:
                if e.get('timestamp') and e['timestamp'] != 'N/A':
                    try:
                        # Attempt to parse common date formats if needed, or use string handling
                        valid_dates.append({'time': e['timestamp'], 'message': e['message'][:30], 'severity': e.get('severity', 'UNKNOWN')})
                    except:
                        pass
            
            if valid_dates:
                df_time = pd.DataFrame(valid_dates)
                fig_time = px.scatter(
                    df_time, 
                    x='time', 
                    y='severity', 
                    hover_data=['message'],
                    title='Incident Timeline',
                    color='severity',
                    size_max=20
                )
                st.plotly_chart(fig_time, use_container_width=True)
            else:
                st.info("No timestamp data available for timeline")

        st.divider()
        
        # Parsed Errors
        st.subheader("Parsed Errors & Warnings")
        
        if final_state['parsed_errors']:
            for idx, error in enumerate(final_state['parsed_errors'], 1):
                with st.expander(f"#{idx}: {error['message'][:60]}...", expanded=idx <= 2):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Type:** {error['type']}")
                        st.write(f"**Severity:** {error['severity']}")
                        st.write(f"**Timestamp:** {error.get('timestamp', 'N/A')}")
                        st.write(f"**Line:** {error['line_number']}")
                        st.write(f"**Message:** {error['message']}")
                        
                        if error.get('stack_trace'):
                            st.code(error['stack_trace'], language="text")
                    
                    with col2:
                        if error['type'] == 'ERROR':
                            st.markdown('<span class="error-badge">ERROR</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="warning-badge">WARNING</span>', unsafe_allow_html=True)
        else:
            st.info("[SUCCESS] No errors or warnings found!")
        
        st.divider()
        
        # Search Results
        st.subheader("External Research Results")
        
        if final_state['search_results']:
            for idx, result in enumerate(final_state['search_results'], 1):
                with st.expander(f"Research #{idx}: {result['error']['message'][:50]}...", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Wikipedia Result:**")
                        st.info(result.get('wikipedia', 'No results'))
                    
                    with col2:
                        st.write("**Stack Overflow Results:**")
                        so_results = result.get('stackoverflow', [])
                        if so_results:
                            for so in so_results:
                                st.markdown(f"[{so['title']}]({so['url']})")
                                st.caption(so['snippet'])
                        else:
                            st.info("No results")
        
        st.divider()
        
        # Solutions
        st.subheader("AI-Generated Solutions")
        
        if final_state['solutions']:
            for idx, solution in enumerate(final_state['solutions'], 1):
                with st.expander(f"Solution #{idx}", expanded=idx <= 1):
                    if isinstance(solution, dict):
                        st.json(solution)
                    else:
                        st.write(solution)
        else:
            st.info("No solutions generated")
        
        st.divider()
        
        # Final Report
        st.subheader("Complete Report")
        
        if final_state['final_report']:
            st.markdown(final_state['final_report'])
    
    else:
        st.info("[INFO] Complete analysis first to see results")

with tab4:
    st.header("Download Report")
    
    if st.session_state.analysis_complete and st.session_state.final_state:
        final_state = st.session_state.final_state
        
        # Generate report content
        report_content = final_state['final_report']
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="Download as Markdown",
                data=report_content,
                file_name=f"log_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            # Convert to plain text
            text_content = report_content.replace("# ", "").replace("## ", "").replace("### ", "")
            st.download_button(
                label="Download as Text",
                data=text_content,
                file_name=f"log_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # Export as JSON
            json_data = {
                "timestamp": datetime.now().isoformat(),
                "error_count": final_state['error_count'],
                "errors": final_state['parsed_errors'],
                "solutions": final_state['solutions'],
                "report": report_content
            }
            st.download_button(
                label="Download as JSON",
                data=json.dumps(json_data, indent=2),
                file_name=f"log_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.divider()
        
        # Report preview
        st.subheader("Report Preview")
        st.markdown(final_state['final_report'][:2000])
        st.info("[INFO] See the full report above or download it")
    
    else:
        st.info("[INFO] Complete analysis first to download report")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; margin-top: 30px;'>
    <p>Log Analysis Agent | Powered by OpenAI, LangGraph & Streamlit</p>
    <p>© 2024 | All rights reserved</p>
</div>
""", unsafe_allow_html=True)
