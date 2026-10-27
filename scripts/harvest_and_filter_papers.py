import urllib.request
import urllib.parse
import json
import time
import sys
import re

QUERIES = [
    # Query 1: Core Indian Classical MIR, Raga, Swara
    '("indian art music" OR "indian classical music" OR "raga recognition" OR "raga classification")',
    # Query 2: Carnatic & Hindustani Audio / Pitch / Computational
    '("carnatic" OR "hindustani") AND ("audio" OR "pitch" OR "transcription" OR "computation" OR "recognition" OR "melody")',
    # Query 3: Tonic, Drone, Intonation, Gamaka, Meend, Shruti
    '("tonic identification" OR "tonic estimation" OR "gamaka" OR "gamak" OR "meend" OR "andolan" OR "shruti" OR "swara")',
    # Query 4: Tala, Rhythm, Tabla, Mridangam stroke detection
    '("tala tracking" OR "meter tracking" OR "tabla stroke" OR "mridangam stroke" OR "taal recognition")',
    # Query 5: Singing Voice Evaluation, Vocal Ornamentation, Pitch Tracking
    '("singing voice evaluation" OR "vocal ornamentation" OR "singing pitch tracking" OR "vocal transcription" OR "continuous pitch to notes")'
]

HEADERS = {
    'User-Agent': 'SongLabResearch/1.0 (mailto:songlab_mir_research@deepmind-antigravity.dev)'
}

FAMOUS_IAM_RESEARCHERS = [
    'xavier serra', 'preeti rao', 'sankalp gulati', 'ajay srinivasamurthy', 'parag chordia',
    'alex rae', 'h. g. ranjani', 'sertan senturk', 'kaustuv kanti ganguli', 'gopala krishna koduri',
    'suvarnalata rao', 'wim van der meer', 'justin salamon', 'joan serra', 'andre holzapfel',
    't. m. krishna', 'suman narayan', 'vinutha', 'arun shenoy', 'chandan vaidya'
]

MIR_VENUES = [
    'ismir', 'international society for music information retrieval', 'icassp', 'dafx',
    'computer music journal', 'journal of the acoustical society of america',
    'ieee transactions on audio, speech, and language processing', 'transactions of the international society for music information retrieval',
    'tismir', 'folk music analysis', 'fma', 'sound and music computing', 'smc'
]

IRRELEVANT_PATTERNS = [
    r'\braga protein\b', r'\brag-a\b', r'\bgene\b', r'\bmutation\b', r'\bmolecular\b',
    r'\bcarcinoma\b', r'\btherapeutic effect\b', r'\bautism\b', r'\bdementia\b',
    r'\bpharmacology\b', r'\bclinical trial\b', r'\bneoplasm\b', r'\brabbit\b', r'\bmice\b',
    r'\bpatient\b', r'\bblood pressure\b', r'\bhypertension\b', r'\bpsychiatry\b'
]

def fetch_candidates_from_openalex(target_total=3000):
    candidates = {}
    per_query_target = target_total // len(QUERIES) + 150
    
    print(f"Starting harvest of ~{target_total} candidate papers across {len(QUERIES)} search domains...")
    
    for q_idx, query_str in enumerate(QUERIES, 1):
        page = 1
        query_candidates = 0
        encoded_query = urllib.parse.quote(query_str)
        
        print(f"\n[Query {q_idx}/{len(QUERIES)}] Harvesting: {query_str[:70]}...")
        
        while query_candidates < per_query_target and page <= 12:
            url = f"https://api.openalex.org/works?search={encoded_query}&per-page=100&page={page}&select=id,title,publication_year,cited_by_count,doi,authorships,primary_location,concepts,type&mailto=songlab_mir_research@deepmind-antigravity.dev"
            
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    results = data.get('results', [])
                    if not results:
                        break
                    
                    for item in results:
                        work_id = item.get('id')
                        if work_id and work_id not in candidates:
                            candidates[work_id] = item
                            query_candidates += 1
                            
                    print(f"  Page {page}: fetched {len(results)} items (Total unique so far: {len(candidates)})")
                    page += 1
                    time.sleep(0.15) # Polite delay
            except Exception as e:
                print(f"  Error on page {page}: {e}")
                time.sleep(1)
                break
                
            if len(candidates) >= target_total + 200:
                break
        if len(candidates) >= target_total + 200:
            break
            
    print(f"\nHarvesting complete! Total unique candidate papers collected: {len(candidates)}")
    return list(candidates.values())

