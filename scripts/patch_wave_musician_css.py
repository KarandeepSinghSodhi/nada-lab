# scripts/patch_wave_musician_css.py

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''#acoustic-wave-canvas {
  width: 100%;
  height: 74px;
  display: block;
  background: #0c0c0c;
  border-radius: 2px;
}'''

addition = '''#acoustic-wave-canvas {
  width: 100%;
  height: 74px;
  display: block;
  background: #0c0c0c;
  border-radius: 2px;
}

[data-ui="wave-container"] .tracker-wave-musician-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 4px;
}

[data-ui="wave-container"] .wave-musician-pill {
  font-size: 11px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
  letter-spacing: 0.02em;
}

[data-ui="wave-container"] .wave-musician-pill.is-highlight {
  color: var(--accent);
}'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
addition_lf = addition.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, addition_lf).replace('\n', '\r\n')
    with open('styles.css', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched styles.css with wave-musician-strip!')
else:
    print('ERROR: Target not found in styles.css')
