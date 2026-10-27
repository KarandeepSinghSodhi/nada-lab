with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<span class="btn-icon">📁</span>\n                  ', '')
text = text.replace('<span>⚡ Try Sample Phrase</span>', '<span>Try Sample Phrase</span>')
text = text.replace('<span>📄 Download JSON</span>', '<span>Download JSON</span>')
text = text.replace('<span>🖨️ Print Report</span>', '<span>Print Report</span>')
text = text.replace('<span class="dossier-drill-lbl">💡 Prescriptive Guru Drill:</span>', '<span class="dossier-drill-lbl">Prescriptive Guru Drill:</span>')

with open('d:/Music/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Removed emojis from index.html')
