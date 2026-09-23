from typing import Dict, List
from src.tokenizer import Tokenizer
from src.segmenter import MorphemeSegmenter
from src.tense import TenseDetector
from src.subject_marker import SubjectMarkerDetector
from src.object_marker import ObjectMarkerDetector
from src.noun_class import NounClassAnalyzer

class KiswahiliMorphologyEngine:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.segmenter = MorphemeSegmenter()
        self.tense_detector = TenseDetector()
        self.subject_detector = SubjectMarkerDetector()
        self.object_detector = ObjectMarkerDetector()
        self.noun_analyzer = NounClassAnalyzer()

    def analyze_word(self, word: str) -> Dict:
        analysis = {
            'word': word,
            'tokens': self.tokenizer.tokenize_word(word),
            'is_valid': self.tokenizer.is_valid_word(word)
        }

        segmentation = self.segmenter.identify_morphemes(word)
        analysis.update(segmentation)

        if segmentation.get('type') == 'verb':
            analysis['tense'] = self.tense_detector.detect_tense(word)
            analysis['subject'] = self.subject_detector.detect_subject(word)
            analysis['object'] = self.object_detector.detect_object(word)

        if segmentation.get('type') == 'noun':
            analysis['noun_class'] = self.noun_analyzer.analyze_noun(word)

        return analysis

    def analyze_sentence(self, sentence: str) -> List[Dict]:
        tokens = self.tokenizer.tokenize_sentence(sentence)
        analyses = []
        for token in tokens:
            if self.tokenizer.is_valid_word(token):
                analyses.append(self.analyze_word(token))
        return analyses

    def extract_root(self, word: str) -> str:
        segmentation = self.segmenter.identify_morphemes(word)
        word_type = segmentation.get('type')

        if word_type == 'verb':
            return segmentation.get('root', word)
        elif word_type == 'noun':
            return segmentation.get('stem', word)

        return word

    def detect_prefixes_suffixes(self, word: str) -> Dict[str, List[str]]:
        prefixes = []
        suffixes = []
        segmentation = self.segmenter.identify_morphemes(word)

        if segmentation.get('type') == 'verb':
            if segmentation.get('negative'): prefixes.append('negative')
            if segmentation.get('subject_marker'): prefixes.append(f"subject: {segmentation['subject_marker']}")
            if segmentation.get('tense_marker'): prefixes.append(f"tense: {segmentation['tense_marker']}")
            if segmentation.get('object_marker'): prefixes.append(f"object: {segmentation['object_marker']}")

        if segmentation.get('type') == 'noun':
            if segmentation.get('prefix'): prefixes.append(f"class prefix: {segmentation['prefix']}")

        return {'prefixes': prefixes, 'suffixes': suffixes}