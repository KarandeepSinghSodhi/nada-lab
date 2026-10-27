with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """  document.addEventListener('DOMContentLoaded', function () {
    initWorkspaceModes();
    initTutorialSystem();
    initTonicCalibration();
    initMusicianControls();"""

replacement = """  function initVideoDemoModal() {
    const watchBtn = document.getElementById('watch-demo-btn');
    const modal = document.getElementById('video-demo-modal');
    const closeBtn = document.getElementById('demo-close-btn');
    const backdrop = document.getElementById('demo-backdrop');
    const video = document.getElementById('demo-modal-video');
    const chapterBtns = document.querySelectorAll('.demo-ch-btn');

    if (!watchBtn || !modal || !video) return;

    function openModal() {
      modal.classList.remove('is-hidden');
      modal.setAttribute('aria-hidden', 'false');
      video.play().catch(function () {});
    }

    function closeModal() {
      modal.classList.add('is-hidden');
      modal.setAttribute('aria-hidden', 'true');
      video.pause();
    }

    watchBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.classList.contains('is-hidden')) {
        closeModal();
      }
    });

    chapterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const sec = parseFloat(btn.getAttribute('data-seek') || '0');
        video.currentTime = sec;
        video.play().catch(function () {});
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initWorkspaceModes();
    initTutorialSystem();
    initVideoDemoModal();
    initTonicCalibration();
    initMusicianControls();"""

# Normalize line endings for replacement
if target.replace('\r\n', '\n') in text.replace('\r\n', '\n'):
    # Detect line ending
    crlf = '\r\n' in text
    sep = '\r\n' if crlf else '\n'
    t = sep.join(target.splitlines())
    r = sep.join(replacement.splitlines())
    text = text.replace(t, r, 1)
    with open('d:/Music/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated app.js successfully')
else:
    print('Target not found in app.js')
