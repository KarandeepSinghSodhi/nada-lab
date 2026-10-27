with open('d:/Music/src/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"swara_name": sw_info["name_hindi"],', '"swara_name": sw_info["name"],')
with open('d:/Music/src/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed swara_name in src/pipeline.py')
