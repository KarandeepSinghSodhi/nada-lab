"""
Raga Knowledge Graph & Literature RAG Query Engine for Song Lab.
Indexes:
1. 672 Peer-Reviewed MIR Research Papers from data/curated_research_papers.json
2. 56 Ragas from RAGA_DATABASE with classical treatise grammar (Bhatkhande, Natyashastra)
Provides sub-second lexical and semantic BM25-style search and structured synthesis.
"""

import json
import math
import os
import re
from typing import Dict, List, Optional, Tuple

from src.raga_matcher import RAGA_DATABASE, RagaDefinition, SWARA_TO_SEMITONE


class RagaRAGEngine:
    """
    In-memory knowledge graph and research literature RAG search engine.
    Fast, deterministic, zero-external-dependency BM25-style index.
    """

    def __init__(self, papers_json_path: str = "data/curated_research_papers.json"):
        self.papers_path = papers_json_path
        self.papers: List[Dict] = []
        self.paper_tokens: List[List[str]] = []
        self.doc_freqs: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0
        
        self.raga_index: Dict[str, RagaDefinition] = {
            r.name.lower(): r for r in RAGA_DATABASE
        }
        
        self._load_and_index_papers()

    def _tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 2]
        return tokens

    def _load_and_index_papers(self):
        if not os.path.exists(self.papers_path):
            return
        
        with open(self.papers_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict) and "retained_papers" in data:
            self.papers = data["retained_papers"]
        elif isinstance(data, list):
            self.papers = data
        else:
            self.papers = []

        total_tokens = 0
        self.paper_tokens = []
        self.doc_freqs = {}

        for p in self.papers:
            # Combine searchable fields
            text = " ".join([
                p.get("title", ""),
                p.get("takeaway", ""),
                p.get("target_component", ""),
                " ".join(p.get("concepts", [])),
                " ".join(p.get("authors", [])),
                str(p.get("year", "")),
            ])
            tokens = self._tokenize(text)
            self.paper_tokens.append(tokens)
            total_tokens += len(tokens)

            # Document frequency
            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        self.avg_doc_len = (total_tokens / len(self.papers)) if self.papers else 1.0

    def _bm25_score(self, query_tokens: List[str], doc_idx: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_tokens = self.paper_tokens[doc_idx]
        doc_len = len(doc_tokens)
        N = len(self.papers)
        
        token_counts: Dict[str, int] = {}
        for t in doc_tokens:
            token_counts[t] = token_counts.get(t, 0) + 1

        for q in query_tokens:
            if q not in self.doc_freqs:
                continue
            df = self.doc_freqs[q]
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
            tf = token_counts.get(q, 0)
            numerator = tf * (k1 + 1.0)
            denominator = tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))
            score += idf * (numerator / max(1e-5, denominator))
            
        return score

    def search_literature(self, query: str, top_k: int = 5) -> List[Dict]:
        q_tokens = self._tokenize(query)
        if not q_tokens or not self.papers:
            return []

        scored: List[Tuple[float, int]] = []
        for i in range(len(self.papers)):
            s = self._bm25_score(q_tokens, i)
            if s > 0.05:
                # Add citation weight bonus
                citations = self.papers[i].get("citations", 0)
                cite_bonus = math.log1p(citations) * 0.1
                scored.append((s + cite_bonus, i))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, idx in scored[:top_k]:
            p = self.papers[idx]
            results.append({
                "title": p.get("title"),
                "year": p.get("year"),
                "authors": p.get("authors", [])[:3],
                "doi": p.get("doi"),
                "citations": p.get("citations", 0),
                "takeaway": p.get("takeaway"),
                "target_component": p.get("target_component"),
                "relevance_score": round(score, 3)
            })
        return results

    def get_raga_musicology(self, raga_name: str) -> Optional[Dict]:
        clean_name = raga_name.strip().lower()
        # Direct lookup or substring match
        matched_raga: Optional[RagaDefinition] = self.raga_index.get(clean_name)
        if not matched_raga:
            for name, r in self.raga_index.items():
                if clean_name in name or name in clean_name:
                    matched_raga = r
                    break
        
        if not matched_raga:
            return None

        return {
            "name": matched_raga.name,
            "tradition": matched_raga.tradition,
            "thaat_or_mela": matched_raga.thaat_or_mela,
            "vadi": matched_raga.vadi,
            "samvadi": matched_raga.samvadi,
            "arohana": matched_raga.arohana,
            "avarohana": matched_raga.avarohana,
            "allowed_swaras": matched_raga.allowed_swaras,
            "varjya_swaras": matched_raga.varjya_swaras,
            "pakad_phrases": [" - ".join(p) for p in matched_raga.pakad_phrases],
            "mandatory_ornaments": matched_raga.mandatory_ornaments,
            "treatise_canonical_rules": [
                f"Vadi (Primary King Swara): {matched_raga.vadi} - requires highest resting dwell time.",
                f"Samvadi (Queen Consonant): {matched_raga.samvadi} - provides structural symmetry.",
                f"Varjya Swaras (Prohibited): {', '.join(matched_raga.varjya_swaras) if matched_raga.varjya_swaras else 'None (Sampurna)'}",
                f"Mandatory Ornaments: {', '.join([f'{k} ({v})' for k, v in matched_raga.mandatory_ornaments.items()]) if matched_raga.mandatory_ornaments else 'Clean portamento meends'}",
            ]
        }

    def answer_query(self, query: str, target_raga: Optional[str] = None) -> Dict:
        """
        Synthesizes an authoritative musicological answer cross-referencing
        classical treatise rules and peer-reviewed MIR papers.
        """
        # 1. Detect any mentioned raga if target_raga not explicitly given
        detected_raga_name = target_raga
        if not detected_raga_name:
            for name in self.raga_index.keys():
                if name in query.lower():
                    detected_raga_name = self.raga_index[name].name
                    break

        raga_info = self.get_raga_musicology(detected_raga_name) if detected_raga_name else None

        # 2. Search relevant literature
        combined_query = query
        if detected_raga_name:
            combined_query += f" {detected_raga_name} raga ornament pitch tracking"
        papers = self.search_literature(combined_query, top_k=3)

        # 3. Formulate structured response
        explanation_parts = []
        if raga_info:
            explanation_parts.append(
                f"In the {raga_info['tradition']} tradition, **Raga {raga_info['name']}** belongs to the {raga_info['thaat_or_mela']} framework. "
                f"Its Vadi is **{raga_info['vadi']}** and Samvadi is **{raga_info['samvadi']}**."
            )
            if raga_info['varjya_swaras']:
                explanation_parts.append(
                    f"**Forbidden Invariants (Varjya):** The notes `{', '.join(raga_info['varjya_swaras'])}` are strictly prohibited in normal scalar movement."
                )
            if raga_info['mandatory_ornaments']:
                orn_desc = ", ".join([f"**{k}** requiring {v}" for k, v in raga_info['mandatory_ornaments'].items()])
                explanation_parts.append(f"**Ornamental Requirements:** {orn_desc}.")
            if raga_info['pakad_phrases']:
                explanation_parts.append(f"**Canonical Pakad Phrase:** `{raga_info['pakad_phrases'][0]}`.")
        else:
            explanation_parts.append(
                "Acoustic and musicological analysis according to Indian Classical Music Information Retrieval (MIR) literature."
            )

        if papers:
            explanation_parts.append(
                f"**Acoustic Literature Evidence:** Documented across peer-reviewed publications, including {papers[0]['authors'][0]} et al. ({papers[0]['year']}) on *'{papers[0]['title']}'* ({papers[0]['takeaway']})."
            )

        return {
            "query": query,
            "target_raga": detected_raga_name,
            "raga_musicology": raga_info,
            "literature_citations": papers,
            "synthesis": " \n\n".join(explanation_parts)
        }
