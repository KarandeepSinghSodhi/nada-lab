with open('d:/Music/styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

cut_marker = "/* =========================================================\n   OFFICIAL VIDEO DEMO & MARKETING SHOWCASE MODAL"
if cut_marker in text:
    base = text[:text.index(cut_marker)]
elif "/* =========================================================\r\n   OFFICIAL VIDEO DEMO & MARKETING SHOWCASE MODAL" in text:
    base = text[:text.index("/* =========================================================\r\n   OFFICIAL VIDEO DEMO & MARKETING SHOWCASE MODAL")]
else:
    base = text

new_css = """/* =========================================================
   OFFICIAL VIDEO DEMO & MARKETING SHOWCASE MODAL
   ========================================================= */
.nav-demo-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: rgba(143, 166, 142, 0.16);
  border-radius: 4px;
  color: #a4bca3;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-demo-btn:hover {
  background: #8fa68e;
  color: #121212;
}

[data-ui="demo-modal"].demo-modal {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

[data-ui="demo-modal"].demo-modal.is-hidden {
  display: none;
}

[data-ui="demo-modal"] .demo-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(10, 10, 10, 0.92);
}

[data-ui="demo-modal"] .demo-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 920px;
  background: #141414;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

[data-ui="demo-modal"] .demo-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 18px 24px 14px;
  background: #1c1c1c;
}

[data-ui="demo-modal"] .demo-modal-badge {
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #d4a373;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

[data-ui="demo-modal"] .demo-title {
  font-family: 'Cabinet Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #f1f1ef;
  margin-top: 4px;
}

[data-ui="demo-modal"] .demo-close {
  background: transparent;
  border: none;
  color: #928f85;
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
  padding: 4px;
  transition: color 0.15s ease;
}

[data-ui="demo-modal"] .demo-close:hover {
  color: #f1f1ef;
}

[data-ui="demo-modal"] .demo-body {
  padding: 20px 24px;
}

[data-ui="demo-modal"] .demo-video-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

[data-ui="demo-modal"] .demo-video-element {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

[data-ui="demo-modal"] .demo-chapters-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

[data-ui="demo-modal"] .demo-ch-btn {
  background: #1c1c1c;
  border-radius: 4px;
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 12px;
  padding: 6px 12px;
  border: none;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="demo-modal"] .demo-ch-btn:hover {
  background: #8fa68e;
  color: #121212;
}

[data-ui="demo-modal"] .demo-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 14px 24px 18px;
  background: #181818;
}

[data-ui="demo-modal"] .demo-btn-secondary {
  color: #c8c5ba;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 4px;
  background: #242424;
  transition: background 0.15s ease, color 0.15s ease;
}

[data-ui="demo-modal"] .demo-btn-secondary:hover {
  background: #2e2e2e;
  color: #f1f1ef;
}

[data-ui="demo-modal"] .demo-btn-primary {
  color: #121212;
  font-family: 'Clash Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  background: #8fa68e;
  transition: background 0.15s ease;
}

[data-ui="demo-modal"] .demo-btn-primary:hover {
  background: #a4bca3;
}
"""

with open('d:/Music/styles.css', 'w', encoding='utf-8') as f:
    f.write(base.rstrip() + '\n\n' + new_css)
print('Updated styles.css successfully')
