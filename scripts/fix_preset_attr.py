with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_target = """        const hz = parseFloat(btn.getAttribute('data-hz') || '146.83');
        const note = btn.getAttribute('data-note') || '';"""

new_target = """        const hz = parseFloat(btn.getAttribute('data-preset') || btn.getAttribute('data-hz') || '146.83');
        const note = btn.getAttribute('data-note') || btn.textContent.trim();"""

if old_target in text:
    text = text.replace(old_target, new_target, 1)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed data-preset in app.js")
else:
    print("old_target not found")
