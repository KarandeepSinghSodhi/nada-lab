with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_pipeline = False
for i, l in enumerate(lines):
    if '<section id="pipeline"' in l:
        in_pipeline = True
    elif in_pipeline and '<section ' in l:
        break
    if in_pipeline:
        if '<div id=' in l or '<nav' in l or 'class="universal-' in l or 'class="sadhana-' in l or 'class="ui-layout' in l or 'class="ui-canvas-pane' in l or 'class="ui-diagnostics-pane' in l:
            print(f'{i+1}: {l.strip()[:95]}')
