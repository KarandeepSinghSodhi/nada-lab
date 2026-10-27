# Script to generate cleanly refactored index.html with the 5 Musician Studio Tabs
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Segment extraction
# Everything before pipeline-header-grid
pipe_start = text.find('<section id="pipeline" class="chapter pipeline-chapter">')
header_end = text.find('        </div>\n\n        <!-- 5-Panel Horizontal Accordion')
if header_end == -1:
    header_end = text.find('        <!-- 5-Panel Horizontal Accordion')

# Accordion strip
acc_start = text.find('        <!-- 5-Panel Horizontal Accordion')
acc_end = text.find('        </div>\n\n        <!-- Sādhanā Quick Status Bar')
if acc_end == -1:
    acc_end = text.find('        <!-- Sādhanā Quick Status Bar')

# Sādhana bar
sadhana_bar_start = text.find('        <!-- Sādhanā Quick Status Bar')
sadhana_bar_end = text.find('        <!-- UNIVERSAL 1-CLICK AUDIO TRACK UPLOADER -->')

# Uploader
uploader_start = text.find('        <!-- UNIVERSAL 1-CLICK AUDIO TRACK UPLOADER -->')
uploader_end = text.find('        <!-- INSTANT TRACK INTELLIGENCE & COMPLETE REPORT CARD -->')

# Dossier
dossier_start = text.find('        <!-- INSTANT TRACK INTELLIGENCE & COMPLETE REPORT CARD -->')
dossier_end = text.find('        <!-- THE LIVE THING: Interactive Phrase & Deficit Inspector -->')

# Workbench
workbench_start = text.find('        <!-- THE LIVE THING: Interactive Phrase & Deficit Inspector -->')
pipeline_close = text.find('      </div>\n    </section>\n\n    <!-- CHAPTER 4: LIST')
if pipeline_close == -1:
    pipeline_close = text.find('    <!-- CHAPTER 4: LIST')

print("All segments located successfully!")
