# -*- coding: utf-8 -*-
"""
Script to add Circadian Bio-Clock into index.html
"""

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_bar = """        <!-- Sādhanā Quick Status Bar (Surfaced in Guided Practice Mode) -->
        <div class="sadhana-guidance-bar" id="sadhana-guidance-bar" data-ui="sadhana-bar">
          <div class="sadhana-step-pill">
            <span class="sadhana-step-num">PRACTICE FOCUS</span>
            <span class="sadhana-step-title" id="sadhana-focus-text">Raga Yaman · Meend Glide (Re to Ga)</span>
          </div>
          <p class="sadhana-instruction-text" id="sadhana-quick-tip">
            Listen to the phrase, then start your mic and sing along with the tanpura drone. Watch your pitch line glide into Gandhar (5/4).
          </p>
        </div>"""

new_bar = """        <!-- Sādhanā Quick Status Bar (Surfaced in Guided Practice Mode) -->
        <div class="sadhana-guidance-bar" id="sadhana-guidance-bar" data-ui="sadhana-bar">
          <div class="sadhana-step-pill">
            <span class="sadhana-step-num">PRACTICE FOCUS</span>
            <span class="sadhana-step-title" id="sadhana-focus-text">Raga Yaman · Meend Glide (Re to Ga)</span>
          </div>
          <p class="sadhana-instruction-text" id="sadhana-quick-tip">
            Listen to the phrase, then start your mic and sing along with the tanpura drone. Watch your pitch line glide into Gandhar (5/4).
          </p>
          <div class="sadhana-circadian-group">
            <span class="circadian-prahara-tag" id="ui-circadian-tag" title="Chronobiological time-of-day prahara and neuro-endocrine phase">Circadian: Prahara 4 · Bhimpalasi</span>
            <button type="button" class="circadian-sync-btn" id="btn-circadian-sync" title="1-click align raga, drone, and affective radar to current solar time">Sync Solar Hour</button>
          </div>
        </div>"""

if old_bar in content:
    content = content.replace(old_bar, new_bar, 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html updated with Circadian Samay Chakra controls!")
else:
    print("Error: old_bar not found in index.html!")
