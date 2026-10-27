from pathlib import Path

p = Path("app.js")
text = p.read_text(encoding="utf-8")
old_line = "'<span class=\"antar-tr-desc\">' + tr.description + kanTag + '</span>' +"
new_line = "'<span class=\"antar-tr-desc\">' + (tr.description || (tr.curvature_name + ' connecting ' + tr.interval)) + kanTag + '</span>' +"

assert old_line in text, "old_line not found"
text = text.replace(old_line, new_line, 1)
p.write_bytes(text.encode("utf-8"))
print("SUCCESS: Updated description fallback in app.js")
