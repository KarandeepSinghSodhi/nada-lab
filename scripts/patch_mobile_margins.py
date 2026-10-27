# scripts/patch_mobile_margins.py

with open('styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update @media (max-width: 767px) to hide mobile nav extra buttons
target1 = '''.site-nav .nav-link {

    display: none;

  }'''

replacement1 = '''.site-nav .nav-link,
  .site-nav .nav-tutorial-btn,
  .site-nav .nav-demo-btn {

    display: none;

  }'''

# 2. Add overflow protection for mobile
target2 = '''@media (max-width: 767px) {'''

addition2 = '''@media (max-width: 767px) {

  html, body {
    overflow-x: hidden;
    max-width: 100vw;
  }

  .sadhana-guidance-bar,
  .sadhana-circadian-group,
  .inspector-workbench,
  .ui-canvas-grid,
  .ui-canvas-pane,
  .ui-live-tracker,
  .tracker-top-grid,
  .tracker-note-card,
  .tracker-gauge-card,
  .tracker-profile-card {
    max-width: 100%;
    min-width: 0;
    box-sizing: border-box;
  }'''

text_lf = text.replace('\r\n', '\n')
target1_lf = target1.replace('\r\n', '\n')
replacement1_lf = replacement1.replace('\r\n', '\n')
target2_lf = target2.replace('\r\n', '\n')
addition2_lf = addition2.replace('\r\n', '\n')

if target1_lf in text_lf and target2_lf in text_lf:
    new_text = text_lf.replace(target1_lf, replacement1_lf).replace(target2_lf, addition2_lf, 1).replace('\n', '\r\n')
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('SUCCESS: Patched styles.css for mobile centering & overflow!')
else:
    print('ERROR: Targets not found in styles.css')
