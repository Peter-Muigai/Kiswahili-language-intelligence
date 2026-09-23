import re
from typing import List

class Tokenizer:
    """Tokenizes Kiswahili text into words and morphemes"""

    def __init__(self):
        # Common punctuation to remove.
        self.punctuation = r'[.,!?;:"\'(){}\[\]]'

    def tokenize_sentence(self, text:str) -> List[str]:
        """
        Split text into words/tokens

        Args:
            text: Kiswahili sentence

        Returns:
            List of word tokens
        """
        # Remove punctuation.
        text = re.sub(self.punctuation, '', text)
        # Split on white space.
        tokens = text.strip().split()
        return tokens

    def tokenize_word(self, word: str) -> List[str]:
        """
        Split a word into character-level tokens

        Args:
            word: Single Kiswahili word
        Returns:
            List of characters
        """
        return list(word)

    def is_valid_word(self, word: str) -> bool:
        """
        Check if string is a valid Kiswahili word

        Args:
            word: string to check
        Return:
            Boolean
        """
        # Basic validation: at least 2 characters, contains only letters.
        if len(word) < 2:
            return False
        if not word.isalpha():
            return False
        return True