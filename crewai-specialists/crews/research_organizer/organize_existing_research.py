#!/usr/bin/env python3
"""
Research Organization Crew - Organize Existing Research into NotebookLM

Takes your existing Gemini Deep Research and Perplexity research,
formats it, and organizes it into NotebookLM.
"""
import sys
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# Load configurations
config_dir = Path(__file__).parent.parent.parent / "config"

with open(config_dir / "models.yaml") as f:
    models_config = yaml.safe_load(f)

def get_llm(model_type="general"):
    """Get LLM instance for specified model type"""
    base_url = models_config["ollama"]["base_url"]
    model_name = models_config["models"][model_type]["name"]
    timeout = models_config["ollama"]["timeout"]
    return Ollama(model=model_name, base_url=base_url, timeout=timeout)

# Create specialized agents
research_collector = Agent(
    role="Research File Collector",
    goal="Scan and collect existing research files from specified locations",
    backstory="""You specialize in finding and cataloging research files.
    You can scan directories, identify research documents (PDFs, markdown, text),
    and extract metadata like topics, dates, and sources.""",
    llm=get_llm("general"),
    verbose=True,
    allow_delegation=False
)

document_formatter = Agent(
    role="NotebookLM Document Formatter",
    goal="Format existing research into NotebookLM-optimized documents",
    backstory="""You are an expert in NotebookLM's optimal document format.
    You take existing research and restructure it with proper headings,
    citations, metadata, and organization for NotebookLM import.""",
    llm=get_llm("general"),
    verbose=True,
    allow_delegation=False
)

notebooklm_uploader = Agent(
    role="NotebookLM Upload Coordinator",
    goal="Upload formatted documents to NotebookLM and organize the notebook",
    backstory="""You coordinate the upload of research to NotebookLM.
    You provide clear instructions for manual upload or automate via
    browser automation when possible. You ensure proper organization.""",
    llm=get_llm("reasoning"),
    verbose=True,
    allow_delegation=True
)

# Define tasks
task1_collect = Task(
    description="""
    Collect all existing research files from specified locations.
    
    **User Input**: Directories, file paths, or URLs where research is stored
    
    **Locations to Check**:
    - Local directories (Downloads, Documents, Research folders)
    - Gemini Deep Research exports (PDFs, text files)
    - Perplexity saved threads or screenshots
    - Obsidian vault notes
    - Google Drive sync folders
    
    **For Each File Found**:
    - Extract filename and path
    - Identify file type (PDF, MD, TXT, HTML)
    - Determine source (Gemini, Perplexity, manual notes)
    - Extract title/topic from filename or content
    - Read first 200 characters for summary
    - Note file size and modification date
    
    **Output Format**:
    ```json
    {
      "research_files": [
        {
          "path": "/Users/mikefinneran/Downloads/gemini-research-ai-healthcare.pdf",
          "filename": "gemini-research-ai-healthcare.pdf",
          "type": "pdf",
          "source": "Gemini Deep Research",
          "topic": "AI in Healthcare",
          "size_kb": 450,
          "modified": "2025-11-05",
          "preview": "Executive Summary: AI in healthcare..."
        },
        {
          "path": "/Users/mikefinneran/Documents/perplexity-quantum-computing.md",
          "filename": "perplexity-quantum-computing.md",
          "type": "markdown",
          "source": "Perplexity",
          "topic": "Quantum Computing",
          "size_kb": 25,
          "modified": "2025-11-07"
        }
      ],
      "total_files": 15,
      "sources": ["Gemini Deep Research", "Perplexity", "Manual Notes"]
    }
    ```
    """,
    expected_output="JSON catalog of all research files with metadata",
    agent=research_collector
)

task2_format = Task(
    description="""
    Format all collected research files into NotebookLM-ready markdown documents.
    
    **Context**: JSON catalog of research files from Task 1
    
    **Formatting Strategy**:
    
    1. **Group by Topic**: Merge related files into single documents
       - Combine Gemini + Perplexity on same topic
       - Keep distinct topics separate
       - Maximum 10,000 words per document
    
    2. **Markdown Structure**:
       ```markdown
       ---
       title: "Topic Name"
       sources: ["Gemini Deep Research", "Perplexity AI"]
       files_merged: 3
       created: "2025-11-08"
       topics: ["AI", "Healthcare"]
       ---
       
       # Topic Name
       
       ## Overview
       [Synthesized introduction from all sources]
       
       ## Key Findings
       
       ### From Gemini Deep Research
       [Content from gemini-research-ai-healthcare.pdf]
       - Finding 1
       - Finding 2
       
       ### From Perplexity AI
       [Content from perplexity-ai-healthcare.md]
       - Complementary insight 1
       - Update from [date]
       
       ## Detailed Analysis
       
       ### Subtopic 1
       [Merged content from all sources]
       
       ## Sources
       
       ### Original Files
       - `gemini-research-ai-healthcare.pdf` (Gemini, Nov 5)
       - `perplexity-ai-healthcare.md` (Perplexity, Nov 7)
       - `healthcare-notes.txt` (Manual notes, Nov 6)
       ```
    
    3. **Quality Standards**:
       - Clean, consistent headings (#, ##, ###)
       - Preserve all citations and links
       - Remove duplicate content
       - Maintain source attribution
       - Valid markdown syntax
    
    4. **File Naming**: `[topic-slug].md` (e.g., `ai-healthcare-2025.md`)
    
    **Output**:
    - Formatted markdown files saved to: `~/crewai-specialists/outputs/notebooklm-docs/`
    - Manifest JSON listing all created files
    
    **Output Format**:
    ```json
    {
      "formatted_documents": [
        {
          "filename": "ai-healthcare-2025.md",
          "path": "~/crewai-specialists/outputs/notebooklm-docs/ai-healthcare-2025.md",
          "topic": "AI in Healthcare 2025",
          "word_count": 7500,
          "sources_merged": 3,
          "original_files": ["gemini-research-ai-healthcare.pdf", "perplexity-ai-healthcare.md"]
        }
      ],
      "total_documents": 5,
      "total_word_count": 35000
    }
    ```
    """,
    expected_output="Formatted markdown documents and manifest JSON",
    agent=document_formatter
)

