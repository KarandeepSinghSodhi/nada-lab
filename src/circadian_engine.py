"""
Circadian Samay Chakra & Neuro-Acoustic Bio-Clock Engine
Implements Indian Classical Music Chronobiology & Prahara Theory
Coupled with Neuro-Endocrine Circadian Phases (Cortisol, Melatonin, Autonomic Tone)
"""

from typing import Dict, Any, List
from datetime import datetime


PRAHARA_REGISTRY = [
    {
        "prahara_num": 1,
        "name": "Pratham Prahara (Dawn / Pratahkal)",
        "sanskrit": "प्रथम प्रहर (प्रातःकाल)",
        "start_hour": 6,
        "end_hour": 9,
        "biological_phase": "Cortisol Awakening Response (CAR) & Parasympathetic-to-Sympathetic Transition",
        "neuro_correlates": "Alpha-wave stabilization, awakening focus, baseline heart rate rise.",
        "primary_raga": "Bhairav",
        "allied_ragas": ["Ahir Bhairav", "Ramkali", "Gunakri", "Nat Bhairav"],
        "acoustic_rationale": "Komal Re (112c) and Komal Dha (814c) provide solemn microtonal grounding, easing neural awakening without sensory shock.",
        "drone_tuning": "pa",
        "target_valence": -0.45,
        "target_arousal": -0.20,
        "dominant_rasa": "Shanta / Karuna (Ascetic Stillness & Devotion)"
    },
    {
        "prahara_num": 2,
        "name": "Dwitiya Prahara (Morning / Madhyahna-Purva)",
        "sanskrit": "द्वितीय प्रहर (पूर्वाह्न)",
        "start_hour": 9,
        "end_hour": 12,
        "biological_phase": "Peak Cognitive Vigilance & Dopaminergic Concentration",
        "neuro_correlates": "Beta-wave elevation, working memory optimization, high executive focus.",
        "primary_raga": "Todi",
        "allied_ragas": ["Jaunpuri", "Alhaiya Bilawal", "Bilasakhani Todi", "Deshkar"],
        "acoustic_rationale": "Sharp ascending intervals and Tivra Ma / Komal Ga tension stimulate active alertness and intellectual vigor.",
        "drone_tuning": "pa",
        "target_valence": 0.35,
        "target_arousal": 0.40,
        "dominant_rasa": "Veera / Utsaha (Energy & Purposeful Focus)"
    },
    {
        "prahara_num": 3,
        "name": "Tritiya Prahara (Midday / Madhyahna)",
        "sanskrit": "तृतीय प्रहर (मध्याह्न)",
        "start_hour": 12,
        "end_hour": 15,
        "biological_phase": "Solar Zenith & Metabolic Culmination",
        "neuro_correlates": "Sympathetic stabilization, high body temperature, balanced mental equilibrium.",
        "primary_raga": "Shuddha Sarang",
        "allied_ragas": ["Madhmad Sarang", "Gaud Sarang", "Brindavani Sarang", "Bhimpalasi"],
        "acoustic_rationale": "Dual Madhyams (Shuddha and Tivra Ma) mirror the transition from morning ascendancy to afternoon declination.",
        "drone_tuning": "pa",
        "target_valence": 0.50,
        "target_arousal": 0.10,
        "dominant_rasa": "Gambhirya / Shanta (Majestic Balance)"
    },
    {
        "prahara_num": 4,
        "name": "Chaturtha Prahara (Late Afternoon / Aparahna)",
        "sanskrit": "चतुर्थ प्रहर (अपराह्न)",
        "start_hour": 15,
        "end_hour": 18,
        "biological_phase": "Post-Prandial Relaxation & Gradual Sympathetic De-escalation",
        "neuro_correlates": "Mild cognitive deceleration, emotional receptivity, sensorimotor soothing.",
        "primary_raga": "Bhimpalasi",
        "allied_ragas": ["Multani", "Patdeep", "Pilu", "Dhani"],
        "acoustic_rationale": "Soft Komal Ga (316c) and Komal Ni (1018c) in avaroha create tender release from midday fatigue.",
        "drone_tuning": "pa",
        "target_valence": 0.20,
        "target_arousal": -0.15,
        "dominant_rasa": "Shringara / Karuna (Tender Longing & Warmth)"
    },
    {
        "prahara_num": 5,
        "name": "Panchama Prahara (Sandhiprakash / Twilight)",
        "sanskrit": "पञ्चम प्रहर (सन्धिप्रकाश / गोधूलि)",
        "start_hour": 18,
        "end_hour": 21,
        "biological_phase": "Circadian Twilight Transition & Pineal Melatonin Onset",
        "neuro_correlates": "Shift toward parasympathetic dominance, release of diurnal cortisol.",
        "primary_raga": "Marwa",
        "allied_ragas": ["Puriya", "Purvi", "Shree", "Yaman"],
        "acoustic_rationale": "Tivra Ma (45/32, 590c) and Komal Re (112c) without Pancham create intense threshold tension, reflecting day-night dusk.",
        "drone_tuning": "ni",
        "target_valence": -0.30,
        "target_arousal": 0.25,
        "dominant_rasa": "Adbhuta / Sandhiprakash (Twilight Mystery & Intensity)"
    },
    {
        "prahara_num": 6,
        "name": "Shashtha Prahara (Early Night / Ratri Prathama)",
        "sanskrit": "षष्ठ प्रहर (रात्रि प्रथम प्रहर)",
        "start_hour": 21,
        "end_hour": 24,
        "biological_phase": "Melatonin Surge, Core Temperature Drop & Serotonergic Peace",
        "neuro_correlates": "Alpha/Theta wave emergence, emotional contentment, profound sensory soothing.",
        "primary_raga": "Yaman",
        "allied_ragas": ["Bihag", "Bageshri", "Khamaj", "Kafi", "Jaijaiwanti"],
        "acoustic_rationale": "Luminous Shuddha Ga (5/4) and Shuddha Ni (15/8) anchor into the unceasing Sa-Pa drone, inducing nocturnal serenity.",
        "drone_tuning": "pa",
        "target_valence": 0.75,
        "target_arousal": -0.30,
        "dominant_rasa": "Shanta / Shringara (Nocturnal Peace & Devotion)"
    },
    {
        "prahara_num": 7,
        "name": "Saptama Prahara (Midnight / Nishitha)",
        "sanskrit": "सप्तम प्रहर (निशीथ / मध्यरात्रि)",
        "start_hour": 0,
        "end_hour": 3,
        "biological_phase": "Slow-Wave Deep Sleep (Delta Brainwaves) & Cellular Regeneration",
        "neuro_correlates": "High parasympathetic tone, heart rate nadir, profound subconscious introspection.",
        "primary_raga": "Darbari Kanada",
        "allied_ragas": ["Malkauns", "Chandrakauns", "Adana", "Shahana"],
        "acoustic_rationale": "Heavy Mandra Saptak resonance and slow, deliberate Komal Ga/Dha oscillations (1.8-2.4 Hz) produce deep meditative immersion.",
        "drone_tuning": "ma",
        "target_valence": -0.25,
        "target_arousal": -0.60,
        "dominant_rasa": "Karuna / Gambhirya (Midnight Majesty & Trance)"
    },
    {
        "prahara_num": 8,
        "name": "Ashtama Prahara (Brahma Muhurta / Pre-Dawn)",
        "sanskrit": "अष्टम प्रहर (ब्रह्म मुहूर्त / उषाकाल)",
        "start_hour": 3,
        "end_hour": 6,
        "biological_phase": "Circadian Biological Reset & Pre-Awakening Neural Clarity",
        "neuro_correlates": "Theta-Alpha border, highest meditative receptivity, lowest auditory noise floor.",
        "primary_raga": "Bhairavi",
        "allied_ragas": ["Lalit", "Sohini", "Bhatiyar", "Paraj"],
        "acoustic_rationale": "Both Shuddha and Komal variants of Re, Ga, Dha, Ni unlock universal modal fluidity before the sun rises.",
        "drone_tuning": "pa",
        "target_valence": 0.10,
        "target_arousal": -0.40,
        "dominant_rasa": "Bhakti / Shanta (Universal Sacred Devotion)"
    }
]


