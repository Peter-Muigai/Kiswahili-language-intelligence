from typing import Dict, Optional
from src.utils import DataLoader


class SubjectMarkerDetector:
    def __init__(self):
        self.loader = DataLoader()
        self.subject_data = self.loader.get_subject_markers()

        self.subject_markers = {
            'wa': {'class': '2', 'type': 'noun_class', 'person': '3rd_plural'},
            'ni': {'class': '1st_singular', 'type': 'personal', 'person': '1st_singular'},
            'tu': {'class': '1st_plural', 'type': 'personal', 'person': '1st_plural'},
            'ku': {'class': '15', 'type': 'noun_class', 'person': None},
            'li': {'class': '5', 'type': 'noun_class', 'person': None},
            'ya': {'class': '6', 'type': 'noun_class', 'person': None},
            'ki': {'class': '7', 'type': 'noun_class', 'person': None},
            'vi': {'class': '8', 'type': 'noun_class', 'person': None},
            'zi': {'class': '10', 'type': 'noun_class', 'person': None},
            'm': {'class': '18', 'type': 'locative', 'person': None},
            'u': {'class': '3/11/14', 'type': 'noun_class', 'person': None},
            'a': {'class': '1', 'type': 'noun_class', 'person': '3rd_singular'},
            'i': {'class': '4/9', 'type': 'noun_class', 'person': None},
            'pa': {'class': '16', 'type': 'locative', 'person': None}
        }

    def detect_subject(self, verb: str) -> Optional[Dict]:
        if verb.lower().startswith('si'):
            return {
                'marker': 'ni-',
                'class': '1st_singular',
                'type': 'personal',
                'person': '1st_singular',
                'is_negative': True
            }

        verb_body = verb.lower()
        if verb_body.startswith('ha'):
            verb_body = verb_body[2:]

        for marker, info in self.subject_markers.items():
            if verb_body.startswith(marker):
                return {
                    'marker': marker + '-',
                    **info,
                    'is_negative': verb.lower().startswith('ha')
                }
        return None

    def get_subject_marker(self, person_class: str) -> Optional[str]:
        for marker, info in self.subject_markers.items():
            if info['class'] == person_class or info.get('person') == person_class:
                return marker + '-'
        return None