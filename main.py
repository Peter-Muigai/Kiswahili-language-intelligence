from src.morphology import KiswahiliMorphologyEngine
import json

def main():
    """Main function to demonstrate the morphology engine"""

    # Initialize the engine
    engine = KiswahiliMorphologyEngine()

    print("=" * 60)
    print("KISWAHILI MORPHOLOGY ENGINE")
    print("=" * 60)

    # Example 1: Analyze a verb
    print("\n1. VERB ANALYSIS")
    print("-" * 40)
    verb = "anampenda"
    print(f"Analyzing: {verb}")
    analysis = engine.analyze_word(verb)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

    # Example 2: Analyze a sentence
    print("\n2. SENTENCE ANALYSIS")
    print("-" * 40)
    sentence = "Ninapenda kusoma kitabu"
    print(f"Analyzing: {sentence}")
    analyses = engine.analyze_sentence(sentence)
    for i, analysis in enumerate(analyses, 1):
        print(f"\nWord {i}: {analysis['word']}")
        print(f"  Type: {analysis.get('type', 'unknown')}")
        if analysis.get('tense'):
            print(f"  Tense: {analysis['tense']}")
        if analysis.get('noun_class'):
            print(f"  Noun Class: {analysis['noun_class']}")

    # Example 3: Extract roots
    print("\n3. ROOT EXTRACTION")
    print("-" * 40)
    words = ["wanasoma", "tulikula", "wataenda", "vitabu", "watoto"]
    for word in words:
        root = engine.extract_root(word)
        print(f"{word} → {root}")

    # Example 4: Detect prefixes and suffixes
    print("\n4. PREFIX/SUFFIX DETECTION")
    print("-" * 40)
    word = "hawatasoma"
    prefixes = engine.detect_prefixes_suffixes(word)
    print(f"{word}:")
    print(f"  Prefixes: {', '.join(prefixes['prefixes'])}")
    print(f"  Suffixes: {', '.join(prefixes['suffixes'])}")

    # Example 5: Noun class analysis
    print("\n5. NOUN CLASS ANALYSIS")
    print("-" * 40)
    nouns = ["kitabu", "mtu", "nyumba", "gari"]
    for noun in nouns:
        analysis = engine.analyze_word(noun)
        if analysis.get('noun_class'):
            nc = analysis['noun_class']
            print(f"{noun}:")
            print(f"  Class: {nc.get('class')}")
            print(f"  Prefix: {nc.get('prefix')}")
            print(f"  Stem: {nc.get('stem')}")
            print(f"  Plural: {nc.get('plural_form')}")

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()