task3_upload = Task(
    description="""
    Coordinate upload of formatted documents to NotebookLM.
    
    **Context**: Formatted documents from Task 2
    
    **Upload Process**:
    
    1. **Prepare Upload Instructions**:
       - List all files to upload (with full paths)
       - Provide NotebookLM URL
       - Step-by-step upload guide
    
    2. **Manual Upload Steps**:
       ```
       1. Open https://notebooklm.google.com
       2. Click "New notebook" or open existing
       3. Name: "Research Library - [Date]"
       4. For each file:
          - Click "Sources" → "Upload"
          - Select: ~/crewai-specialists/outputs/notebooklm-docs/[filename].md
          - Add description: [topic name]
          - Wait for processing
       5. Verify all sources uploaded successfully
       ```
    
    3. **Post-Upload Configuration**:
       - Suggested notebook description
       - Recommended tags for each document
       - Sample prompts to ask NotebookLM:
         * "What are the key findings across all research?"
         * "Compare perspectives from different sources"
         * "What topics need more research?"
    
    4. **User Guide**:
       Create `NOTEBOOKLM_GUIDE.md` with:
       - How to navigate the research
       - Best prompts for different question types
       - How to export or share findings
    
    **Output Format**:
    ```json
    {
      "upload_method": "manual",
      "files_to_upload": [
        {
          "file": "~/crewai-specialists/outputs/notebooklm-docs/ai-healthcare-2025.md",
          "topic": "AI in Healthcare 2025",
          "suggested_description": "Combined research from Gemini and Perplexity on AI healthcare trends"
        }
      ],
      "notebook_name": "Research Library - Nov 2025",
      "manual_steps_file": "~/crewai-specialists/outputs/UPLOAD_INSTRUCTIONS.md",
      "user_guide_file": "~/crewai-specialists/outputs/NOTEBOOKLM_GUIDE.md",
      "suggested_prompts": [
        "What are the key findings about AI in healthcare?",
        "Summarize research on quantum computing",
        "What sources disagree and where?"
      ]
    }
    ```
    """,
    expected_output="Upload instructions, user guide, and suggested NotebookLM prompts",
    agent=notebooklm_uploader
)

# Create the crew
organize_crew = Crew(
    agents=[research_collector, document_formatter, notebooklm_uploader],
    tasks=[task1_collect, task2_format, task3_upload],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("📚 ORGANIZE EXISTING RESEARCH → NotebookLM")
    print("="*80)
    print("\nTeam:")
    print("  1. Research File Collector - Find existing research files")
    print("  2. Document Formatter - Format for NotebookLM")
    print("  3. Upload Coordinator - Upload to NotebookLM")
    print("\n" + "="*80)
    
    # Get research locations from user
    print("\nWhere is your existing research?")
    print("Examples:")
    print("  • ~/Downloads")
    print("  • ~/Documents/Research")
    print("  • ~/Documents/ObsidianVault/Projects/Research")
    print("")
    
    research_locations = input("Enter directory paths (comma-separated): ")
    
    print("\n" + "="*80)
    print("Starting organization process...\n")
    
    # Execute the crew
    inputs = {"research_locations": research_locations}
    result = organize_crew.kickoff(inputs=inputs)
    
    # Save output
    output_dir = Path(__file__).parent.parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "research_organization_summary.md"
    with open(output_file, 'w') as f:
        f.write(str(result))
    
    print("\n" + "="*80)
    print(f"✅ Organization complete!")
    print(f"📄 Summary: {output_file}")
    print(f"📁 Formatted docs: {output_dir}/notebooklm-docs/")
    print(f"📋 Upload instructions: {output_dir}/UPLOAD_INSTRUCTIONS.md")
    print("="*80 + "\n")
