with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"Kan Touch"\'', "'Kan Touch'")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned trailing quote.")
