# -*- coding: utf-8 -*-
"""
Script to fix reveal-item blank-gap in styles.css and index.html
"""

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('class="inspector-workbench reveal-item"', 'class="inspector-workbench"')
html = html.replace('class="accordion-strip reveal-item"', 'class="accordion-strip"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html updated (reveal-item removed from workbench and accordion).")

# 2. Update styles.css
with open("styles.css", "r", encoding="utf-8") as f:
    css = f.read()

old_reveal_css = """.reveal-item {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 560ms var(--ease-out), transform 560ms var(--ease-out);
}

.reveal-item.is-visible {
  opacity: 1;
  transform: translateY(0);
}"""

new_reveal_css = """.reveal-item {
  opacity: 1;
  transform: none;
  transition: opacity 560ms var(--ease-out), transform 560ms var(--ease-out);
}

.reveal-item.is-visible {
  opacity: 1;
  transform: none;
}"""

if old_reveal_css in css:
    css = css.replace(old_reveal_css, new_reveal_css, 1)
    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("styles.css updated with safe reveal-item rules.")
else:
    print("Warning: old_reveal_css not found in styles.css!")
