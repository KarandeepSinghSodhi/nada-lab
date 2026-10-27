# Rebuild index.html with the 5 Clean Studio Tabs
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Identify key segments:
# S1: from start of file up to before <div class="sadhana-guidance-bar"
idx_sadhana = text.find('        <!-- Sādhanā Quick Status Bar (Surfaced in Guided Practice Mode) -->')
if idx_sadhana == -1:
    idx_sadhana = text.find('<div class="sadhana-guidance-bar"')

# S2: Universal track uploader
idx_uploader_start = text.find('        <!-- UNIVERSAL 1-CLICK AUDIO TRACK UPLOADER -->')
if idx_uploader_start == -1:
    idx_uploader_start = text.find('<div class="track-uploader-banner"')

# S3: Instant dossier card
idx_dossier_start = text.find('        <!-- INSTANT TRACK INTELLIGENCE & COMPLETE REPORT CARD -->')
if idx_dossier_start == -1:
    idx_dossier_start = text.find('<div class="instant-dossier-card')

# S4: Inspector workbench
idx_workbench = text.find('        <!-- THE LIVE THING: Interactive Phrase & Deficit Inspector -->')
if idx_workbench == -1:
    idx_workbench = text.find('<div class="inspector-workbench"')

# S5: Shrutis section
idx_shrutis = text.find('    <!-- CHAPTER 4: LIST (Canonical Rational Shruti Intervals) -->')
if idx_shrutis == -1:
    idx_shrutis = text.find('<section id="shrutis"')

print("Boundaries found:")
print("idx_sadhana:", idx_sadhana)
print("idx_uploader_start:", idx_uploader_start)
print("idx_dossier_start:", idx_dossier_start)
print("idx_workbench:", idx_workbench)
print("idx_shrutis:", idx_shrutis)
