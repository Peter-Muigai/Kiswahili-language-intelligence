# A curated dataset of Swahili sentences to test the Grammar Engine
GRAMMAR_TEST_DATASET = [
    {
        "sentence": "Mtoto anapenda maziwa.",
        "is_correct": True,
        "explanation": "Mtoto (Cl 1) correctly uses 'a-' subject marker in 'anapenda'."
    },
    {
        "sentence": "Vitabu vinapotea.",
        "is_correct": True,
        "explanation": "Vitabu (Cl 8) correctly uses 'vi-' subject marker in 'vinapotea'."
    },
    {
        "sentence": "Kitabu kinapotea.",
        "is_correct": True,
        "explanation": "Kitabu (Cl 7) correctly uses 'ki-' subject marker in 'kinapotea'."
    },
    {
        "sentence": "Watoto wanakula vyakula.",
        "is_correct": True,
        "explanation": "Watoto (Cl 2) correctly uses 'wa-' subject marker in 'wanakula'."
    },
    {
        "sentence": "Mti unakua.",
        "is_correct": True,
        "explanation": "Mti (Cl 3) correctly uses 'u-' subject marker in 'unakua'."
    },
    {
        "sentence": "Vitabu kinapotea.",
        "is_correct": False,
        "explanation": "ERROR: Vitabu is Class 8 (plural), but 'kinapotea' uses the Class 7 (singular) marker 'ki-'. It should be 'vinapotea'."
    },
    {
        "sentence": "Mtoto wapenda maziwa.",
        "is_correct": False,
        "explanation": "ERROR: Mtoto is Class 1 (singular), but 'wapenda' uses the Class 2 (plural) marker 'wa-'. It should be 'anapenda'."
    },
    {
        "sentence": "Nyumba zinaanguka.",
        "is_correct": True,
        "explanation": "Nyumba (Cl 9/10 plural context) correctly uses 'zi-' subject marker."
    },
    {
        "sentence": "Daktari mzuri anakuja.",
        "is_correct": True,
        "explanation": "Daktari (Cl 9) referring to a person correctly takes Class 1 adjective prefix 'm-' (mzuri) and Class 1 verb marker 'a-' (anakuja)."
    }
]