#!/usr/bin/env python3
"""
Research Organization Crew - Gemini Deep Research + Perplexity → NotebookLM

Collects research from Gemini Deep Research and Perplexity, then organizes it into NotebookLM
"""
import sys
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# Add parent directory to path for vaultwarden_client
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from vaultwarden_client import get_api_key

# Load configurations
config_dir = Path(__file__).parent.parent.parent / "config"

with open(config_dir / "models.yaml") as f:
    models_config = yaml.safe_load(f)

with open(config_dir / "agents.yaml") as f:
    agents_config = yaml.safe_load(f)

def get_llm(model_type="general"):
    """Get LLM instance for specified model type"""
    base_url = models_config["ollama"]["base_url"]
    model_name = models_config["models"][model_type]["name"]
    timeout = models_config["ollama"]["timeout"]
    return Ollama(model=model_name, base_url=base_url, timeout=timeout)

# Create specialized agents
gemini_researcher = Agent(
    role="Gemini Deep Research Collector",
    goal="Extract and organize research from Gemini Deep Research reports",
    backstory="""You are an expert at working with Gemini Deep Research, Google's 
    comprehensive AI research tool. You can parse deep research reports, extract
    key findings, citations, and organize insights into structured formats.""",
    llm=get_llm("reasoning"),  # DeepSeek R1 for analysis
    verbose=True,
    allow_delegation=False
)

perplexity_researcher = Agent(
    role="Perplexity Research Analyst",
    goal="Gather and synthesize research from Perplexity searches",
    backstory="""You specialize in using Perplexity AI to conduct deep research.
    You know how to extract key insights, citations, and organize findings
    into coherent research summaries.""",
    llm=get_llm("reasoning"),  # DeepSeek R1 for analysis
    verbose=True,
    allow_delegation=False
)

document_formatter = Agent(
    role="NotebookLM Document Formatter",
    goal="Format research content optimally for NotebookLM import",
    backstory="""You are an expert in NotebookLM's document structure and formatting.
    You know how to organize research into clean markdown documents
    that NotebookLM can parse effectively, with proper headings, citations,
    and hierarchical structure.""",
    llm=get_llm("general"),
    verbose=True,
    allow_delegation=False
)

notebooklm_organizer = Agent(
    role="NotebookLM Project Organizer",
    goal="Create and organize NotebookLM projects with imported research",
    backstory="""You manage NotebookLM projects, creating organized notebooks
    with proper source attribution, topic grouping, and metadata tagging.
    You ensure research is accessible and well-structured for AI analysis.""",
    llm=get_llm("reasoning"),
    verbose=True,
    allow_delegation=True
)

# Define tasks
task1_collect_gemini = Task(
    description="""
    Collect and parse research from Gemini Deep Research reports.
    
    **Input**: User provides Gemini Deep Research report URLs, exported files, or topic names
    
    **Collection Methods**:
    1. **Exported Reports**: Parse PDF or text exports from Gemini Deep Research
    2. **Web Scraping**: Extract content from Gemini Deep Research web interface
    3. **API Access**: Use Gemini API if available for programmatic access
    
    **Extract from Each Report**:
    - Research topic/question
    - Executive summary
    - Key findings (numbered list)
    - Detailed analysis sections
    - Source citations (URLs, papers, articles)
    - Related topics suggested by Gemini
    - Confidence scores/caveats
    - Timestamp of research
    
    **Required Output**:
    JSON structure:
    ```json
    {
      "source": "Gemini Deep Research",
      "reports": [
        {
          "topic": "AI in Healthcare 2025",
          "url": "https://gemini.google.com/...",
          "timestamp": "ISO date",
          "summary": "Executive summary...",
          "key_findings": [
            "Finding 1...",
            "Finding 2..."
          ],
          "sections": [
            {
              "heading": "Current State",
              "content": "...",
              "citations": [{"url": "...", "title": "..."}]
            }
          ],
          "sources_count": 45,
          "topics": ["AI", "Healthcare", "2025 Trends"]
        }
      ]
    }
    ```
    
    **Tools to Use**:
    - Gemini API (if available)
    - PDF parser for exported reports
    - Web scraper for Gemini interface
    - Natural language processing for structure extraction
    """,
    expected_output="JSON list of Gemini Deep Research reports with complete content and citations",
    agent=gemini_researcher
)

