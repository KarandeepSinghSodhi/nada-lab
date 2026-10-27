with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    const u = Math.max(0, Math.min(1, scrubValue / 100));
    const activeCurveFn = (isGuruPlaying && phrase.guruCurveFn) ? phrase.guruCurveFn : phrase.curveFn;
    const cNow = activeCurveFn(u);
    const cNext = activeCurveFn(Math.min(1, u + 0.01));
    const effectiveSa = userCustomSaHz || phrase.saHz || 146.83;
    const estHz = effectiveSa * Math.pow(2, cNow / 1200);
    updateLiveNoteTracker(estHz, cNow, effectiveSa, 0.08);
    computeAffectiveCoordinates(cNow, velNow, 0.08, estHz);
    renderRasaRadarCanvas();
    const velNow = (cNext - cNow) / 0.025;
    const tSec = (u * 2.5).toFixed(2);"""

replacement = """    const u = Math.max(0, Math.min(1, scrubValue / 100));
    const activeCurveFn = (isGuruPlaying && phrase.guruCurveFn) ? phrase.guruCurveFn : phrase.curveFn;
    const cNow = activeCurveFn(u);
    const cNext = activeCurveFn(Math.min(1, u + 0.01));
    const velNow = (cNext - cNow) / 0.025;
    const tSec = (u * 2.5).toFixed(2);
    const effectiveSa = userCustomSaHz || phrase.saHz || 146.83;
    const estHz = effectiveSa * Math.pow(2, cNow / 1200);
    updateLiveNoteTracker(estHz, cNow, effectiveSa, 0.08);
    computeAffectiveCoordinates(cNow, velNow, 0.08, estHz);
    renderRasaRadarCanvas();"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed velNow order in app.js")
else:
    print("target not found")
