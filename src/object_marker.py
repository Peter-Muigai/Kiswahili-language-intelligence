from typing import Dict, Optional
from src.utils import DataLoader

class ObjectMarkerDetector:
    def __init__(self):
        self.loader = DataLoader()
        self.object_data = self.loader.get_object_markers()

        self.object_markers = {
            'ni': {'class': '1st_singular', 'type': 'personal'},
            'ku': {'class': '2nd_singular', 'type': 'personal'},
            'm': {'class': '1', 'type': 'noun_class'},
            'wa': {'class': '2', 'type': 'noun_class'},
            'tu': {'class': '1st_plural', 'type': 'personal'},
            'li': {'class': '5', 'type': 'noun_class'},
            'ya': {'class': '6', 'type': 'noun_class'},
            'ki': {'class': '7', 'type': 'noun_class'},
            'vi': {'class': '8', 'type': 'noun_class'},
            'zi': {'class': '10', 'type': 'noun_class'},
            'u': {'class': '3/11/14', 'type': 'noun_class'},
            'i': {'class': '4/9', 'type': 'noun_class'},
            'pa': {'class': '16', 'type': 'locative'}
        }

    def detect_object(self, verb: str) -> Optional[Dict]:
        tense_markers = ['na', 'li', 'ta', 'me', 'a']

        for tense in tense_markers:
            if tense in verb.lower():
                idx = verb.lower().find(tense)
                after_tense = verb.lower()[idx + len(tense):]

                for marker, info in self.object_markers.items():
                    if after_tense.startswith(marker):
                        return {
                            'marker': '-' + marker + '-',
                            **info
                        }
        return None

    def get_object_marker(self, person_class: str) -> Optional[str]:
        for marker, info in self.object_markers.items():
            if info['class'] == person_class:
                return '-' + marker + '-'
        return None