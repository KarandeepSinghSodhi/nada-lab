"""
High-Resolution 14-Bit Pitch Bend MIDI & Canonical Sargam Formatter for Song Lab.
Exports:
1. Pure binary MIDI Standard Format 0 with continuous 100 Hz 14-bit pitch bend messages (+/- 12 semitones).
2. Standardized Bhatkhande Sargam notation with Unicode diacritics and Devanagari characters.
"""

import io
import math
import struct
from typing import Dict, List, Optional, Tuple
import numpy as np

from src.tonal_engine import SHRUTI_TABLE, quantize_to_12_swara, quantize_to_shruti


SWARA_TO_DEVANAGARI = {
    "S": "सा",
    "r": "रे॒",
    "R": "रे",
    "g": "ग॒",
    "G": "ग",
    "m": "म",
    "M": "म॑",
    "P": "प",
    "d": "ध॒",
    "D": "ध",
    "n": "नि॒",
    "N": "नि",
}

SWARA_TO_BHATKHANDE = {
    "S": "S",
    "r": "r",
    "R": "R",
    "g": "g",
    "G": "G",
    "m": "M",
    "M": "M'",
    "P": "P",
    "d": "d",
    "D": "D",
    "n": "n",
    "N": "N",
}


def encode_varlen(val: int) -> bytes:
    """Encodes an integer into MIDI variable-length quantity bytes."""
    buf = []
    buf.append(val & 0x7F)
    val >>= 7
    while val > 0:
        buf.append((val & 0x7F) | 0x80)
        val >>= 7
    buf.reverse()
    return bytes(buf)


