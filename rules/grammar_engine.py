from .agreement_rules import (
    SUBJECT_MARKER_RULES, OBJECT_MARKER_RULES, ADJECTIVE_PREFIX_RULES,ANIMATE_EXCEPTION_CLASSES
)


class KiswahiliGrammarEngine:
    """
    Evaluates Swahili sentences for grammatical correctness based on
    Noun Class agreements and syntax rules.
    """

    def __init__(self):
        self.errors = []
        self.warnings = []

    def _get_effective_class(self, noun_class, word_type="noun"):
        """
        Handles the Animate Exception rule from the Swahili Guide.
        If a Class 9/10 noun refers to a person/animal, it behaves as Class 1/2.
        """
        if noun_class in ANIMATE_EXCEPTION_CLASSES:
            # Note: In a full production app, we'd check a lexicon to see if
            # the specific Cl 9 noun is animate. For now, we flag it as a warning
            # if it doesn't match, or we can assume standard Cl 9 rules.
            pass
        return noun_class

    def check_subject_verb_agreement(self, noun_analysis, verb_analysis):
        """
        Checks if the verb's subject marker matches the noun's class.
        """
        if not noun_analysis or not verb_analysis:
            return True, "Skipped: Missing data"

        noun_class = str(noun_analysis.get('class', ''))
        subject_marker = verb_analysis.get('subject_marker', '')

        # Clean up subject marker for comparison (e.g., "a-" -> "a")
        expected_marker = SUBJECT_MARKER_RULES.get(noun_class, "")

        if subject_marker and expected_marker:
            if subject_marker.strip('-') == expected_marker.strip('-'):
                return True, "Subject-Verb agreement is correct."
            else:
                return False, f"Subject-Verb disagreement. Noun is Class {noun_class} (expects '{expected_marker}'), but verb has '{subject_marker}'."

        return True, "Agreement check passed."

    def check_adjective_noun_agreement(self, noun_analysis, adjective_word):
        """
        Checks if an adjective has the correct prefix for the noun.
        """
        if not noun_analysis or not adjective_word:
            return True, "Skipped"

        noun_class = str(noun_analysis.get('class', ''))
        expected_prefix = ADJECTIVE_PREFIX_RULES.get(noun_class, "")

        # If the class expects no prefix (like Cl 5, 9, 10), check if it starts with a prefix
        if not expected_prefix:
            # Basic check: if it's a known invariant adjective (like 'safi', 'bora'), it's fine.
            # For this engine, we assume standard agreement.
            return True, "Class requires no prefix or invariant adjective."

        if adjective_word.lower().startswith(expected_prefix):
            return True, "Adjective-Noun agreement is correct."
        else:
            return False, f"Adjective-Noun disagreement. Noun is Class {noun_class} (expects prefix '{expected_prefix}'), but adjective is '{adjective_word}'."

    def evaluate_sentence(self, morphological_analyses):
        """
        Main method to evaluate a fully parsed sentence.
        morphological_analyses: List of dicts outputted by Peter's Morphology Engine.
        """
        self.errors = []
        self.warnings = []
        score = 100

        # 1. Find the Subject and the Main Verb
        subject = None
        verb = None

        for analysis in morphological_analyses:
            if analysis.get('type') == 'noun' and not subject:
                subject = analysis
            elif analysis.get('type') == 'verb' and not verb:
                verb = analysis

        # 2. Check Subject-Verb Agreement
        if subject and verb:
            is_valid, message = self.check_subject_verb_agreement(subject, verb)
            if not is_valid:
                self.errors.append(message)
                score -= 40
            else:
                self.warnings.append(message)

        # 3. Check Adjective Agreements (Simple heuristic: look for words after nouns)
        for i in range(len(morphological_analyses) - 1):
            current = morphological_analyses[i]
            next_word = morphological_analyses[i + 1].get('word', '')

            if current.get('type') == 'noun' and next_word.isalpha():
                # Heuristic: if the next word isn't a verb or known noun, assume it's an adjective
                if morphological_analyses[i + 1].get('type') not in ['verb', 'noun']:
                    is_valid, message = self.check_adjective_noun_agreement(current, next_word)
                    if not is_valid:
                        self.errors.append(message)
                        score -= 30

        # Ensure score doesn't drop below 0
        score = max(0, score)

        return {
            "is_grammatically_correct": len(self.errors) == 0,
            "grammar_score": score,
            "errors": self.errors,
            "warnings": self.warnings
        }