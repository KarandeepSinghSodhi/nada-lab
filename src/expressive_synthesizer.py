"""
Expressive Meend & Continuous Pitch Trajectory Generative Synthesizer
Inspired by Diffusion & Flow-Matching Pitch Curve Models (ConTuner, StylePitcher)
Implements physics-informed sigmoidal meend flow splines and microtonal andolan oscillators.
"""

import math
import io
import wave
import base64
from typing import List, Dict, Any


SWARA_CENTS_MAP = {
    "S": 0.0, "Sa": 0.0,
    "r": 111.7, "Komal Re": 111.7, "k-Re": 111.7,
    "R": 203.9, "Re": 203.9, "Shuddha Re": 203.9,
    "g": 315.6, "Komal Ga": 315.6, "k-Ga": 315.6,
    "G": 386.3, "Ga": 386.3, "Shuddha Ga": 386.3,
    "m": 498.0, "Ma": 498.0, "Shuddha Ma": 498.0,
    "M": 590.2, "Tivra Ma": 590.2, "t-Ma": 590.2,
    "P": 702.0, "Pa": 702.0,
    "d": 813.7, "Komal Dha": 813.7, "k-Dha": 813.7,
    "D": 905.9, "Dha": 905.9, "Shuddha Dha": 905.9,
    "n": 1017.6, "Komal Ni": 1017.6, "k-Ni": 1017.6,
    "N": 1088.3, "Ni": 1088.3, "Shuddha Ni": 1088.3,
    "S'": 1200.0, "Taar Sa": 1200.0, "S+": 1200.0
}


class ExpressiveMeendSynthesizer:
    """Generates continuous microtonal pitch trajectories with authentic gayaki dynamics."""

    @staticmethod
    def parse_note_cents(note: str) -> float:
        cleaned = note.strip()
        if cleaned in SWARA_CENTS_MAP:
            return SWARA_CENTS_MAP[cleaned]
        # Octave shift handling (e.g. S- for Mandra, S+ for Taar)
        if cleaned.endswith("-"):
            base = cleaned[:-1]
            return SWARA_CENTS_MAP.get(base, 0.0) - 1200.0
        if cleaned.endswith("+") or cleaned.endswith("'"):
            base = cleaned[:-1]
            return SWARA_CENTS_MAP.get(base, 0.0) + 1200.0
        return 0.0

    @classmethod
    def generate_trajectory(
        cls,
        notes: List[str],
        raga: str = "Yaman",
        tonic_hz: float = 146.83,
        tempo_bpm: float = 60.0,
        meend_expressiveness: float = 0.85
    ) -> Dict[str, Any]:
        """
        Synthesizes a continuous 100 Hz pitch trajectory from a discrete note sequence.
        """
        if not notes:
            notes = ["Sa", "Re", "Ga", "Pa"]

        # Parse target cents for each note
        note_targets = [cls.parse_note_cents(n) for n in notes]
        num_notes = len(note_targets)

        # Compute durations based on tempo
        sec_per_beat = 60.0 / max(30.0, min(180.0, tempo_bpm))
        note_duration = sec_per_beat * 1.2
        total_duration = num_notes * note_duration

        # 100 Hz frame rate (10 ms hop)
        fps = 100
        total_frames = int(total_duration * fps)
        frames_per_note = int(note_duration * fps)

        trajectory = []
        c_prev = note_targets[0]

        for i in range(total_frames):
            t = i / fps
            note_idx = min(num_notes - 1, int(t / note_duration))
            local_t = (t - note_idx * note_duration) / note_duration # 0.0 to 1.0 within the note

            c_target = note_targets[note_idx]
            c_start = note_targets[note_idx - 1] if note_idx > 0 else c_target

            # 1. Sigmoidal Meend Transition Spline
            # meend_expressiveness governs glide duration vs. steady dwell
            glide_ratio = 0.15 + (meend_expressiveness * 0.45) # 15% to 60% of beat is glide
            k = 12.0 # Curvature steepness

            if local_t < glide_ratio and note_idx > 0:
                # Gliding from previous note to target
                norm_u = local_t / glide_ratio
                sigmoid_val = 1.0 / (1.0 + math.exp(-k * (norm_u - 0.5)))
                c_base = c_start + (c_target - c_start) * sigmoid_val
            else:
                c_base = c_target

            # 2. Microtonal Andolan Oscillation for characteristic swaras
            andolan_cent = 0.0
            raga_lower = raga.lower()

            # Darbari Komal Ga (316c) or Komal Dha (814c) slow heavy andolan
            if "darbari" in raga_lower and (abs(c_target - 315.6) < 30.0 or abs(c_target - 813.7) < 30.0):
                if local_t >= glide_ratio:
                    osc_freq = 2.1 # Hz
                    andolan_cent = 24.0 * math.sin(2.0 * math.pi * osc_freq * (t - glide_ratio * note_duration))
            # Bhairav Komal Re (112c) or Komal Dha (814c) oscillatory suspension
            elif "bhairav" in raga_lower and (abs(c_target - 111.7) < 30.0 or abs(c_target - 813.7) < 30.0):
                if local_t >= glide_ratio:
                    osc_freq = 1.9 # Hz
                    andolan_cent = 18.0 * math.sin(2.0 * math.pi * osc_freq * t)

            c_total = c_base + andolan_cent
            freq = tonic_hz * math.pow(2.0, c_total / 1200.0)

            # Compute kinematic derivative (velocity in cents/sec)
            velocity = (c_total - c_prev) * fps if i > 0 else 0.0
            c_prev = c_total

            trajectory.append({
                "t": round(t, 3),
                "cents": round(c_total, 2),
                "hz": round(freq, 2),
                "velocity": round(velocity, 1)
            })

        # Synthesize audio preview (44.1 kHz 16-bit mono WAV)
        audio_b64 = cls._synthesize_wav(trajectory, total_duration)

        return {
            "raga": raga,
            "tonic_hz": tonic_hz,
            "tempo_bpm": tempo_bpm,
            "meend_expressiveness": meend_expressiveness,
            "notes_parsed": notes,
            "duration_sec": round(total_duration, 2),
            "trajectory_points": len(trajectory),
            "pitch_trajectory": trajectory,
            "audio_wav_base64": audio_b64
        }

    @staticmethod
    def _synthesize_wav(trajectory: List[Dict[str, Any]], duration: float) -> str:
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        audio_data = bytearray()

        phase = 0.0
        fps = 100

        for s in range(num_samples):
            t = s / sample_rate
            frame_idx = min(len(trajectory) - 1, int(t * fps))
            freq = trajectory[frame_idx]["hz"]

            phase += 2.0 * math.pi * freq / sample_rate
            if phase > 2.0 * math.pi:
                phase -= 2.0 * math.pi

            # Dual-formant vocal tone (fundamental + 2nd + 3rd harmonic)
            sample = (
                0.60 * math.sin(phase) +
                0.28 * math.sin(phase * 2.0) +
                0.12 * math.sin(phase * 3.0)
            )

            # Envelope tapering at start and end
            env = 1.0
            if t < 0.04:
                env = t / 0.04
            elif t > duration - 0.06:
                env = max(0.0, (duration - t) / 0.06)

            val = int(sample * env * 16000)
            val = max(-32767, min(32767, val))
            audio_data.extend(val.to_bytes(2, byteorder="little", signed=True))

        # Write WAV buffer
        wav_io = io.BytesIO()
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data)

        return base64.b64encode(wav_io.getvalue()).decode("ascii")
