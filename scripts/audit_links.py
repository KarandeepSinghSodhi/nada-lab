"""Audit every URL/DOI referenced in the docs against live sources."""
import re, json, glob, os, urllib.request, urllib.error, time

DOCS = glob.glob(r'd:\Music\*.md')
HDR = {'User-Agent': 'Mozilla/5.0 SongLabAudit/1.0 (mailto:songlab_audit@example.com)'}

def fetch(url, method='GET', timeout=20):
    req = urllib.request.Request(url, headers=HDR, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(200000).decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return None, str(e)

urls = {}
for d in DOCS:
    txt = open(d, encoding='utf-8').read()
    for u in re.findall(r'https?://[^\s\)\]"`>]+', txt):
        u = u.rstrip('.,;')
        urls.setdefault(u, set()).add(os.path.basename(d))

results = []
for u, srcs in sorted(urls.items()):
    note = ''
    status = None
    m = re.match(r'https://github\.com/([^/]+)/([^/#?]+)', u)
    if m:
        status, body = fetch(f'https://api.github.com/repos/{m.group(1)}/{m.group(2)}')
        if status == 200:
            j = json.loads(body); note = f"repo ok: {j.get('full_name')} stars={j.get('stargazers_count')}"
        elif status == 404:
            note = 'REPO NOT FOUND'
        else:
            note = f'github api status {status}'
    elif 'doi.org/' in u:
        doi = u.split('doi.org/')[1]
        status, body = fetch(f'https://api.openalex.org/works/doi:{doi}')
        if status == 200:
            j = json.loads(body); note = f"DOI resolves to: {j.get('title')!r} ({j.get('publication_year')})"
        else:
            note = 'DOI NOT FOUND IN OPENALEX'
    elif 'openalex.org/W' in u:
        wid = u.rsplit('/', 1)[1]
        status, body = fetch(f'https://api.openalex.org/works/{wid}')
        note = (f"W-id is: {json.loads(body).get('title')!r}" if status == 200 else 'OPENALEX ID NOT FOUND')
    elif 'arxiv.org/abs/' in u:
        aid = u.split('/abs/')[1]
        status, body = fetch(f'http://export.arxiv.org/api/query?id_list={aid}')
        t = re.findall(r'<title>(.*?)</title>', body, re.S)
        note = f"arXiv title: {t[1].strip()[:90]!r}" if len(t) > 1 else 'ARXIV ID NOT FOUND'
    elif 'zenodo.org/records/' in u:
        rid = u.rstrip('/').rsplit('/', 1)[1]
        status, body = fetch(f'https://zenodo.org/api/records/{rid}')
        note = (f"zenodo record: {json.loads(body)['metadata']['title'][:90]!r}" if status == 200 else 'ZENODO RECORD NOT FOUND')
    elif 'kaggle.com/datasets/' in u:
        slug = u.split('kaggle.com/datasets/')[1].strip('/')
        parts = slug.split('/')
        if len(parts) < 2:
            status, note = 'BAD', 'INVALID KAGGLE URL (needs owner/slug) -> fabricated'
        else:
            status, body = fetch(u)
            note = f'kaggle http {status}'
    elif 'vertexaisearch' in u:
        continue
    else:
        status, body = fetch(u)
        note = f'http {status}'
    results.append({'url': u, 'status': status, 'note': note, 'docs': sorted(srcs)})
    print(f'[{status}] {u}\n      -> {note}  (in {", ".join(sorted(srcs))})')
    time.sleep(0.4)

json.dump(results, open(r'd:\Music\data\link_audit.json', 'w', encoding='utf-8'), indent=2)
print('\nTOTAL URLS', len(results))
