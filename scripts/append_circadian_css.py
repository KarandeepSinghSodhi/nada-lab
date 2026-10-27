# -*- coding: utf-8 -*-
"""
Script to append Circadian Bio-Clock CSS into styles.css
"""

circadian_css = """
/* =========================================================
   CIRCADIAN SAMAY CHAKRA BIO-CLOCK & CHRONOBIOLOGY
   ========================================================= */
[data-ui="sadhana-bar"] .sadhana-circadian-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}

@media (max-width: 900px) {
  [data-ui="sadhana-bar"] .sadhana-circadian-group {
    width: 100%;
    justify-content: space-between;
    margin-left: 0;
  }
}

[data-ui="sadhana-bar"] .circadian-prahara-tag {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #a4bca3;
  background: rgba(143, 166, 142, 0.12);
  border: 1px solid rgba(143, 166, 142, 0.25);
  padding: 3px 8px;
  border-radius: 3px;
  white-space: nowrap;
}

[data-ui="sadhana-bar"] .circadian-sync-btn {
  background: #242424;
  border: 1px solid rgba(241, 241, 239, 0.12);
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 3px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="sadhana-bar"] .circadian-sync-btn:hover {
  background: #8fa68e;
  color: #121212;
}
"""

with open("styles.css", "a", encoding="utf-8") as f:
    f.write(circadian_css)

print("styles.css updated successfully with Circadian Bio-Clock styles!")
