# scripts/clean_styles_lint.py
import re

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any stray JetBrains Mono in styles.css that is not in a code block
text = text.replace("font-family: 'JetBrains Mono', monospace;", "font-variant-numeric: tabular-nums;")
# Remove border on .tala-tuning-pill
text = re.sub(r'border:\s*1px\s*solid\s*rgba\(143,\s*166,\s*142,\s*0\.25\);', '', text)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned styles.css successfully.')
