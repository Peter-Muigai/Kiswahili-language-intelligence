from typing import Dict
from src.utils import DataLoader

class MorphemeSegmenter:
    def __init__(self):
        self.loader = DataLoader()

        # Load dictionaries for disambiguation
        self.verbs = {row['infinitive'].lower(): row for row in self.loader.get_verbs()}
        self.nouns = {row['noun'].lower(): row for row in self.loader.get_nouns()}
        # Create a lookup for plural forms
        self.noun_plurals = {row['plural_form'].lower(): row for row in self.loader.get_nouns() if
                             row.get('plural_form')}
        self.valid_roots = {row['root'].lower() for row in self.loader.get_verbs()}

        # Clean tense markers (remove dashes for matching)
        self.tense_prefixes = ['na', 'li', 'ta', 'me', 'a', 'ku', 'ja', 'hu']
        self.subject_marker_patterns = [
            'wa', 'ni', 'tu', 'ku', 'li', 'ya', 'ki', 'vi', 'zi', 'm', 'u', 'a', 'i', 'pa'
        ]
        self.object_marker_patterns = [
            'ni', 'wa', 'ku', 'tu', 'm', 'li', 'ya', 'ki', 'vi', 'zi', 'u', 'i', 'pa'
        ]
        self.negative_prefixes = ['si', 'ha']

    def _get_plural_class(self, singular_class: str) -> str:
        """Helper to map singular noun class to its plural counterpart."""
        class_pairs = {
            '1': '2', '2':'1', '3': '4', '4': '3',
            '5': '6', '6': '5', '7': '8', '8': '7',
            '9': '10', '10': '9', '11': '10'
        }
        return class_pairs.get(singular_class, singular_class)
    def segment_verb(self, verb: str) -> Dict[str, str]:
        result = {
            'original': verb, 'negative': False, 'subject_marker': None,
            'tense_marker': None, 'object_marker': None, 'root': None, 'suffix': None
        }
        remaining = verb.lower()

        for neg in self.negative_prefixes:
            if remaining.startswith(neg):
                result['negative'] = True
                remaining = remaining[len(neg):]
                break

        for sm in self.subject_marker_patterns:
            if remaining.startswith(sm):
                result['subject_marker'] = sm + '-'
                remaining = remaining[len(sm):]
                break

        for tm in self.tense_prefixes:
            if remaining.startswith(tm):
                result['tense_marker'] = '-' + tm + '-'
                remaining = remaining[len(tm):]
                break

        # FIX: Check for object marker ONLY if the remaining part is not a known verb form
        is_known_verb_form = remaining in self.verbs or remaining in self.valid_roots

        if result['subject_marker'] and result['tense_marker'] and not is_known_verb_form:
            for om in self.object_marker_patterns:
                if remaining.startswith(om):
                    result['object_marker'] = '-' + om + '-'
                    remaining = remaining[len(om):]
                    break

        if remaining:
            result['root'] = remaining
        return result

    def segment_noun(self, noun: str) -> Dict[str, str]:
        result = {'original': noun, 'prefix': None, 'stem': None, 'class': None}
        noun_classes = self.loader.get_noun_classes()['classes']

        for class_num, class_data in noun_classes.items():
            prefix = class_data.get('singular_prefix')
            if not prefix or prefix in ['', 'ji-/']:
                continue
            clean_prefix = prefix.split('/')[0].rstrip('-')

            if noun.lower().startswith(clean_prefix) and len(noun) > len(clean_prefix):
                result['prefix'] = clean_prefix + '-'
                result['stem'] = noun[len(clean_prefix):]
                result['class'] = class_num
                break

        if result['prefix'] is None:
            result['stem'] = noun
            result['class'] = '9/10'
        return result

    def identify_morphemes(self, word: str) -> Dict:
        word_lower = word.lower()

        # 1. Check if it's a known singular noun
        if word_lower in self.nouns:
            noun_data = self.nouns[word_lower]
            return {
                'type': 'noun', 'original': word,
                'prefix': noun_data.get('singular_prefix', ''),
                'stem': word_lower, 'class': noun_data['class'],
                'plural_form': noun_data.get('plural_form', '')
            }

        # 2. FIX: Check if it's a known plural noun (e.g., vitabu, watoto)
        if word_lower in self.noun_plurals:
            noun_data = self.noun_plurals[word_lower]
            plural_prefix = noun_data.get('plural_prefix', '')
            clean_plural_prefix = plural_prefix.split('/')[0].rstrip('-') if plural_prefix else ''
            stem = word_lower[len(clean_plural_prefix):] if clean_plural_prefix else word_lower

            # Calculate the actual plural class
            singular_class = noun_data['class']
            plural_class = self._get_plural_class(singular_class)

            return {
                'type': 'noun', 'original': word,
                'prefix': clean_plural_prefix + '-' if clean_plural_prefix else '',
                'stem': stem, 'class': noun_data['class'],
                'plural_form': word_lower
            }

        # 3. Check if it's a known verb (infinitive)
        if word_lower in self.verbs:
            return {
                'type': 'verb', 'original': word,
                'root': self.verbs[word_lower]['root'],
                'tense_marker': None, 'subject_marker': None
            }

        # 4. Rule-based segmentation for conjugated verbs
        verb_result = self.segment_verb(word)

        # Only accept as verb if it has markers AND a plausible root
        if verb_result['subject_marker'] and verb_result['tense_marker'] and verb_result['root']:
            if verb_result['root'] in self.valid_roots or len(verb_result['root']) > 2:
                return {'type': 'verb', **verb_result}

        # 5. Rule-based segmentation for prefixed nouns
        noun_result = self.segment_noun(word)
        if noun_result['prefix']:
            return {'type': 'noun', **noun_result}

        # 6. Fallback
        return {
            'type': 'noun', 'original': word,
            'prefix': '', 'stem': word, 'class': '9/10'
        }