# Research Organization Crew

**Organize Your Existing Research → NotebookLM**

Takes your existing Gemini Deep Research and Perplexity research files, formats them properly, and helps you upload them to NotebookLM.

## What It Does

1. **Finds Your Research** - Scans directories you specify for research files
2. **Formats for NotebookLM** - Converts to clean markdown with proper structure
3. **Uploads to NotebookLM** - Provides clear upload instructions

## Team

- **Research File Collector** (Llama3 70B) - Finds and catalogs your research files
- **Document Formatter** (Llama3 70B) - Formats into NotebookLM-ready markdown
- **Upload Coordinator** (DeepSeek R1 70B) - Guides you through upload process

## Usage

```bash
cd ~/crewai-specialists/crews/research_organizer
python organize_existing_research.py
```

**You'll be prompted for:**
```
Enter directory paths: ~/Downloads, ~/Documents/Research
```

**The crew will:**
1. Scan those directories for research files (PDFs, markdown, text)
2. Group by topic and format as clean markdown
3. Save to `~/crewai-specialists/outputs/notebooklm-docs/`
4. Create upload instructions

## Supported File Types

- **Gemini Deep Research**: PDFs, exported text files
- **Perplexity**: Saved threads, screenshots, markdown exports
- **Manual Notes**: Text files, markdown, Word docs
- **Web Pages**: Saved HTML, browser exports

## Output

### Formatted Documents
`~/crewai-specialists/outputs/notebooklm-docs/`
- `ai-healthcare-2025.md`
- `quantum-computing-overview.md`
- `autonomous-vehicles-safety.md`

### Upload Instructions
`~/crewai-specialists/outputs/UPLOAD_INSTRUCTIONS.md`
- Step-by-step guide to upload to NotebookLM
- Suggested notebook name and descriptions
- Verification checklist

### User Guide
`~/crewai-specialists/outputs/NOTEBOOKLM_GUIDE.md`
- How to use NotebookLM with your research
- Best prompts to ask
- Navigation tips

## Example

```bash
$ python organize_existing_research.py

Where is your existing research?
Enter directory paths: ~/Downloads, ~/Documents/ObsidianVault/Research

Starting organization process...

✓ Found 12 research files
✓ Grouped into 5 topics
✓ Formatted 5 markdown documents
✓ Created upload instructions

Files ready at: ~/crewai-specialists/outputs/notebooklm-docs/
Upload guide: ~/crewai-specialists/outputs/UPLOAD_INSTRUCTIONS.md
```

Then follow the upload instructions to add to NotebookLM!

## Quick Start

1. **Collect your research** in one or more folders
2. **Run the crew**: `python organize_existing_research.py`
3. **Upload to NotebookLM** following provided instructions
4. **Start asking questions** in NotebookLM!

## Tips

- **Keep files organized**: Put similar topics in same folder
- **Name files clearly**: Better filenames = better topic grouping
- **Include sources**: The crew preserves source attribution
- **Review before upload**: Check formatted docs in `outputs/notebooklm-docs/`

## Files

- `organize_existing_research.py` - Main crew (use this one)
- `research_to_notebooklm_crew.py` - Advanced: Creates new research
- `research_tools.py` - API tools (if needed)
- `README.md` - This file
