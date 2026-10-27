with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Verify markers
markers = [
    '<div class="sadhana-guidance-bar"',
    '<div class="track-uploader-banner"',
    '<div class="instant-dossier-card',
    '<div class="ui-controls-bar">',
    '<div class="ui-canvas-grid">',
    '<div id="tala-matra-grid"',
    '<div class="ui-diagnostic-pane">',
    '<div class="ui-rasa-panel"',
    '<div id="analyst-drawer"'
]

for m in markers:
    print(m, 'found:', m in html)