task2_collect_perplexity = Task(
    description="""
    Gather research from Perplexity AI searches and complement Gemini findings.
    
    **Context**: You'll receive Gemini Deep Research topics to understand research focus.
    
    **Collection Strategy**:
    1. **Identify Gaps**: Find topics Gemini covered that need more depth
    2. **Recent Updates**: Search for information newer than Gemini's research
    3. **Alternative Perspectives**: Get different angles on same topics
    
    **Collection Methods**:
    - Perplexity API searches for each major topic
    - Extract saved Perplexity threads from browser/account
    - Run targeted follow-up queries based on Gemini findings
    
    **Required Output**:
    For each search:
    - Query asked
    - Perplexity's answer (full text)
    - Source citations with URLs
    - Follow-up questions suggested
    - Relationship to Gemini research (complementary/contradictory/confirmatory)
    
    **Output Format**:
    ```json
    {
      "source": "Perplexity",
      "searches": [
        {
          "query": "Latest developments in AI healthcare 2025",
          "gemini_relation": "Updates Gemini finding #3",
          "answer": "Full Perplexity response...",
          "citations": [
            {"url": "...", "title": "...", "date": "2025-11-01"}
          ],
          "timestamp": "ISO date",
          "topics": ["AI", "Healthcare"]
        }
      ],
      "coverage_analysis": {
        "new_topics": ["Topic X", "Topic Y"],
        "confirmed_findings": ["Gemini finding #1", "#4"],
        "contradictions": []
      }
    }
    ```
    """,
    expected_output="JSON list of Perplexity searches with analysis of how they complement Gemini research",
    agent=perplexity_researcher
)

task3_format_for_notebooklm = Task(
    description="""
    Format all collected research into NotebookLM-optimized markdown documents.
    
    **Context**: 
    - Gemini Deep Research reports (JSON from Task 1)
    - Perplexity research (JSON from Task 2)
    
    **Document Strategy**:
    Create one comprehensive markdown document per major research topic that merges
    insights from both Gemini and Perplexity.
    
    **Document Structure**:
    ```markdown
    ---
    title: "Research Topic Name"
    sources: ["Gemini Deep Research", "Perplexity AI"]
    gemini_reports: 2
    perplexity_searches: 8
    created: "2025-11-08"
    topics: ["topic1", "topic2"]
    ---
    
    # Research Topic Name
    
    ## Executive Summary
    
    [Synthesized summary from both Gemini and Perplexity]
    
    ## Key Findings
    
    ### From Gemini Deep Research
    
    1. **Finding Name**
       - [Details from Gemini report]
       - Sources: [Citation 1], [Citation 2]
    
    ### Confirmed by Perplexity
    
    - Additional evidence from Perplexity search on [date]
    - Source: [Perplexity citation]
    
    ### From Perplexity Research
    
    1. **New Finding**
       - [Details from Perplexity]
       - Updates/extends Gemini research
       - Source: [URL with title]
    
    ## Detailed Analysis
    
    ### Subtopic 1
    
    #### Gemini Perspective
    [Content from Gemini report section]
    
    #### Perplexity Insights  
    [Complementary information from Perplexity]
    
    ### Subtopic 2
    ...
    
    ## Source Index
    
    ### Gemini Deep Research Reports
    - [Report Title](gemini-url) - Researched: [Date]
    
    ### Perplexity Searches
    - [Query](perplexity-url) - Searched: [Date]
    
    ### Primary Sources (Cited by Both)
    - [Source Title](URL) - Publication: [Date]
    ```
    
    **Formatting Rules**:
    1. Maximum 10,000 words per document
    2. Clear attribution for every claim (Gemini vs Perplexity)
    3. Merge overlapping content, note differences
    4. Keep all URLs as working links
    5. Use blockquotes for direct quotes
    6. Include metadata frontmatter
    
    **Output**:
    ```json
    {
      "documents": [
        {
          "filename": "ai-healthcare-2025-research.md",
          "content": "full markdown...",
          "word_count": 7500,
          "gemini_sources": 2,
          "perplexity_sources": 8,
          "primary_citations": 45
        }
      ]
    }
    ```
    """,
    expected_output="Array of NotebookLM-ready markdown documents merging Gemini and Perplexity research",
    agent=document_formatter
)

