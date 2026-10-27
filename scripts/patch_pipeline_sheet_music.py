# scripts/patch_pipeline_sheet_music.py

with open('src/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = 'from src.phrase_rasa_engine import PhraseRasaEngine'
replacement1 = 'from src.phrase_rasa_engine import PhraseRasaEngine\nfrom src.sheet_music_extractor import SheetMusicExtractor'

target2 = '''            "transcribed_notations": transcriptions,
            "waveform_peaks": waveform_peaks or [],'''

replacement2 = '''            "transcribed_notations": transcriptions,
            "sheet_music_score": SheetMusicExtractor.extract_sheet_music(
                notations=transcriptions,
                tempo_bpm=float(tempo_bpm),
                tonic_hz=float(tonic_hz),
                instrument="piano"
            ),
            "waveform_peaks": waveform_peaks or [],'''

text_lf = text.replace('\r\n', '\n')
target1_lf = target1.replace('\r\n', '\n')
replacement1_lf = replacement1.replace('\r\n', '\n')
target2_lf = target2.replace('\r\n', '\n')
replacement2_lf = replacement2.replace('\r\n', '\n')

if target1_lf in text_lf and target2_lf in text_lf:
    new_text = text_lf.replace(target1_lf, replacement1_lf).replace(target2_lf, replacement2_lf).replace('\n', '\r\n')
    with open('src/pipeline.py', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched src/pipeline.py with sheet_music_score extraction!')
else:
    print('ERROR: Target not found in src/pipeline.py')
