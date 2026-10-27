import re

corpus_path = r'd:\Music\research_lab\benchmarks\hindi_songs_benchmark_corpus.py'

with open(corpus_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Additional 4 songs code:
additions = '''
    # 5. Raga Bhoopali: "Jyoti Kalash Chhalke"
    bhoopali_notes = [
        {"note": "D4", "sargam": "S", "cents": 0.0, "start_time": 0.0, "end_time": 0.35, "syllable": "Jyo-"},
        {"note": "E4", "sargam": "R", "cents": 200.0, "start_time": 0.55, "end_time": 0.90, "syllable": "ti"},
        {"note": "F#4", "sargam": "G", "cents": 400.0, "start_time": 1.10, "end_time": 1.45, "syllable": "ka-"},
        {"note": "A4", "sargam": "P", "cents": 700.0, "start_time": 1.65, "end_time": 2.05, "syllable": "lash"},
        {"note": "B4", "sargam": "D", "cents": 900.0, "start_time": 2.30, "end_time": 2.70, "syllable": "chhal-"},
        {"note": "F#4", "sargam": "G", "cents": 400.0, "start_time": 2.95, "end_time": 3.45, "syllable": "ke"},
    ]

    t_bhoopali = np.linspace(0.0, 3.5, 351)
    c_bhoopali = np.zeros_like(t_bhoopali)
    for i, t in enumerate(t_bhoopali):
        if t < 0.35:
            c_bhoopali[i] = 0.0
        elif 0.35 <= t < 0.55:
            u = (t - 0.35) / 0.20
            c_bhoopali[i] = 200.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 0.55 <= t < 0.90:
            c_bhoopali[i] = 200.0
        elif 0.90 <= t < 1.10:
            u = (t - 0.90) / 0.20
            c_bhoopali[i] = 200.0 + 200.0 * (u ** 3)
        elif 1.10 <= t < 1.45:
            c_bhoopali[i] = 400.0
        elif 1.45 <= t < 1.65:
            u = (t - 1.45) / 0.20
            c_bhoopali[i] = 400.0 + 300.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 1.65 <= t < 2.05:
            c_bhoopali[i] = 700.0
        elif 2.05 <= t < 2.30:
            u = (t - 2.05) / 0.25
            if u < 0.45:
                v = u / 0.45
                c_bhoopali[i] = 700.0 + 500.0 / (1.0 + np.exp(-14.0 * (v - 0.5))) # Touch Taar Sa (1200)
            else:
                w = (u - 0.45) / 0.55
                c_bhoopali[i] = 1200.0 - 300.0 / (1.0 + np.exp(-14.0 * (w - 0.5))) # Land Dha (900)
        elif 2.30 <= t < 2.70:
            c_bhoopali[i] = 900.0
        elif 2.70 <= t < 2.95:
            u = (t - 2.70) / 0.25
            c_bhoopali[i] = 900.0 - 500.0 / (1.0 + np.exp(-14.0 * (u - 0.5))) # Descending meend Dha -> Ga
        else:
            c_bhoopali[i] = 400.0

    corpus["bhoopali_jyoti"] = {
        "title": "Jyoti Kalash Chhalke (Raga Bhoopali)",
        "raga": "Bhoopali",
        "tonic_hz": 146.83,
        "notes": bhoopali_notes,
        "times": t_bhoopali,
        "cents": c_bhoopali,
        "ground_truth_transitions": [
            {"from": "S", "to": "R", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "R", "to": "G", "type": "MEEND_CONVEX_SCOOP", "has_kan": False},
            {"from": "G", "to": "P", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "P", "to": "D", "type": "KAN_INFLECTED", "has_kan": True, "kan_swara": "S'"},
            {"from": "D", "to": "G", "type": "MEEND_SIGMOID", "has_kan": False},
        ],
    }

    # 6. Raga Ahir Bhairav: "Poocho Na Kaise Maine Rain Bitai"
    ahir_notes = [
        {"note": "D4", "sargam": "S", "cents": 0.0, "start_time": 0.0, "end_time": 0.40, "syllable": "Poo-"},
        {"note": "Eb4", "sargam": "r", "cents": 100.0, "start_time": 0.65, "end_time": 1.05, "syllable": "cho"},
        {"note": "F#4", "sargam": "G", "cents": 400.0, "start_time": 1.25, "end_time": 1.60, "syllable": "na"},
        {"note": "G4", "sargam": "m", "cents": 500.0, "start_time": 1.80, "end_time": 2.15, "syllable": "kai-"},
        {"note": "A4", "sargam": "P", "cents": 700.0, "start_time": 2.35, "end_time": 2.70, "syllable": "se"},
        {"note": "B4", "sargam": "D", "cents": 900.0, "start_time": 2.90, "end_time": 3.25, "syllable": "mai-"},
        {"note": "C5", "sargam": "n", "cents": 1000.0, "start_time": 3.50, "end_time": 3.85, "syllable": "ne"},
        {"note": "B4", "sargam": "D", "cents": 900.0, "start_time": 4.05, "end_time": 4.50, "syllable": "rain"},
    ]

    t_ahir = np.linspace(0.0, 4.6, 461)
    c_ahir = np.zeros_like(t_ahir)
    for i, t in enumerate(t_ahir):
        if t < 0.40:
            c_ahir[i] = 0.0
        elif 0.40 <= t < 0.65:
            # Gamak oscillation approaching Komal Re
            u = (t - 0.40) / 0.25
            c_ahir[i] = 100.0 * u + 40.0 * np.sin(2.0 * np.pi * 5.0 * (t - 0.40))
        elif 0.65 <= t < 1.05:
            c_ahir[i] = 100.0
        elif 1.05 <= t < 1.25:
            u = (t - 1.05) / 0.20
            c_ahir[i] = 100.0 + 300.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 1.25 <= t < 1.60:
            c_ahir[i] = 400.0
        elif 1.60 <= t < 1.80:
            u = (t - 1.60) / 0.20
            c_ahir[i] = 400.0 + 100.0 * (u ** 3) # Scoop into Ma
        elif 1.80 <= t < 2.15:
            c_ahir[i] = 500.0
        elif 2.15 <= t < 2.35:
            u = (t - 2.15) / 0.20
            c_ahir[i] = 500.0 + 200.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 2.35 <= t < 2.70:
            c_ahir[i] = 700.0
        elif 2.70 <= t < 2.90:
            u = (t - 2.70) / 0.20
            c_ahir[i] = 700.0 + 200.0 * u # Linear ramp to Dha
        elif 2.90 <= t < 3.25:
            c_ahir[i] = 900.0
        elif 3.25 <= t < 3.50:
            # Kan touch of Taar Sa (1200) then resolve to Komal Ni (1000)
            u = (t - 3.25) / 0.25
            if u < 0.45:
                v = u / 0.45
                c_ahir[i] = 900.0 + 300.0 / (1.0 + np.exp(-14.0 * (v - 0.5)))
            else:
                w = (u - 0.45) / 0.55
                c_ahir[i] = 1200.0 - 200.0 / (1.0 + np.exp(-14.0 * (w - 0.5)))
        elif 3.50 <= t < 3.85:
            c_ahir[i] = 1000.0
        elif 3.85 <= t < 4.05:
            u = (t - 3.85) / 0.20
            c_ahir[i] = 1000.0 - 100.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        else:
            c_ahir[i] = 900.0

    corpus["ahir_bhairav_poocho"] = {
        "title": "Poocho Na Kaise Maine (Raga Ahir Bhairav)",
        "raga": "Ahir Bhairav",
        "tonic_hz": 146.83,
        "notes": ahir_notes,
        "times": t_ahir,
        "cents": c_ahir,
        "ground_truth_transitions": [
            {"from": "S", "to": "r", "type": "GAMAK_OSCILLATION", "has_kan": False},
            {"from": "r", "to": "G", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "G", "to": "m", "type": "MEEND_CONVEX_SCOOP", "has_kan": False},
            {"from": "m", "to": "P", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "P", "to": "D", "type": "MEEND_LINEAR", "has_kan": False},
            {"from": "D", "to": "n", "type": "KAN_INFLECTED", "has_kan": True, "kan_swara": "S'"},
            {"from": "n", "to": "D", "type": "MEEND_SIGMOID", "has_kan": False},
        ],
    }

    # 7. Raga Hamir: "Madhuban Mein Radhika Nache Re"
    hamir_notes = [
        {"note": "A4", "sargam": "P", "cents": 700.0, "start_time": 0.0, "end_time": 0.35, "syllable": "Ma-"},
        {"note": "G#4", "sargam": "M", "cents": 600.0, "start_time": 0.50, "end_time": 0.80, "syllable": "dhu-"},
        {"note": "A4", "sargam": "P", "cents": 700.0, "start_time": 1.00, "end_time": 1.35, "syllable": "ban"},
        {"note": "F#4", "sargam": "G", "cents": 400.0, "start_time": 1.55, "end_time": 1.90, "syllable": "mein"},
        {"note": "G4", "sargam": "m", "cents": 500.0, "start_time": 2.10, "end_time": 2.45, "syllable": "Ra-"},
        {"note": "E4", "sargam": "R", "cents": 200.0, "start_time": 2.65, "end_time": 3.00, "syllable": "dhi-"},
        {"note": "D4", "sargam": "S", "cents": 0.0, "start_time": 3.20, "end_time": 3.65, "syllable": "ka"},
    ]

    t_hamir = np.linspace(0.0, 3.7, 371)
    c_hamir = np.zeros_like(t_hamir)
    for i, t in enumerate(t_hamir):
        if t < 0.35:
            c_hamir[i] = 700.0
        elif 0.35 <= t < 0.50:
            u = (t - 0.35) / 0.15
            c_hamir[i] = 700.0 - 100.0 * (u ** 2)
        elif 0.50 <= t < 0.80:
            c_hamir[i] = 600.0
        elif 0.80 <= t < 1.00:
            u = (t - 0.80) / 0.20
            c_hamir[i] = 600.0 + 100.0 * (u ** 3) # Scoop back into Pa
        elif 1.00 <= t < 1.35:
            c_hamir[i] = 700.0
        elif 1.35 <= t < 1.55:
            u = (t - 1.35) / 0.20
            c_hamir[i] = 700.0 - 300.0 / (1.0 + np.exp(-14.0 * (u - 0.5))) # S-curve glide Pa -> Ga
        elif 1.55 <= t < 1.90:
            c_hamir[i] = 400.0
        elif 1.90 <= t < 2.10:
            # Kan touch of Pa (700) then resolve down to Ma (500)
            u = (t - 1.90) / 0.20
            if u < 0.50:
                v = u / 0.50
                c_hamir[i] = 400.0 + 300.0 / (1.0 + np.exp(-14.0 * (v - 0.5))) # Touch Pa
            else:
                w = (u - 0.50) / 0.50
                c_hamir[i] = 700.0 - 200.0 / (1.0 + np.exp(-14.0 * (w - 0.5))) # Land Ma
        elif 2.10 <= t < 2.45:
            c_hamir[i] = 500.0
        elif 2.45 <= t < 2.65:
            u = (t - 2.45) / 0.20
            c_hamir[i] = 500.0 - 300.0 * (u ** 3) # Scoop down to Re
        elif 2.65 <= t < 3.00:
            c_hamir[i] = 200.0
        elif 3.00 <= t < 3.20:
            u = (t - 3.00) / 0.20
            c_hamir[i] = 200.0 - 200.0 / (1.0 + np.exp(-14.0 * (u - 0.5))) # S-curve to Sa
        else:
            c_hamir[i] = 0.0

    corpus["hamir_madhuban"] = {
        "title": "Madhuban Mein Radhika (Raga Hamir)",
        "raga": "Hamir",
        "tonic_hz": 146.83,
        "notes": hamir_notes,
        "times": t_hamir,
        "cents": c_hamir,
        "ground_truth_transitions": [
            {"from": "P", "to": "M", "type": "MEEND_CONCAVE_SLIDE", "has_kan": False},
            {"from": "M", "to": "P", "type": "MEEND_CONVEX_SCOOP", "has_kan": False},
            {"from": "P", "to": "G", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "G", "to": "m", "type": "KAN_INFLECTED", "has_kan": True, "kan_swara": "P"},
            {"from": "m", "to": "R", "type": "MEEND_CONVEX_SCOOP", "has_kan": False},
            {"from": "R", "to": "S", "type": "MEEND_SIGMOID", "has_kan": False},
        ],
    }

    # 8. Raga Sohini: "Kuhu Kuhu Bole Koyaliya"
    sohini_notes = [
        {"note": "D4", "sargam": "S", "cents": 0.0, "start_time": 0.0, "end_time": 0.35, "syllable": "Ku-"},
        {"note": "F#4", "sargam": "G", "cents": 400.0, "start_time": 0.55, "end_time": 0.90, "syllable": "hu"},
        {"note": "G#4", "sargam": "M", "cents": 600.0, "start_time": 1.10, "end_time": 1.45, "syllable": "ku-"},
        {"note": "B4", "sargam": "D", "cents": 900.0, "start_time": 1.65, "end_time": 2.00, "syllable": "hu"},
        {"note": "C#5", "sargam": "N", "cents": 1100.0, "start_time": 2.20, "end_time": 2.55, "syllable": "bo-"},
        {"note": "D5", "sargam": "S'", "cents": 1200.0, "start_time": 2.75, "end_time": 3.10, "syllable": "le"},
        {"note": "C#5", "sargam": "N", "cents": 1100.0, "start_time": 3.35, "end_time": 3.70, "syllable": "ko-"},
        {"note": "B4", "sargam": "D", "cents": 900.0, "start_time": 3.90, "end_time": 4.25, "syllable": "ya-"},
        {"note": "G#4", "sargam": "M", "cents": 600.0, "start_time": 4.45, "end_time": 4.80, "syllable": "li-"},
        {"note": "F#4", "sargam": "G", "cents": 400.0, "start_time": 5.00, "end_time": 5.45, "syllable": "ya"},
    ]

    t_sohini = np.linspace(0.0, 5.5, 551)
    c_sohini = np.zeros_like(t_sohini)
    for i, t in enumerate(t_sohini):
        if t < 0.35:
            c_sohini[i] = 0.0
        elif 0.35 <= t < 0.55:
            u = (t - 0.35) / 0.20
            c_sohini[i] = 400.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 0.55 <= t < 0.90:
            c_sohini[i] = 400.0
        elif 0.90 <= t < 1.10:
            u = (t - 0.90) / 0.20
            c_sohini[i] = 400.0 + 200.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 1.10 <= t < 1.45:
            c_sohini[i] = 600.0
        elif 1.45 <= t < 1.65:
            u = (t - 1.45) / 0.20
            c_sohini[i] = 600.0 + 300.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 1.65 <= t < 2.00:
            c_sohini[i] = 900.0
        elif 2.00 <= t < 2.20:
            u = (t - 2.00) / 0.20
            c_sohini[i] = 900.0 + 200.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 2.20 <= t < 2.55:
            c_sohini[i] = 1100.0
        elif 2.55 <= t < 2.75:
            u = (t - 2.55) / 0.20
            c_sohini[i] = 1100.0 + 100.0 * np.sqrt(max(0.0, u)) # Concave float landing on Taar Sa
        elif 2.75 <= t < 3.10:
            c_sohini[i] = 1200.0
        elif 3.10 <= t < 3.35:
            # Kan touch of Taar Re (1400c) then resolve down to Ni (1100c)
            u = (t - 3.10) / 0.25
            if u < 0.45:
                v = u / 0.45
                c_sohini[i] = 1200.0 + 200.0 / (1.0 + np.exp(-14.0 * (v - 0.5)))
            else:
                w = (u - 0.45) / 0.55
                c_sohini[i] = 1400.0 - 300.0 / (1.0 + np.exp(-14.0 * (w - 0.5)))
        elif 3.35 <= t < 3.70:
            c_sohini[i] = 1100.0
        elif 3.70 <= t < 3.90:
            # Murki turn: 1100c -> 1200c -> 1100c -> 900c
            u = (t - 3.70) / 0.20
            c_sohini[i] = 1000.0 + 100.0 * np.sin(2.0 * np.pi * u)
        elif 3.90 <= t < 4.25:
            c_sohini[i] = 900.0
        elif 4.25 <= t < 4.45:
            u = (t - 4.25) / 0.20
            c_sohini[i] = 900.0 - 300.0 / (1.0 + np.exp(-14.0 * (u - 0.5)))
        elif 4.45 <= t < 4.80:
            c_sohini[i] = 600.0
        elif 4.80 <= t < 5.00:
            u = (t - 4.80) / 0.20
            c_sohini[i] = 600.0 - 200.0 * (u ** 3) # Scoop into Ga
        else:
            c_sohini[i] = 400.0

    corpus["sohini_kuhu_kuhu"] = {
        "title": "Kuhu Kuhu Bole Koyaliya (Raga Sohini)",
        "raga": "Sohini",
        "tonic_hz": 146.83,
        "notes": sohini_notes,
        "times": t_sohini,
        "cents": c_sohini,
        "ground_truth_transitions": [
            {"from": "S", "to": "G", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "G", "to": "M", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "M", "to": "D", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "D", "to": "N", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "N", "to": "S'", "type": "MEEND_CONCAVE_SLIDE", "has_kan": False},
            {"from": "S'", "to": "N", "type": "KAN_INFLECTED", "has_kan": True, "kan_swara": "R'"},
            {"from": "N", "to": "D", "type": "MURKI_TURN", "has_kan": False},
            {"from": "D", "to": "M", "type": "MEEND_SIGMOID", "has_kan": False},
            {"from": "M", "to": "G", "type": "MEEND_CONVEX_SCOOP", "has_kan": False},
        ],
    }
'''

code = code.replace('    return corpus', additions + '\n    return corpus')

with open(corpus_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Expanded hindi_songs_benchmark_corpus.py to 8 iconic songs!")
