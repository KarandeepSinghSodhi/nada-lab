# scripts/collapse_blank_lines.py
import re

for filename in ['styles.css', 'app.js', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # Collapse 3 or more newlines to 2 newlines (\n\n)
    collapsed = re.sub(r'\n{3,}', '\n\n', content)
    with open(filename, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(collapsed)
    print(f'Cleaned {filename}: now {len(collapsed.splitlines())} lines')
