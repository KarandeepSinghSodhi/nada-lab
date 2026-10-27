# 1. Update app.js
with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('rupak: {')
end_idx = text.find('};', idx)
rupak_block = text[idx:end_idx]

new_rupak_block = """rupak: {
      name: 'Rupak',
      matras: 7,
      vibhags: [3, 2, 2],
      bols: ['Tin', 'Tin', 'Na', 'Dhin', 'Na', 'Dhin', 'Na'],
      tags: ['0 (Khali)', '2', '3', '1 (Tali)', '5', '2 (Tali)', '7'],
      samIndex: 0
    },
    jhaptal: {
      name: 'Jhaptal',
      matras: 10,
      vibhags: [2, 3, 2, 3],
      bols: ['Dhi', 'Na', 'Dhi', 'Dhi', 'Na', 'Ti', 'Na', 'Dhi', 'Dhi', 'Na'],
      tags: ['X (Sam)', '2', '2 (Tali)', '4', '5', '0 (Khali)', '7', '3 (Tali)', '9', '10'],
      samIndex: 0
    },
    dadra: {
      name: 'Dadra',
      matras: 6,
      vibhags: [3, 3],
      bols: ['Dha', 'Dhin', 'Na', 'Dha', 'Tin', 'Na'],
      tags: ['X (Sam)', '2', '3', '0 (Khali)', '5', '6'],
      samIndex: 0
    }
  """

text = text[:idx] + new_rupak_block + text[end_idx:]

# Also update Laya indicator in slider
old_slider = "talaTempoBpm = parseInt(slider.value, 10);"
new_slider = """talaTempoBpm = parseInt(slider.value, 10);
        const layaLabel = talaTempoBpm < 60 ? 'Vilambit' : (talaTempoBpm > 140 ? 'Drut' : 'Madhya');
        if (tempoVal) tempoVal.textContent = talaTempoBpm + ' BPM (' + layaLabel + ')';"""
if old_slider in text:
    text = text.replace(old_slider, new_slider, 1)

with open('d:/Music/app.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

# 2. Update index.html
with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx_html = html.find('<select id="ui-tala-select"')
end_idx_html = html.find('</select>', idx_html)

new_select = """<select id="ui-tala-select" class="ui-tala-select">
                      <option value="teentaal">Teentaal (16 Matras · 4+4+4+4)</option>
                      <option value="jhaptal">Jhaptal (10 Matras · 2+3+2+3)</option>
                      <option value="rupak">Rupak (7 Matras · 3+2+2)</option>
                      <option value="keharwa">Keharwa (8 Matras · 4+4)</option>
                      <option value="dadra">Dadra (6 Matras · 3+3)</option>
                      <option value="aditala">Adi Tala (8 Aksharas · 4+2+2)</option>
                    </select>"""

html = html[:idx_html] + new_select + html[end_idx_html+9:]

with open('d:/Music/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(html)

print("SUCCESS: Updated app.js and index.html with Jhaptal and Dadra!")
