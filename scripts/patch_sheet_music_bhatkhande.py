import re

target_file = r'd:\Music\src\sheet_music_extractor.py'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Expand CANONICAL_PHRASE_LYRICS
old_lyrics = '''    CANONICAL_PHRASE_LYRICS = {
        "yaman_meend": "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
        "yaman_varjya": "Ni-si di-na ta-da-pat chain na aa-ve",
        "darbari_andolan": "A-no-kha laad-la khe-lan-ko maa-nge chaand",
        "darbari_flat": "Haz-rat Khwa-ja sang khe-lie ho-ri",
        "bhairav_flutter": "Jaa-go mo-han pya-re jaa-go nan-da la-la",
        "real_vocal": "Baa-je re mu-ra-li-ya baa-je baan-su-ri"
    }'''

new_lyrics = '''    CANONICAL_PHRASE_LYRICS = {
        "yaman_meend": "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
        "yaman_eri_aali": "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
        "yaman_varjya": "Ni-si di-na ta-da-pat chain na aa-ve",
        "darbari_andolan": "A-no-kha laad-la khe-lan-ko maa-nge chaand",
        "darbari_rakhwale": "O du-ni-ya ke rakh-waa-le su-no dard bha-re var-daan",
        "darbari_flat": "Haz-rat Khwa-ja sang khe-lie ho-ri",
        "bhairav_flutter": "Jaa-go mo-han pya-re jaa-go nan-da la-la",
        "bhairav_jaago": "Jaa-go mo-han pya-re jaa-go nan-da la-la",
        "real_vocal": "Baa-je re mu-ra-li-ya baa-je baan-su-ri",
        "bhoopali_jyoti": "Jyo-ti ka-lash chhal-ke hue gu-laa-bi laal do na-yan",
        "khamaj_panghat": "Mo-he pang-hat pe Nan-da-laal chhed ga-yo re",
        "ahir_bhairav_poocho": "Poo-cho na kai-se mai-ne rain bi-tai",
        "hamir_madhuban": "Ma-dhu-ban mein Ra-dhi-ka na-che re",
        "sohini_kuhu_kuhu": "Ku-hu ku-hu bo-le ko-ya-li-ya kun-jan mein ko-ya-li-ya"
    }'''

if old_lyrics in content:
    content = content.replace(old_lyrics, new_lyrics)
    print("Expanded CANONICAL_PHRASE_LYRICS in sheet_music_extractor.py")
else:
    print("WARNING: old_lyrics not found in sheet_music_extractor.py")

