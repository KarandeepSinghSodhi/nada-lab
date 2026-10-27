"""Verify the specific paper claims made in the docs exist (title/year/authors)."""
import json, urllib.request, urllib.parse, time

HDR = {'User-Agent': 'SongLabAudit/1.0 (mailto:songlab_audit@example.com)'}
CLAIMS = [
    ("Raag recognition using pitch-class and pitch-class dyad distributions", 2007, "Chordia"),
    ("Time-delayed melody surfaces for raga recognition", 2016, "Gulati"),
    ("DeepSRGM sequence classification and ranking in Indian classical music", 2019, "Madhusudhan"),
    ("A multipitch approach to tonic identification in Indian classical music", 2012, "Salamon"),
    ("Automatic tonic identification in Indian art music: approaches and evaluation", 2014, "Gulati"),
    ("Particle filters for efficient meter tracking with dynamic Bayesian networks", 2015, "Srinivasamurthy"),
    ("A hierarchical Bayesian approach to tala tracking", 2014, "Srinivasamurthy"),
    ("Quantized melodic contours in Indian art music perception application to transcription", None, "Ranjani"),
    ("Tabla gharana recognition from audio music recordings of tabla solo performances", None, "Gowriprasad"),
    ("Saraga: open datasets for research on Indian art music", 2020, "Srinivasamurthy"),
    ("Dunya: a system for browsing audio music collections exploiting cultural context", 2013, "Porter"),
    ("Essentia: an audio analysis library for music information retrieval", 2013, "Bogdanov"),
    ("Modeling ornaments in Carnatic music signals via wavelets", 2020, "Sasindran"),
    ("Carnatic music: svara, gamaka, motif and raga identity", 2012, "Krishna"),
    ("Hierarchical generative modeling of melodic vocal contours in Hindustani classical music", 2024, "Shikarpur"),
    ("Mellotron: multispeaker expressive voice synthesis by conditioning on rhythm, pitch and global style tokens", 2020, "Valle"),
    ("Raga and tonic identification in Carnatic music", 2017, "Manjabhat"),
    ("Segmentation and recognition of tabla strokes", 2005, "Chordia"),
    ("Tracking the odd: meter inference in a culturally diverse music corpus", 2014, "Holzapfel"),
    ("Informed automatic meter analysis of music recordings", 2017, "Srinivasamurthy"),
    ("Recognizing ornaments in vocal Indian art music with active annotation", None, "Kumar"),
]

out = []
for title, year, author in CLAIMS:
    q = urllib.parse.quote(title)
    url = f"https://api.openalex.org/works?search={q}&per-page=3&select=id,title,publication_year,doi,authorships,primary_location"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=20) as r:
            res = json.loads(r.read())['results']
    except Exception as e:
        res = []
    best = None
    for w in res:
        names = ' '.join(a['author']['display_name'] for a in w.get('authorships', []))
        if author.lower() in names.lower():
            best = w; break
    if best:
        src = ((best.get('primary_location') or {}).get('source') or {}).get('display_name')
        rec = dict(claim=title, claimed_year=year, found=best['title'], year=best['publication_year'],
                   doi=best.get('doi'), id=best['id'], venue=src)
        flag = '' if (year is None or best['publication_year'] == year) else f'  <-- YEAR MISMATCH (claimed {year})'
        print(f"OK   {best['publication_year']} | {best['title'][:80]} | {src} | {best.get('doi')}{flag}")
    else:
        rec = dict(claim=title, claimed_year=year, found=None)
        print(f"MISS {title}  (top hit: {res[0]['title'][:70] if res else 'none'})")
    out.append(rec)
    time.sleep(0.3)
json.dump(out, open(r'd:\Music\data\paper_claim_audit.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
