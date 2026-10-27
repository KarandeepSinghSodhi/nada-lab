# scripts/patch_andolan_var.py

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''  // Musician-Grade Real-Time Acoustic Oscilloscope & Timbre Engine
  let prevWaveTriggerOffset = 0;
  let rollingRmsHistory = [];'''

replacement = '''  // Musician-Grade Real-Time Acoustic Oscilloscope & Timbre Engine
  let prevWaveTriggerOffset = 0;
  let rollingRmsHistory = [];
  let currentAndolanSpeed = 0;'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace('\n', '\r\n')
    with open('app.js', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Declared currentAndolanSpeed in app.js!')
else:
    print('ERROR: Target not found')
