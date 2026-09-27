#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
concordance.py - Külliyat Metin Korpusu İçin Konkordans ve Frekans Analizörü

Kullanım:
    python scripts/concordance.py --kwic "istikamet" --window 5
    python scripts/concordance.py --top 20
"""

import os
import sys
import re
import argparse
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CORPUS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STOP_WORDS = {
    "ve", "bir", "bu", "ile", "için", "olan", "olarak", "da", "de", "gibi",
    "en", "her", "daha", "çok", "kadar", "kendi", "ise", "ya", "ki", "sonra",
    "önce", "üzere", "bunu", "buna", "tarafından", "şekilde", "olarak", "aynı"
}

def load_corpus_text():
    all_text = []
    for root, dirs, files in os.walk(CORPUS_ROOT):
        if '.git' in root:
            continue
        for f in sorted(files):
            if f.endswith('.md'):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        all_text.append((os.path.relpath(fp, CORPUS_ROOT), fh.read()))
                except Exception:
                    pass
    return all_text

def analyze_frequencies(top_n=30):
    corpus = load_corpus_text()
    words = []
    for path, text in corpus:
        # Clean text
        clean = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text.lower())
        tokens = clean.split()
        for t in tokens:
            if len(t) > 2 and t not in STOP_WORDS and not t.isdigit():
                words.append(t)

    counter = Counter(words)
    print("================================================================")
    print(f"      En Sık Geçen {top_n} Kavram ve Terim Frekans Tablosu     ")
    print("================================================================")
    for rank, (word, count) in enumerate(counter.most_common(top_n), 1):
        bar = "█" * min(30, count // 2)
        print(f" {rank:>2}. {word:<22} : {count:>4} defa  {bar}")
    print("================================================================")

def find_kwic(target_word, window=5):
    corpus = load_corpus_text()
    pattern = re.compile(r'\b' + re.escape(target_word) + r'\b', re.IGNORECASE)
    matches_found = 0

    print("================================================================")
    print(f"   KWIC (Key Word In Context) Konkordans: '{target_word}'     ")
    print("================================================================")

    for path, text in corpus:
        words = text.split()
        for i, w in enumerate(words):
            clean_w = re.sub(r'[^\w\s]', '', w)
            if pattern.search(clean_w):
                start = max(0, i - window)
                end = min(len(words), i + window + 1)
                left_context = " ".join(words[start:i])
                keyword = words[i]
                right_context = " ".join(words[i+1:end])
                
                print(f"[{path}]")
                print(f"   ... {left_context:>35}  >>> {keyword.upper()} <<<  {right_context:<35} ...\n")
                matches_found += 1
                if matches_found >= 15:
                    break
        if matches_found >= 15:
            print("   ... (Daha fazla sonuç listelenmedi)")
            break

    print(f"Toplam listelenen eşleşme: {matches_found}")

def main():
    parser = argparse.ArgumentParser(description="Külliyat konkordans ve frekans analizörü.")
    parser.add_argument("--top", type=int, default=0, help="En sık geçen N kavramı listeler")
    parser.add_argument("--kwic", help="Bağlam içinde anahtar kelime araması (KWIC)")
    parser.add_argument("--window", type=int, default=5, help="KWIC bağlam kelime sayısı")
    args = parser.parse_args()

    if args.kwic:
        find_kwic(args.kwic, args.window)
    elif args.top:
        analyze_frequencies(args.top)
    else:
        analyze_frequencies(25)

if __name__ == "__main__":
    main()
