from typing import Dict, Optional
from src.utils import DataLoader

class NounClassAnalyzer:
    def __init__(self):
        self.loader = DataLoader()
        self.noun_classes = self.loader.get_noun_classes()['classes']
        self.noun_data = self.loader.get_nouns()

    def analyze_noun(self, noun: str) -> Optional[Dict]:
        result = {
            'noun': noun, 'class': None, 'prefix': None, 'stem': None,
            'plural_class': None, 'plural_form': None
        }

        for class_num, class_info in self.noun_classes.items():
            prefix = class_info.get('singular_prefix')
            if not prefix or prefix in ['∅', 'ji-/∅']:
                continue

            clean_prefix = prefix.split('/')[0].rstrip('-')

            if noun.lower().startswith(clean_prefix) and len(noun) > len(clean_prefix):
                result['class'] = class_num
                result['prefix'] = clean_prefix + '-'
                result['stem'] = noun[len(clean_prefix):]
                result['plural_class'] = class_info.get('plural_class')
                result['description'] = class_info.get('description')

                if result['plural_class']:
                    plural_prefix = self.noun_classes[result['plural_class']].get('singular_prefix', '')
                    plural_prefix = plural_prefix.split('/')[0].rstrip('-').replace('∅', '')

                    if plural_prefix:
                        result['plural_form'] = plural_prefix + result['stem']
                    else:
                        result['plural_form'] = result['stem']  # No prefix needed
                break

        # Fallback to CSV data if rule-based fails
        if result['class'] is None:
            for noun_entry in self.noun_data:
                if noun_entry['noun'].lower() == noun.lower():
                    result['class'] = noun_entry['class']
                    result['stem'] = noun
                    result['plural_form'] = noun_entry.get('plural_form')
                    result['plural_class'] = self._get_plural_class(noun_entry['class'])
                    break

        return result

    def _get_plural_class(self, singular_class: str) -> Optional[str]:
        class_pairs = {
            '1': '2', '2': '1', '3': '4', '4': '3',
            '5': '6', '6': '5', '7': '8', '8': '7',
            '9': '10', '10': '9', '11': '10'
        }
        return class_pairs.get(singular_class)

    def get_class_agreement(self, class_num: str) -> Dict:
        subject_data = self.loader.get_subject_markers()
        object_data = self.loader.get_object_markers()
        return {
            'class': class_num,
            'subject_marker': subject_data.get('noun_classes', {}).get(class_num, {}).get('marker'),
            'object_marker': object_data.get('noun_classes', {}).get(class_num, {}).get('marker')
        }

    def validate_agreement(self, subject: str, verb: str) -> bool:
        subject_analysis = self.analyze_noun(subject)
        if not subject_analysis or not subject_analysis['class']:
            return False
        expected_marker = self.get_class_agreement(subject_analysis['class'])['subject_marker']
        return expected_marker is not None and expected_marker in verb