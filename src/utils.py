import json
import csv
from pathlib import Path

class DataLoader:
    """Utility class for loading linguistic data."""

    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent / 'data'
        else:
            self.data_dir = Path(data_dir)

    def load_json(self, filename):
        """Load JSON data file."""
        filepath = self.data_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_csv(self, filename):
        """Load CSV data file."""
        filepath = self.data_dir / filename
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def get_subject_markers(self):
        return self.load_json('subject_markers.json')

    def get_tense_markers(self):
        return self.load_json('tense_markers.json')

    def get_object_markers(self):
        return self.load_json('object_markers.json')

    def get_noun_classes(self):
        return self.load_json('noun_classes.json')


    def get_verbs(self):
        return self.load_csv('verbs.csv')

    def get_nouns(self):
        return self.load_csv('nouns.csv')