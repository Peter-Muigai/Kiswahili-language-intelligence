# rules/agreement_rules.py
# Maps Noun Class to the expected Subject Marker on the verb
SUBJECT_MARKER_RULES = {
    "1": "a-", "2": "wa-", "3": "u-", "4": "i-",
    "5": "li-", "6": "ya-", "7": "ki-", "8": "vi-",
    "9": "i-", "10": "zi-", "11": "u-", "14": "u-",
    "15": "ku-", "16": "pa-", "17": "ku-", "18": "m-"
}

# Maps Noun Class to the expected Adjective Prefix
ADJECTIVE_PREFIX_RULES = {
    "1": "m-", "2": "wa-", "3": "m-", "4": "mi-",
    "5": "", "6": "ma-", "7": "ki-", "8": "vi-",
    "9": "", "10": "", "11": "m-", "14": "m-",
    "15": "ku-", "16": "pa-", "17": "ku-", "18": "m-"
}

# Maps Noun Class to the expected Object Marker
OBJECT_MARKER_RULES = {
    "1": "-m-", "2": "-wa-", "3": "-u-", "4": "-i-",
    "5": "-li-", "6": "-ya-", "7": "-ki-", "8": "-vi-",
    "9": "-i-", "10": "-zi-", "11": "-u-", "14": "-u-",
    "15": "-ku-", "16": "-pa-", "17": "-ku-", "18": "-m-"
}

# CRITICAL RULE FROM SWAHILI GUIDE (Page 117 & 132):
# Nouns referring to people/animals take Class 1 (singular) or Class 2 (plural)
# agreements for adjectives and verbs, REGARDLESS of their actual noun class.
ANIMATE_EXCEPTION_CLASSES = {
    "9": "1",  # e.g., mbwa (dog, Cl 9) -> takes Cl 1 agreement (mbwa mkali)
    "10": "2"  # e.g., mbwa (dogs, Cl 10) -> takes Cl 2 agreement (mbwa wakali)
}