from typing import Dict, Optional
from src.utils import DataLoader

class TenseDetector:
    def __init__(self):
        self.loader = DataLoader()
        self.tense_data = self.loader.get_tense_markers()

        # Clean markers (remove dashes)
        self.tense_markers = {
            'na': 'present_progressive',
            'a': 'simple_present',
            'li': 'past',
            'ta': 'future',
            'me': 'perfect',
            'ku': 'negative_past',
            'ja': 'negative_perfect',
            'hu': 'habitual'
        }

    def detect_tense(self, verb: str) -> Optional[Dict]:
        is_negative = verb.lower().startswith('si') or verb.lower().startswith('ha')

        verb_body = verb.lower()
        if is_negative:
            verb_body = verb_body[2:]

        if verb_body.startswith('hu'):
            return {
                'tense': 'habitual',
                'marker': 'hu-',
                'is_negative': False,
                'name': self.tense_data.get('tense_markers', {}).get('habitual', {}).get('name', 'habitual')
            }

        for marker, tense_name in self.tense_markers.items():
            if marker in verb_body:
                idx = verb_body.find(marker)
                if idx >= 1:
                    tense_info = self.tense_data.get('tense_markers', {}).get(tense_name, {})
                    return {
                        'tense': tense_name,
                        'marker': '-' + marker + '-',
                        'is_negative': is_negative,
                        'name': tense_info.get('name', tense_name),
                        'example': tense_info.get('example', '')
                    }
        return None

    def get_tense_marker(self, tense_name: str) -> Optional[str]:
        for marker, name in self.tense_markers.items():
            if name == tense_name:
                return '-' + marker + '-'
        return None