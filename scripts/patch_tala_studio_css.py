# scripts/patch_tala_studio_css.py

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''.ui-tala-btn.is-active {
  background-color: var(--accent);
  color: var(--accent-ink);
}'''

addition = '''.ui-tala-btn.is-active {
  background-color: var(--accent);
  color: var(--accent-ink);
}

.ui-tala-action-group {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.tala-tuning-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 500;
  color: var(--accent);
  background: rgba(143, 166, 142, 0.10);
  border: 1px solid rgba(143, 166, 142, 0.25);
  padding: 6px 12px;
  border-radius: 4px;
}'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
addition_lf = addition.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, addition_lf).replace('\n', '\r\n')
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('SUCCESS: Patched styles.css with tala-action-group and tala-tuning-pill!')
else:
    print('ERROR: Target string not found in styles.css')