class MidiSargamExporter:
    """
    Exports high-resolution pitch bend MIDI and classical Sargam notation.
    """

    @staticmethod
    def format_sargam_note(cents: float) -> Dict:
        """
        Formats a continuous pitch point in cents into authentic Sargam notation.
        """
        sw_dict, err, oct_shift = quantize_to_12_swara(cents)
        sym = sw_dict["symbol"]
        is_komal = sym in ["r", "g", "d", "n"]
        is_tivra = sym == "M"

        # Determine Octave Diacritic
        # Octave -1: Mandra (dot below), 0: Madhya, +1: Taar (dot above)
        if oct_shift > 0:
            oct_label = "Taar (Upper Octave)"
            bhatkhande_sym = sym.upper() + "\u0307"  # Combining dot above
            devanagari_sym = SWARA_TO_DEVANAGARI.get(sym, "सा") + "\u0307"
        elif oct_shift < 0:
            oct_label = "Mandra (Lower Octave)"
            bhatkhande_sym = sym.upper() + "\u0323"  # Combining dot below
            devanagari_sym = SWARA_TO_DEVANAGARI.get(sym, "सा") + "\u0323"
        else:
            oct_label = "Madhya (Middle Octave)"
            bhatkhande_sym = SWARA_TO_BHATKHANDE.get(sym, sym)
            devanagari_sym = SWARA_TO_DEVANAGARI.get(sym, "सा")

        shruti_obj, shruti_err, _ = quantize_to_shruti(cents)

        return {
            "cents": round(float(cents), 1),
            "symbol": sym,
            "bhatkhande_sargam": bhatkhande_sym,
            "devanagari": devanagari_sym,
            "octave": oct_label,
            "shruti_name": shruti_obj.swara_hindustani,
            "shruti_ratio": f"{shruti_obj.ratio_num}/{shruti_obj.ratio_den}",
            "shruti_cents": shruti_obj.cents,
            "error_from_pure_shruti": round(float(shruti_err), 1),
            "is_komal": is_komal,
            "is_tivra": is_tivra,
        }

    @staticmethod
    def trajectory_to_sargam_transcript(
        cents_trajectory: List[float],
        hop_sec: float = 0.05,
        min_dur_sec: float = 0.0,
    ) -> List[Dict]:
        """
        Converts a continuous pitch trajectory into a sequence of articulated Sargam notes
        with duration and ornament tags.
        """
        if not cents_trajectory:
            return []

        transcript = []
        current_swara = None
        current_info = None
        start_t = 0.0
        dwell_frames = 0

        for i, c in enumerate(cents_trajectory):
            t = i * hop_sec
            if c is None or math.isnan(c):
                continue

            info = MidiSargamExporter.format_sargam_note(c)
            sw = info["symbol"]

            if current_swara is None:
                current_swara = sw
                current_info = info
                start_t = t
                dwell_frames = 1
            elif sw == current_swara:
                dwell_frames += 1
            else:
                dur = round(dwell_frames * hop_sec, 2)
                if dur >= min_dur_sec:
                    transcript.append({
                        "swara": current_swara,
                        "bhatkhande": current_info["bhatkhande_sargam"] if current_info else current_swara,
                        "devanagari": current_info["devanagari"] if current_info else SWARA_TO_DEVANAGARI.get(current_swara, "सा"),
                        "start_sec": round(start_t, 2),
                        "duration_sec": dur,
                    })
                current_swara = sw
                current_info = info
                start_t = t
                dwell_frames = 1

        if current_swara and dwell_frames > 0:
            dur = round(dwell_frames * hop_sec, 2)
            if dur >= min_dur_sec:
                transcript.append({
                    "swara": current_swara,
                    "bhatkhande": current_info["bhatkhande_sargam"] if current_info else current_swara,
                    "devanagari": current_info["devanagari"] if current_info else SWARA_TO_DEVANAGARI.get(current_swara, "सा"),
                    "start_sec": round(start_t, 2),
                    "duration_sec": dur,
                })

        return transcript

    @staticmethod
    def generate_pitch_bend_midi(
        cents_trajectory: List[float],
        sa_midi_note: int = 60,  # Middle C = 60
        hop_sec: float = 0.01,
        max_bend_semitones: int = 12,
        tempo_bpm: int = 84,
    ) -> bytes:
        """
        Generates standard Format 0 MIDI bytes with continuous 14-bit pitch bend events
        reflecting authentic continuous Meends and Andolans.
        """
        ticks_per_quarter = 480
        sec_per_tick = 60.0 / (tempo_bpm * ticks_per_quarter)
        ticks_per_frame = max(1, int(round(hop_sec / sec_per_tick)))

        events = bytearray()
        
        # Meta Event: Set Tempo
        tempo_us = int(60_000_000 / tempo_bpm)
        events.extend(b"\x00\xFF\x51\x03" + struct.pack(">I", tempo_us)[1:])

        # Note On event for base root anchor note (Sa)
        # Channel 0, Note, Velocity 96
        events.extend(b"\x00\x90" + bytes([sa_midi_note, 96]))

        last_bend = 8192
        max_cents = max_bend_semitones * 100.0

        for i, c in enumerate(cents_trajectory):
            delta_ticks = ticks_per_frame
            if c is None or math.isnan(c):
                c = 0.0

            # Compute 14-bit pitch bend: [0, 16383], 8192 = center
            clamped_cents = max(-max_cents, min(max_cents, float(c)))
            bend_val = int(round(8192 + (clamped_cents / max_cents) * 8191))
            bend_val = max(0, min(16383, bend_val))

            if bend_val != last_bend or i == 0:
                lsb = bend_val & 0x7F
                msb = (bend_val >> 7) & 0x7F
                events.extend(encode_varlen(delta_ticks) + bytes([0xE0, lsb, msb]))
                last_bend = bend_val
            else:
                # Accumulate delta time
                pass

        # Note Off event for base root
        events.extend(encode_varlen(ticks_per_frame) + bytes([0x80, sa_midi_note, 0]))
        # End of Track Meta Event
        events.extend(b"\x00\xFF\x2F\x00")

        # Construct MIDI file Header chunk and Track chunk
        header_chunk = b"MThd" + struct.pack(">IHHH", 6, 0, 1, ticks_per_quarter)
        track_chunk = b"MTrk" + struct.pack(">I", len(events)) + events

        return header_chunk + track_chunk
