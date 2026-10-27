with open('d:/Music/src/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"thaat": raga_obj.thaat if raga_obj else "Kalyan",', '"thaat": raga_obj.thaat_or_mela if raga_obj else "Kalyan",')
with open('d:/Music/src/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed thaat in src/pipeline.py')
