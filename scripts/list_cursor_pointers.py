import re

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'([.a-zA-Z0-9_\-\[\]=": ]+)\s*\{[^}]*cursor:\s*pointer', text)
selectors = []
for m in matches:
    sel = m.strip().split('\n')[-1].strip()
    if sel:
        selectors.append(sel)

for s in sorted(set(selectors)):
    print(s)
