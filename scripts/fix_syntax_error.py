with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    // C. VOICE, FLUTE & SITAR/STRING PROFILE ENGINE
    const swaraEl = document.getElementById('live-swara-val');
    const sargamEl = document.getElementById('live-sargam-script');
    const westernEl = document.getElementById('live-western-val');
    const freqEl = document.getElementById('live-freq-val');
    const saptakEl = document.getElementById('live-saptak-val');
    const centsBadge = document.getElementById('live-cents-badge');
    const gaugeNeedle = document.getElementById('live-gauge-needle');
    const shrutiRatioEl = document.getElementById('live-shruti-ratio');
    const tuningStatusEl = document.getElementById('live-tuning-status');
    const signalMeterEl = document.getElementById('live-signal-meter');"""

replacement = """    // C. VOICE, FLUTE & SITAR/STRING PROFILE ENGINE"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed duplicate declaration in app.js")
else:
    print("Target not found directly, checking normalized...")
