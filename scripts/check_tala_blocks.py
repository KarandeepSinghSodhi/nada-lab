with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('rupak: {')
end_idx = text.find('};', idx)
print("app.js rupak block:")
print(repr(text[idx:end_idx+2]))

with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx_html = html.find('<select id="ui-tala-select"')
end_idx_html = html.find('</select>', idx_html)
print("index.html select block:")
print(repr(html[idx_html:end_idx_html+9]))
