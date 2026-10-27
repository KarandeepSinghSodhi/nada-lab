with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = """        <button type="button" id="start-tutorial-btn" class="nav-tutorial-btn" title="Launch step-by-step interactive walkthrough" data-ui="tut-btn">
          <span class="tut-icon">GUIDE</span>
          <span class="tut-text">Guided Tour</span>
        </button>"""

replacement1 = target1 + """
        <button type="button" id="watch-demo-btn" class="nav-demo-btn" title="Watch official product demo &amp; marketing video" data-ui="demo-btn">
          <span class="demo-icon">▶</span>
          <span class="demo-text">Watch Demo</span>
        </button>"""

modal_markup = """  <!-- Official Video Demo & Marketing Showcase Modal -->
  <div id="video-demo-modal" class="demo-modal is-hidden" aria-hidden="true" data-ui="demo-modal">
    <div class="demo-backdrop" id="demo-backdrop"></div>
    <div class="demo-card" role="dialog" aria-modal="true" aria-labelledby="demo-modal-title">
      <div class="demo-header">
        <div>
          <span class="demo-modal-badge">42s MOTION GRAPHICS &amp; ACOUSTIC WALKTHROUGH</span>
          <h3 id="demo-modal-title" class="demo-title">Song Lab Product Demo &amp; R&amp;D Showcase</h3>
        </div>
        <button type="button" id="demo-close-btn" class="demo-close" aria-label="Close Demo">&times;</button>
      </div>

      <div class="demo-body">
        <div class="demo-video-wrapper">
          <video id="demo-modal-video" controls preload="metadata" poster="marketing_poster.png" playsinline class="demo-video-element">
            <source src="marketing_demo.webm" type="video/webm">
            Your browser does not support HTML5 WebM video.
          </video>
        </div>

        <div class="demo-chapters-row">
          <button type="button" class="demo-ch-btn" data-seek="0">0:00 12-TET Limits</button>
          <button type="button" class="demo-ch-btn" data-seek="7">0:07 22-Shruti Tracker</button>
          <button type="button" class="demo-ch-btn" data-seek="14">0:14 Rasa Radar</button>
          <button type="button" class="demo-ch-btn" data-seek="21">0:21 AI Guru &amp; Clock</button>
          <button type="button" class="demo-ch-btn" data-seek="28">0:28 NEURO-RASA R&amp;D</button>
          <button type="button" class="demo-ch-btn" data-seek="35">0:35 Launch</button>
        </div>
      </div>

      <div class="demo-actions">
        <a href="demo_showcase.html" target="_blank" class="demo-btn-secondary">Open Full Showcase Page ↗</a>
        <a href="marketing_demo.webm" download="Song_Lab_Demo.webm" class="demo-btn-primary">Download WebM Video</a>
      </div>
    </div>
  </div>
"""

if target1 in text:
    text = text.replace(target1, replacement1, 1)
    text = text.replace('  <script src="app.js"></script>', modal_markup + '  <script src="app.js"></script>', 1)
    with open('d:/Music/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated index.html successfully')
else:
    print('Target not found')
