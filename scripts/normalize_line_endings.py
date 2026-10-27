# scripts/normalize_line_endings.py

for filename in ['app.js', 'styles.css', 'index.html']:
    with open(filename, 'rb') as f:
        data = f.read()
    # Normalize \r\r\n and \r to \n first, then to \r\n
    data_norm = data.replace(b'\r\r\n', b'\n').replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    data_crlf = data_norm.replace(b'\n', b'\r\n')
    with open(filename, 'wb') as f:
        f.write(data_crlf)
    print(f'Normalized {filename}: {len(data_crlf.split(b"\r\n"))} lines')
