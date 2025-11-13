#!/usr/bin/env python3
"""
WalterSignal Logo Extraction Crew

Extract raccoon mascot from logo-source.png and create all necessary variations.
Source: ~/Documents/ObsidianVault/Projects/WalterSignal/assets/logo-source.png
"""

import sys
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

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
    return LLM(model=f'ollama/{model_name}', base_url=base_url)

# Specialists
visual_analyst = Agent(
    role=agents_config["visual_content_analyst"]["role"],
    goal="Analyze logo-source.png and identify exact crop boundaries for raccoon mascot",
    backstory=agents_config["visual_content_analyst"]["backstory"],
    llm=get_llm("vision"),  # Vision 90B
    verbose=True
)

graphic_designer = Agent(
    role=agents_config["graphic_brand_designer"]["role"],
    goal="Extract raccoon mascot and create all logo variations needed for WalterSignal",
    backstory=agents_config["graphic_brand_designer"]["backstory"],
    llm=get_llm("general"),  # Llama3 70B
    verbose=True
)

# Tasks
task1_analyze = Task(
    description="""
    Analyze logo-source.png to determine exact extraction requirements.
    
    **Source File**: ~/Documents/ObsidianVault/Projects/WalterSignal/assets/logo-source.png
    
    **Analysis Required**:
    1. **Mascot Boundaries**
       - Exact pixel coordinates of raccoon mascot (without text)
       - Crop box: top, left, bottom, right
       - Include WiFi symbol above head
       - Exclude "FRAMNE SIGNAL" text below
       - Exclude color bar at bottom
    
    2. **Color Extraction**
       - All purple shades used (hex codes)
       - All cyan/turquoise shades (hex codes)
       - All blue shades (hex codes)
       - Background color (currently dark navy)
    
    3. **Element Identification**
       - WiFi symbol (3 curved lines)
       - Raccoon ears (purple geometric)
       - Raccoon mask (cyan/blue geometric)
       - Raccoon face (white/black geometric)
       - Any gradients or effects
    
    **Output Format**:
    Precise specifications:
    - Crop coordinates
    - Color palette with hex codes
    - Element breakdown
    - Recommended export sizes
    """,
    expected_output="Detailed analysis with crop coordinates and color specifications",
    agent=visual_analyst
)

task2_extract = Task(
    description="""
    Create extraction plan and file specifications for all logo variations.
    
    **Context**: You will receive exact crop coordinates and color specs.
    
    **Required Deliverables**:
    
    1. **Primary Mascot (Transparent Background)**
       - Crop raccoon + WiFi symbol from logo-source.png
       - Remove dark navy background (make transparent)
       - Export sizes: 512x512, 256x256, 128x128, 64x64, 32x32, 16x16
       - Format: PNG with alpha channel
       - Naming: waltersignal-mascot-[size].png
    
    2. **Logo Variations**
       - **Full Color**: Original colors on transparent
       - **White**: All elements converted to white
       - **Black**: All elements converted to black  
       - **Purple Mono**: All purple (#8B5CF6)
       - **Cyan Mono**: All cyan (#22D3EE)
       - Export each in multiple sizes
    
    3. **Special Formats**
       - **Favicon**: 16x16, 32x32, 48x48 ICO file
       - **Apple Touch Icon**: 180x180 PNG
       - **SVG Version**: Vector format (if possible to trace)
       - **Social Media**: 512x512 for OpenGraph
    
    4. **Implementation Instructions**
       - Python script using PIL/Pillow for extraction
       - ImageMagick commands for batch processing
       - Figma/Photoshop manual steps (if needed)
       - Quality checks for each variation
    
    **Tools to Use**:
    - Python PIL/Pillow for programmatic extraction
    - ImageMagick for batch conversions
    - Optionally: Figma API or Photoshop scripts
    
    **Quality Standards**:
    - No background artifacts
    - Clean edges (anti-aliased)
    - Consistent sizing across variations
    - Optimized file sizes (PNG compression)
    
    **Output Format**:
    Complete extraction playbook with:
    - Step-by-step extraction process
    - Code snippets for automation
    - File naming convention
    - Directory structure for output files
    - Verification checklist
    """,
    expected_output="Complete logo extraction playbook with code and specifications",
    agent=graphic_designer
)

# Create crew
logo_crew = Crew(
    agents=[visual_analyst, graphic_designer],
    tasks=[task1_analyze, task2_extract],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎨 WALTERSIGNAL LOGO EXTRACTION CREW")
    print("="*80)
    print("\nSource: logo-source.png")
    print("Goal: Extract raccoon mascot + create all variations")
    print("\nTeam:")
    print("  1. Visual Content Analyst (Vision 90B) - Analyze & identify crop area")
    print("  2. Graphic Brand Designer (Llama3 70B) - Create extraction plan")
    print("\n" + "="*80 + "\n")
    
    # Execute
    result = logo_crew.kickoff()
    
    # Save output
    output_dir = Path.home() / "Documents/ObsidianVault/Projects/WalterSignal/assets"
    output_file = output_dir / "LOGO_EXTRACTION_PLAN.md"
    
    with open(output_file, 'w') as f:
        f.write(str(result))
    
    print("\n" + "="*80)
    print(f"✅ Logo extraction plan complete!")
    print(f"📄 Saved to: {output_file}")
    print("\nNext: Run the extraction scripts to create all logo variations")
    print("="*80 + "\n")
