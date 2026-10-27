with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<li class="poster-row reveal-item" data-cents="',
    '<li class="poster-row reveal-item" role="button" tabindex="0" data-cents="'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated index.html poster-row attributes")