class CircadianRagaEngine:
    """Evaluates time-of-day prahara and chronobiological raga recommendation."""

    @staticmethod
    def get_circadian_recommendation(hour: int = None, minute: int = 0) -> Dict[str, Any]:
        if hour is None:
            now = datetime.now()
            hour = now.hour
            minute = now.minute

        # Determine Prahara
        matching_prahara = None
        for p in PRAHARA_REGISTRY:
            s = p["start_hour"]
            e = p["end_hour"]
            if s < e:
                if s <= hour < e:
                    matching_prahara = p
                    break
            else:
                # Wraps midnight (e.g. 21 to 24 or 0 to 3)
                if hour >= s or hour < e:
                    matching_prahara = p
                    break

        if not matching_prahara:
            matching_prahara = PRAHARA_REGISTRY[5] # Default to early night

        time_str = f"{hour:02d}:{minute:02d}"

        return {
            "query_time": time_str,
            "prahara_number": matching_prahara["prahara_num"],
            "prahara_name": matching_prahara["name"],
            "sanskrit_name": matching_prahara["sanskrit"],
            "window": f"{matching_prahara['start_hour']:02d}:00 - {matching_prahara['end_hour']:02d}:00",
            "biological_phase": matching_prahara["biological_phase"],
            "neuro_correlates": matching_prahara["neuro_correlates"],
            "recommended_raga": matching_prahara["primary_raga"],
            "allied_ragas": matching_prahara["allied_ragas"],
            "acoustic_rationale": matching_prahara["acoustic_rationale"],
            "drone_tuning": matching_prahara["drone_tuning"],
            "target_valence": matching_prahara["target_valence"],
            "target_arousal": matching_prahara["target_arousal"],
            "dominant_rasa": matching_prahara["dominant_rasa"]
        }
