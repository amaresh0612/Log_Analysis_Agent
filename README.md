# Log Analysis Agent - Complete Setup Guide

## Project Structure

```
log-analysis-agent/
├── .env
├── requirements.txt
├── main.py
├── agent/
│   ├── __init__.py
│   ├── state.py
│   ├── tools.py
│   ├── nodes.py
│   └── graph.py
├── utils/
│   ├── __init__.py
│   └── parsers.py
├── logs/
└── output/
```

---

## Setup Instructions

### 1. Create project directory
```bash
mkdir log-analysis-agent
cd log-analysis-agent
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create directory structure
```bash
mkdir agent utils logs output
```

### 5. Configure environment
Update `.env` file with your API keys:
- OpenAI API: https://platform.openai.com/api-keys
- Tavily API: https://tavily.com/
- GitHub Token: https://github.com/settings/tokens

### 6. Run the agent

#### Option A: Streamlit Web UI (Recommended)
```bash
streamlit run app.py
```
Opens interactive web interface at `http://localhost:8501`

#### Option B: Command Line
```bash
python main.py
```

---

## Streamlit Web UI

### Features

✨ **User-Friendly Interface**
- File upload or paste log content
- Real-time progress tracking
- Beautiful tabbed interface

📊 **Results Dashboard**
- Key metrics (errors, warnings, solutions)
- Detailed error breakdown with stack traces
- Search results from external sources
- AI-generated solutions

💾 **Export Options**
- Download as Markdown
- Download as Text
- Download as JSON

### Running the Web UI

```bash
streamlit run app.py
```

Then open your browser to: `http://localhost:8501`

### UI Workflow

1. **📥 Input Tab**
   - Upload log file or paste content
   - Optional: Add GitHub repository URL
   - Click "Start Analysis"

2. **🔍 Analysis Tab**
   - See real-time progress
   - Track workflow status

3. **📊 Results Tab**
   - View all parsed errors
   - See external research results
   - Review AI-generated solutions
   - Read complete report

4. **💾 Download Tab**
   - Export report in multiple formats
   - Share analysis results

---

When you run the agent, you'll be prompted to:

1. **Enter log file path** - Path to your log file (or press Enter to use sample)
2. **Enter GitHub repository URL** - Optional, for code analysis
3. **Wait for analysis** - The agent will:
   - Parse logs for errors
   - Search external sources (Wikipedia, Stack Overflow, Reddit)
   - Analyze GitHub repository (if provided)
   - Generate AI-powered solutions
   - Build comprehensive report

4. **Find report** - Check `output/` directory for generated report

---

## Features

✅ **Log Parsing** - Extracts errors, warnings, and stack traces  
✅ **External Search** - Wikipedia and Stack Overflow integration  
✅ **Code Analysis** - GitHub repository analysis  
✅ **AI Solutions** - OpenAI-powered solution generation  
✅ **Report Generation** - Professional markdown reports  

---

## API Keys Required

1. **OpenAI API Key**: https://platform.openai.com/api-keys
2. **Tavily API Key**: https://tavily.com/
3. **GitHub Personal Token**: https://github.com/settings/tokens

---

## Architecture

### Agent State
- `logs`: Raw log content
- `github_repo`: Optional repository URL
- `parsed_errors`: Extracted errors from logs
- `search_results`: Results from external searches
- `code_analysis`: GitHub repo analysis results
- `solutions`: AI-generated solutions
- `final_report`: Markdown report

### Workflow Graph
```
parse_logs → search_solutions → analyze_code → generate_solutions → build_report
```

### Tools
- **LogParser**: Parse various log formats
- **ExternalTools**: Wikipedia, Stack Overflow, and GitHub integration

---

## Example Output

Generated reports include:
- Executive summary
- Critical issues listing
- Detailed error analysis
- Priority matrix
- Step-by-step solutions
- Prevention strategies

---

## Development

To add new features:

1. Add new nodes to `agent/nodes.py`
2. Update graph edges in `agent/graph.py`
3. Extend `ExternalTools` in `agent/tools.py`
4. Modify state in `agent/state.py` if needed

---

## Troubleshooting

- **Import errors**: Run `pip install -r requirements.txt`
- **API key errors**: Check `.env` file configuration
- **GitHub clone fails**: Check token permissions and repository accessibility
- **Memory issues**: Limit log file size or analyze smaller chunks
- **LangGraph state errors**: Ensure all nodes properly return updated state dictionary
- **Streamlit errors**: Clear cache with `streamlit cache clear` and restart

---

## License

MIT License - Feel free to modify and distribute
