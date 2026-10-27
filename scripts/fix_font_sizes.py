with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('font-size: 10px;', 'font-size: 11px;')

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(text)
print("Replaced all font-size: 10px with 11px in styles.css")
