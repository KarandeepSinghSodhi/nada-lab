import re

with open('src/sheet_music_extractor.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize CRLF to LF for consistent handling
text = text.replace('\r\n', '\n')

code_to_append = '''
    @staticmethod
    def _escape_xml(s: str) -> str:
        return (str(s)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    @classmethod
    def export_musicxml(cls, sheet_data: Dict[str, Any]) -> str:
        """
        Serializes lead sheet structure into standard MusicXML 3.1 format.
        Compatible with MuseScore, Sibelius, Finale, Dorico, and Soundslice.
        """
        title = sheet_data.get("title", "Song Lab Lead Sheet")
        tempo = sheet_data.get("tempo_bpm", 84.0)
        measures = sheet_data.get("measures", [])

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">',
            '<score-partwise version="3.1">',
            '  <work>',
            f'    <work-title>{cls._escape_xml(title)}</work-title>',
            '  </work>',
            '  <identification>',
            '    <creator type="composer">Song Lab AI Musicology</creator>',
            '    <encoding>',
            '      <software>Song Lab MusicXML Exporter v2.0</software>',
            '    </encoding>',
            '  </identification>',
            '  <part-list>',
            '    <score-part id="P1">',
            f'      <part-name>{cls._escape_xml(sheet_data.get("instrument", "Lead Voice").title())}</part-name>',
            '    </score-part>',
            '  </part-list>',
            '  <part id="P1">'
        ]

        DIVISIONS = 4
        type_to_divs = {
            "whole": 16,
            "half": 8,
            "quarter": 4,
            "eighth": 2,
            "16th": 1
        }

        for m_idx, m in enumerate(measures):
            m_num = m.get("measure_number", m_idx + 1)
            lines.append(f'    <measure number="{m_num}">')

            if m_idx == 0:
                lines.extend([
                    '      <attributes>',
                    f'        <divisions>{DIVISIONS}</divisions>',
                    '        <key>',
                    '          <fifths>0</fifths>',
                    '        </key>',
                    '        <time>',
                    '          <beats>4</beats>',
                    '          <beat-type>4</beat-type>',
                    '        </time>',
                    '        <clef>',
                    '          <sign>G</sign>',
                    '          <line>2</line>',
                    '        </clef>',
                    '      </attributes>',
                    '      <direction placement="above">',
                    f'        <sound tempo="{round(tempo)}"/>',
                    '      </direction>'
                ])

            chord = m.get("chord", "")
            if chord:
                root_step = chord[0].upper()
                alter = 0
                kind = "major"
                rem = chord[1:]
                if rem.startswith("#"):
                    alter = 1
                    rem = rem[1:]
                elif rem.startswith("b"):
                    alter = -1
                    rem = rem[1:]

                if rem.startswith("m7"):
                    kind = "minor-seventh"
                elif rem.startswith("maj7"):
                    kind = "major-seventh"
                elif rem.startswith("7"):
                    kind = "dominant"
                elif rem.startswith("m"):
                    kind = "minor"

                lines.extend([
                    '      <harmony>',
                    '        <root>',
                    f'          <root-step>{root_step}</root-step>',
                    *( [f'          <root-alter>{alter}</root-alter>'] if alter != 0 else [] ),
                    '        </root>',
                    f'        <kind>{kind}</kind>',
                    '      </harmony>'
                ])

            events = m.get("events", [])
            for ev in events:
                western = ev.get("note_western", "C4")
                syllable = ev.get("syllable", "")
                rhythm_name = ev.get("rhythm_name", "Quarter Note").lower()

                if "whole" in rhythm_name:
                    n_type = "whole"
                elif "half" in rhythm_name:
                    n_type = "half"
                elif "eighth" in rhythm_name or "8th" in rhythm_name:
                    n_type = "eighth"
                elif "16th" in rhythm_name:
                    n_type = "16th"
                else:
                    n_type = "quarter"

                divs = type_to_divs.get(n_type, 4)

                match = re.match(r'^([A-Ga-g])([#b]?)(-?\d+)$', western)
                if match:
                    step = match.group(1).upper()
                    acc = match.group(2)
                    octave = match.group(3)
                    alter = 1 if acc == "#" else (-1 if acc == "b" else 0)
                else:
                    step = "C"
                    octave = "4"
                    alter = 0

                lines.extend([
                    '      <note>',
                    '        <pitch>',
                    f'          <step>{step}</step>',
                    *( [f'          <alter>{alter}</alter>'] if alter != 0 else [] ),
                    f'          <octave>{octave}</octave>',
                    '        </pitch>',
                    f'        <duration>{divs}</duration>',
                    f'        <type>{n_type}</type>'
                ])

                if syllable and syllable != "—":
                    lines.extend([
                        '        <lyric number="1">',
                        f'          <text>{cls._escape_xml(syllable)}</text>',
                        '        </lyric>'
                    ])

                trans = ev.get("in_between_transition")
                if trans and isinstance(trans, dict):
                    curv = trans.get("curvature_type", "")
                    if curv in ["sigmoidal_s_meend", "concave_slide", "convex_scoop", "meend", "linear_ramp"]:
                        lines.extend([
                            '        <notations>',
                            '          <glissando type="start" number="1"/>',
                            '        </notations>'
                        ])

                lines.append('      </note>')

            lines.append('    </measure>')

        lines.extend([
            '  </part>',
            '</score-partwise>'
        ])
        return '\\n'.join(lines)
'''

if "def export_musicxml" not in text:
    text = text.rstrip() + code_to_append + '\n'
    with open('src/sheet_music_extractor.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Appended export_musicxml successfully.")
else:
    print("export_musicxml already present.")