task4_organize_notebooklm = Task(
    description="""
    Upload formatted research to NotebookLM and create an organized research library.
    
    **Context**: Formatted markdown documents from Task 3
    
    **NotebookLM Setup**:
    
    1. **Create Notebook**:
       - Name: "Research Library - [Topic] - [Date]"
       - Description: "Combined insights from Gemini Deep Research and Perplexity AI"
    
    2. **Upload Each Document**:
       - Navigate to https://notebooklm.google.com
       - Create new notebook or select existing
       - Click "Sources" → "Upload"
       - Upload each markdown file
       - Add source description noting it's a synthesis
    
    3. **Organize Sources**:
       - Tag each document by topic
       - Create notebook guide/summary
       - Set up suggested prompts for users
    
    4. **Leverage NotebookLM AI**:
       - Generate cross-source insights
       - Create FAQ from research
       - Identify knowledge gaps
       - Suggest follow-up research questions
    
    5. **Create User Guide**:
       - How to navigate the research
       - Key prompts to ask NotebookLM
       - Source attribution guide
    
    **Implementation**:
    
    Since NotebookLM doesn't have a public API yet, provide:
    
    1. **Automated Upload Script** (using Puppeteer/browser automation):
       ```python
       # Python script to automate NotebookLM upload
       # Uses Puppeteer via Python subprocess
       ```
    
    2. **Manual Instructions** (if automation fails):
       - Step-by-step upload guide
       - Screenshots/terminal output showing what to do
    
    **Output Format**:
    ```json
    {
      "notebook_url": "https://notebooklm.google.com/notebook/abc123",
      "notebook_name": "AI Healthcare Research - Nov 2025",
      "documents_uploaded": 5,
      "upload_method": "manual|automated",
      "suggested_prompts": [
        "What are the key findings about AI in healthcare?",
        "Compare Gemini and Perplexity perspectives on...",
        "What sources were cited most frequently?"
      ],
      "manual_steps": [
        "1. Go to https://notebooklm.google.com",
        "2. Click 'New notebook'",
        "3. Upload files from: ~/outputs/notebooklm-docs/"
      ]
    }
    ```
    
    **Success Criteria**:
    - All documents successfully uploaded to NotebookLM
    - NotebookLM can answer questions using the research
    - Source attribution is maintained
    - User can easily navigate topics
    """,
    expected_output="NotebookLM project URL with uploaded research and usage guide",
    agent=notebooklm_organizer
)

# Create the crew
research_organizer_crew = Crew(
    agents=[gemini_researcher, perplexity_researcher, document_formatter, notebooklm_organizer],
    tasks=[task1_collect_gemini, task2_collect_perplexity, task3_format_for_notebooklm, task4_organize_notebooklm],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("📚 RESEARCH ORGANIZATION CREW")
    print("Gemini Deep Research + Perplexity → NotebookLM")
    print("="*80)
    print("\nTeam:")
    print("  1. Gemini Deep Research Collector (DeepSeek R1 70B)")
    print("  2. Perplexity Research Analyst (DeepSeek R1 70B)")
    print("  3. NotebookLM Document Formatter (Llama3 70B)")
    print("  4. NotebookLM Project Organizer (DeepSeek R1 70B)")
    print("\n" + "="*80)
    
    # Get user input for research sources
    print("\nProvide your research sources:")
    print("  • Gemini Deep Research URLs or exported files")
    print("  • Perplexity thread URLs (optional)")
    print("  • Or just provide topics to research")
    print("")
    
    user_input = input("Enter source URLs, file paths, or topics (comma-separated): ")
    
    print("\n" + "="*80)
    print("Starting research organization process...\n")
    
    # Execute the crew with user input
    inputs = {"research_sources": user_input}
    result = research_organizer_crew.kickoff(inputs=inputs)
    
    # Save output
    output_dir = Path(__file__).parent.parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "notebooklm_research_organization.md"
    with open(output_file, 'w') as f:
        f.write(str(result))
    
    print("\n" + "="*80)
    print(f"✅ Research organization complete!")
    print(f"📄 Saved to: {output_file}")
    print("="*80 + "\n")
