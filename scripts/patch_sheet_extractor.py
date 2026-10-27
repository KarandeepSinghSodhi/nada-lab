from pathlib import Path

path = Path("src/sheet_music_extractor.py")
content = path.read_text(encoding="utf-8")

old_sig = """    @classmethod
    def extract_sheet_music(
        cls,
        notations: List[Dict[str, Any]],
        lyrics_text: Optional[str] = None,
        tempo_bpm: float = 84.0,
        tonic_hz: float = 146.83,
        phrase_key: Optional[str] = None,
        instrument: str = "piano"
    ) -> Dict[str, Any]:"""

new_sig = """    @classmethod
    def extract_sheet_music(
        cls,
        notations: List[Dict[str, Any]],
        lyrics_text: Optional[str] = None,
        tempo_bpm: float = 84.0,
        tonic_hz: float = 146.83,
        phrase_key: Optional[str] = None,
        instrument: str = "piano",
        in_between_transitions: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:"""

old_ev = """            event = SheetMusicEvent(
                syllable=syl,
                note_western=western,
                note_sargam=sargam,
                frequency_hz=round(freq, 1),
                start_time=round(start_t, 3),
                end_time=round(end_t, 3),
                duration_ms=round(dur_ms, 1),
                rhythm_symbol=rhythm_sym,
                rhythm_name=rhythm_name,
                measure_index=measure_idx,
                beat_in_measure=beat_in_measure,
                guitar_tab=guitar_tab,
                flute_fingering=flute_holes,
                piano_key=midi_num
            )"""

new_ev = """            transition_to_next = None
            if in_between_transitions and idx < len(in_between_transitions):
                transition_to_next = in_between_transitions[idx]

            event = SheetMusicEvent(
                syllable=syl,
                note_western=western,
                note_sargam=sargam,
                frequency_hz=round(freq, 1),
                start_time=round(start_t, 3),
                end_time=round(end_t, 3),
                duration_ms=round(dur_ms, 1),
                rhythm_symbol=rhythm_sym,
                rhythm_name=rhythm_name,
                measure_index=measure_idx,
                beat_in_measure=beat_in_measure,
                guitar_tab=guitar_tab,
                flute_fingering=flute_holes,
                piano_key=midi_num,
                in_between_transition=transition_to_next,
            )"""

content_norm = content.replace("\r\n", "\n")
old_sig_norm = old_sig.replace("\r\n", "\n")
new_sig_norm = new_sig.replace("\r\n", "\n")
old_ev_norm = old_ev.replace("\r\n", "\n")
new_ev_norm = new_ev.replace("\r\n", "\n")

if old_sig_norm in content_norm and old_ev_norm in content_norm:
    content_norm = content_norm.replace(old_sig_norm, new_sig_norm, 1)
    content_norm = content_norm.replace(old_ev_norm, new_ev_norm, 1)
    # Convert back to crlf
    path.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
    print("SUCCESS: Patched src/sheet_music_extractor.py")
else:
    print("ERROR: Signatures not found!")