def parse_work(item):
    title = item.get('title') or ''
    year = item.get('publication_year') or 0
    cites = item.get('cited_by_count') or 0
    doi = item.get('doi') or ''
    openalex_id = item.get('id') or ''
    work_type = item.get('type') or ''
    
    authors = []
    for a in item.get('authorships', []):
        author_info = a.get('author', {})
        if author_info.get('display_name'):
            authors.append(author_info.get('display_name'))
            
    source_name = ''
    pl = item.get('primary_location') or {}
    source = pl.get('source') or {}
    if source.get('display_name'):
        source_name = source.get('display_name')
        
    concepts = []
    for c in item.get('concepts', []):
        if c.get('display_name'):
            concepts.append(c.get('display_name'))
            
    return {
        'id': openalex_id,
        'title': title,
        'year': year,
        'citations': cites,
        'doi': doi,
        'authors': authors,
        'source': source_name,
        'concepts': concepts,
        'work_type': work_type
    }

def evaluate_and_filter_paper(paper):
    title_lower = paper['title'].lower()
    source_lower = paper['source'].lower()
    concepts_lower = [c.lower() for c in paper['concepts']]
    concepts_text = " ".join(concepts_lower)
    authors_lower = [a.lower() for a in paper['authors']]
    
    # 1. Immediate Disqualifiers (Medical / Genetics / Non-music collisions)
    for pat in IRRELEVANT_PATTERNS:
        if re.search(pat, title_lower):
            return False, "Biological / Medical / Genetic collision (e.g. RAGA protein, gene mutation, clinical disease)", None, None

    # Check if purely music therapy without computational analysis
    if ('therapy' in title_lower or 'therapeutic' in title_lower) and not any(k in title_lower for k in ['audio', 'pitch', 'model', 'computation', 'feature', 'recognition']):
        return False, "Music therapy / medical application without MIR or signal processing modeling", None, None

    # 2. Relevance Scoring
    score = 0
    
    # Author credibility in IAM MIR
    for author in authors_lower:
        if any(f in author for f in FAMOUS_IAM_RESEARCHERS):
            score += 15
            
    # Venue credibility in MIR / Audio
    for venue in MIR_VENUES:
        if venue in source_lower:
            score += 12
            
    # Core technical keywords in title
    mir_title_keywords = {
        'raga': 8, 'raag': 8, 'carnatic': 7, 'hindustani': 7, 'gamaka': 10, 'meend': 10,
        'andolan': 10, 'swara': 8, 'svara': 8, 'shruti': 8, 'sruti': 8, 'tala': 9, 'taal': 9,
        'tonic': 9, 'tabla': 8, 'mridangam': 8, 'pitch': 6, 'transcription': 7, 'alap': 7,
        'f0': 7, 'singing': 6, 'vocal': 5, 'music information retrieval': 12, 'audio': 4,
        'intonation': 6, 'microtonal': 7, 'classification': 4, 'convolutional': 5, 'lstm': 5,
        'dataset': 5, 'saraga': 12, 'compmusic': 12, 'tanpura': 8, 'drone': 6
    }
    
    for kw, weight in mir_title_keywords.items():
        if kw in title_lower:
            score += weight
            
    # Concept matching
    music_concepts = ['music', 'acoustics', 'speech recognition', 'signal processing', 'melody', 'rhythm', 'artificial intelligence']
    for mc in music_concepts:
        if mc in concepts_text:
            score += 2
            
    # Filter threshold: minimum score 12 required
    if score < 12:
        return False, "Low computational/audio relevance score; generic cultural/historical commentary lacking engineering or signal analysis", None, None
        
    # 3. Component Mapping & Algorithmic Takeaway
    comp = "Component 6: Raga Intelligence & Phrase Matching"
    takeaway = "Extracts melodic contours and transition probabilities for raga classification."
    
    if any(k in title_lower for k in ['tonic', 'drone', 'tanpura', 'tambura']):
        comp = "Component 3: Tonal Normalization & Tonic (Sa) Tracking"
        takeaway = "Provides multipitch salience or spectral peak tracking to reliably anchor fundamental Sa."
    elif any(k in title_lower for k in ['gamak', 'gamaka', 'meend', 'andolan', 'murki', 'ornament', 'vibrato', 'glide', 'inflection']):
        comp = "Component 4: Dual-Mode Ornament & Expression Detection"
        takeaway = "Mathematical modeling of continuous pitch fluctuations, slides, and microtonal inflections."
    elif any(k in title_lower for k in ['tala', 'taal', 'tabla', 'mridangam', 'meter', 'rhythm', 'stroke']):
        comp = "Component 7: Rhythm, Tala & Laya Tracking"
        takeaway = "Models hierarchical metric cycles, stroke onsets, and downbeat (Sam) detection."
    elif any(k in title_lower for k in ['transcription', 'continuous pitch to', 'swara identification', 'note segmentation', 'sargam']):
        comp = "Component 2 & 5: Pitch Extraction, Swara Quantization & Deficit Detection"
        takeaway = "Bridges continuous pitch curves into discrete swara events and identifies structural deviations."
    elif any(k in title_lower for k in ['separation', 'demixing', 'stem', 'accompaniment removal', 'vocal isolation']):
        comp = "Component 1: Vocal Demixing & Audio Ingestion"
        takeaway = "Isolates lead singing from tanpura drone and percussive tabla leakage."
    elif any(k in title_lower for k in ['synthesis', 'voice conversion', 'generative', 'singing voice generation']):
        comp = "Component 10: Generative Audio & Virtual Guru Synthesis"
        takeaway = "Synthesizes raga-constrained melodic drills and applies vocal timbre transfer."
    elif any(k in title_lower for k in ['corpus', 'dataset', 'ontology', 'knowledge', 'saraga', 'dunya']):
        comp = "Component 8: Curated Knowledge Base & Raga Knowledge Graph"
        takeaway = "Standardized musicological ontology and ground-truth metadata for classical verification."
        
    return True, "Highly Relevant", comp, takeaway