# 2. Add to_bhatkhande_sargam_sheet method
bhatkhande_exporter_code = '''
    @classmethod
    def to_bhatkhande_sargam_sheet(cls, lead_sheet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms a Lead Sheet into a conservatory-standard Bhatkhande notation score.
        """
        title = lead_sheet.get("title", "Bhatkhande Sargam Score")
        tempo_bpm = lead_sheet.get("tempo_bpm", 84.0)
        time_sig = lead_sheet.get("time_signature", "4/4")
        measures = lead_sheet.get("measures", [])

        SARGAM_TO_BHATKHANDE = {
            "S": "सा", "r": "<u>रे</u>", "R": "रे", "g": "<u>ग</u>", "G": "ग",
            "m": "म", "M": "म॑", "P": "प", "d": "<u>ध</u>", "D": "ध",
            "n": "<u>नि</u>", "N": "नि", "S'": "सां", "R'": "रे ं", "G'": "गं",
            "N,": "नि़", "D,": "ध़", "P,": "प़", "M,": "म़"
        }

        ascii_lines = []
        ascii_lines.append("══════════════════════════════════════════════════════════════════════")
        ascii_lines.append(f"  BHATKHANDE SARGAM SCORE: {title.upper()}")
        ascii_lines.append(f"  Tala: Teentaal (16 Matras) | Tempo: {tempo_bpm:.0f} BPM | Time Sig: {time_sig}")
        ascii_lines.append("══════════════════════════════════════════════════════════════════════\\n")

        html_measures = []

        for m_idx, m in enumerate(measures):
            m_num = m.get("measure_number", m_idx + 1)
            chord = m.get("chord", "D")
            events = m.get("events", [])

            swara_row = []
            lyric_row = []
            tab_row = []
            tala_marker = "+" if (m_idx % 4 == 0) else ("0" if (m_idx % 4 == 2) else f"{((m_idx % 4) + 1)}")

            html_events = []

            for ev_idx, ev in enumerate(events):
                raw_sargam = ev.get("note_sargam", "S")
                syllable = ev.get("syllable", "—")
                trans = ev.get("in_between_transition") or {}
                has_meend = bool(trans and ("Meend" in str(trans.get("transition_type", "")) or "S-Curve" in str(trans.get("transition_type", ""))))
                kan_swara = (trans.get("kan_touch") or {}).get("swara_symbol", "")

                dev_swara = SARGAM_TO_BHATKHANDE.get(raw_sargam, raw_sargam)
                if has_meend:
                    dev_swara += "⌒"
                if kan_swara:
                    dev_swara = f"({kan_swara})" + dev_swara

                fingering = ev.get("flute_fingering") or (ev.get("guitar_tab") or {}).get("tab_label") or f"Key {ev.get('piano_key', 60)}"

                swara_row.append(f"{dev_swara:>8}")
                lyric_row.append(f"{syllable:>8}")
                tab_row.append(f"{fingering:>8}")

                html_events.append(f"""
                  <div class="bhatkhande-event">
                    <span class="bk-tala-sub">{tala_marker if ev_idx == 0 else ''}</span>
                    <span class="bk-swara-val">{dev_swara}</span>
                    <span class="bk-lyric-val">{syllable}</span>
                    <span class="bk-tab-val">{fingering}</span>
                  </div>
                """)

            ascii_lines.append(f"  [Bar {m_num} · {chord} · Vibhag {tala_marker}]")
            ascii_lines.append("  Swaras:  " + " ".join(swara_row) + " |")
            ascii_lines.append("  Lyrics:  " + " ".join(lyric_row) + " |")
            ascii_lines.append("  Tabs:    " + " ".join(tab_row) + " |\\n")

            html_measures.append(f"""
              <div class="bhatkhande-measure">
                <div class="bhatkhande-measure-header">
                  <span class="bk-measure-badge">Vibhag {tala_marker} (Bar {m_num})</span>
                  <span class="bk-chord-badge">[ {chord} ]</span>
                </div>
                <div class="bhatkhande-events-row">
                  {''.join(html_events)}
                </div>
              </div>
            """)

        full_html = f"""
          <div class="bhatkhande-score-card">
            <div class="bhatkhande-header-box">
              <h3 class="bhatkhande-title">{title}</h3>
              <div class="bhatkhande-meta-row">
                <span class="bk-meta-pill">Tala: Teentaal (16 Matras)</span>
                <span class="bk-meta-pill">Tempo: {tempo_bpm:.0f} BPM</span>
                <span class="bk-meta-pill">Sam: + | Khali: 0 | Taali: 2, 3</span>
              </div>
            </div>
            <div class="bhatkhande-measures-grid">
              {''.join(html_measures)}
            </div>
          </div>
        """

        return {
            "title": title,
            "tempo_bpm": tempo_bpm,
            "time_signature": time_sig,
            "total_measures": len(measures),
            "ascii_sheet": "\\n".join(ascii_lines),
            "html_score": full_html
        }
'''

if "def to_bhatkhande_sargam_sheet" not in content:
    content += bhatkhande_exporter_code
    print("Added to_bhatkhande_sargam_sheet to sheet_music_extractor.py")
else:
    print("to_bhatkhande_sargam_sheet already present.")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated sheet_music_extractor.py successfully.")
