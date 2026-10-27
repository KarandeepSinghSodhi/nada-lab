# scripts/fix_pipeline_tempo.py

with open('src/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'tempo_bpm=float(tempo_bpm),'
replacement = 'tempo_bpm=float(tempo_info.get("bpm", 84.0) if tempo_info else 84.0),'

if target in text:
    new_text = text.replace(target, replacement)
    with open('src/pipeline.py', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Fixed tempo_bpm in src/pipeline.py')
else:
    print('Target not found')
