with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """          chip.addEventListener('click', function () {
            scrubValue = Math.max(0, Math.min(1.0, n.start_time / duration));
            const scrubber = document.getElementById('phrase-scrubber');
            if (scrubber) scrubber.value = String(scrubber.max * scrubValue);
            renderPhraseInspector();
            if (isAudioAuditioning) {
              stopAuditionPlayback();
              startAuditionPlayback();
            }
          });"""

replacement = """          chip.addEventListener('click', function () {
            const relProgress = Math.max(0, Math.min(1.0, n.start_time / (duration || 6.0)));
            scrubValue = Math.round(relProgress * 100);
            const scrubber = document.getElementById('phrase-scrubber');
            if (scrubber) scrubber.value = String(scrubValue);
            renderPhraseInspector();
            notList.querySelectorAll('.notation-chip').forEach(function (c) { c.classList.remove('is-active'); });
            chip.classList.add('is-active');
            if (n.cents !== undefined && n.cents !== null) {
              playShrutiInterval(n.cents);
            }
          });"""

assert target in text, "Target not found in app.js!"
text = text.replace(target, replacement, 1)

with open('d:/Music/app.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("SUCCESS: Fixed notation chip click handler in app.js!")
