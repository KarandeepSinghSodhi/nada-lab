with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add tanpura-strings-strip inside sadhana-guidance-bar
old_circadian = """          <div class="sadhana-circadian-group">
            <span class="circadian-prahara-tag" id="ui-circadian-tag" title="Chronobiological time-of-day prahara and neuro-endocrine phase">Circadian: Prahara 4 · Bhimpalasi</span>
            <button type="button" class="circadian-sync-btn" id="btn-circadian-sync" title="1-click align raga, drone, and affective radar to current solar time">Sync Solar Hour</button>
          </div>"""

new_circadian = """          <div class="sadhana-circadian-group">
            <span class="circadian-prahara-tag" id="ui-circadian-tag" title="Chronobiological time-of-day prahara and neuro-endocrine phase">Circadian: Prahara 4 · Bhimpalasi</span>
            <button type="button" class="circadian-sync-btn" id="btn-circadian-sync" title="1-click align raga, drone, and affective radar to current solar time">Sync Solar Hour</button>
            <div class="tanpura-strings-strip" aria-label="Miraj Tanpura 4-String Pluck Sequence" data-ui="tanpura-pips">
              <span class="tanpura-string-pip" data-string-idx="0"><span class="pip-dot"></span> Pa</span>
              <span class="tanpura-string-pip" data-string-idx="1"><span class="pip-dot"></span> Sa'</span>
              <span class="tanpura-string-pip" data-string-idx="2"><span class="pip-dot"></span> Sa'</span>
              <span class="tanpura-string-pip" data-string-idx="3"><span class="pip-dot"></span> Sa</span>
            </div>
          </div>"""

if old_circadian in html:
    html = html.replace(old_circadian, new_circadian, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added tanpura-strings-strip to index.html")
else:
    print("old_circadian not found")

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

pip_styles = """
/* Tanpura 4-String Pluck Indicator Pips */
.tanpura-strings-strip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-left: 8px;
}

.tanpura-string-pip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 500;
  color: var(--muted);
  padding: 3px 8px;
  background-color: #1c1c1c;
  transition: background-color 150ms var(--ease-out), color 150ms var(--ease-out);
}

.tanpura-string-pip .pip-dot {
  display: inline-block;
  width: 5px;
  height: 5px;
  background-color: #555555;
  border-radius: 50%;
  transition: background-color 150ms var(--ease-out), transform 150ms var(--ease-out);
}

.tanpura-string-pip.is-plucked {
  background-color: #3b4e3b;
  color: #c9e4cb;
}

.tanpura-string-pip.is-plucked .pip-dot {
  background-color: #a4bca3;
  transform: scale(1.3);
}
"""

if '.tanpura-strings-strip' not in css:
    css = css + "\n" + pip_styles
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added pip styles to styles.css")