def main():
    raw_works = fetch_candidates_from_openalex(target_total=3000)
    
    parsed_papers = [parse_work(w) for w in raw_works]
    
    retained_papers = []
    dropped_papers = []
    
    component_stats = {}
    
    for p in parsed_papers:
        is_rel, reason, comp, takeaway = evaluate_and_filter_paper(p)
        p['is_relevant'] = is_rel
        p['evaluation_note'] = reason
        p['target_component'] = comp
        p['takeaway'] = takeaway
        
        if is_rel:
            retained_papers.append(p)
            component_stats[comp] = component_stats.get(comp, 0) + 1
        else:
            dropped_papers.append(p)
            
    # Sort retained by citations descending
    retained_papers.sort(key=lambda x: x['citations'], reverse=True)
    
    print("\n" + "="*60)
    print("HARVESTING & FILTERING RESULTS SUMMARY")
    print("="*60)
    print(f"Total Candidate Papers Screened: {len(parsed_papers)}")
    print(f"Papers Dropped (Irrelevant/Noise): {len(dropped_papers)} ({len(dropped_papers)/len(parsed_papers)*100:.1f}%)")
    print(f"Papers Retained (High-Value MIR): {len(retained_papers)} ({len(retained_papers)/len(parsed_papers)*100:.1f}%)")
    print("\nDistribution Across Song Lab Components:")
    for comp, count in sorted(component_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {comp}: {count} papers")
        
    # Save full JSON dataset
    output_path = r'd:\Music\data\curated_research_papers.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_screened': len(parsed_papers),
                'retained_count': len(retained_papers),
                'dropped_count': len(dropped_papers),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'retained_papers': retained_papers,
            'sample_dropped_papers': dropped_papers[:250] # Sample of dropped for auditing
        }, f, indent=2, ensure_ascii=False)
        
    print(f"\nSaved curated research corpus to: {output_path}")

if __name__ == '__main__':
    main()
