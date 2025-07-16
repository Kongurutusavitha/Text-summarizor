#!/usr/bin/env python3
import re
from collections import Counter
from heapq import nlargest

class TextSummarizer:
    def __init__(self):
        self.stop_words = set("""
            the a an and or but in on at to for of with by is are was were be been being have has had do does did
            will would could should may might must can this that these those i you he she it we they me him her us
            them my your his its our their from up about into through during before after above below between among
            under over so than too very just now
        """.split())

    def summarize(self, text, num_sentences=3):
        text = re.sub(r'[^\w\s.]', '', re.sub(r'\s+', ' ', text)).strip()
        sentences = [s for s in re.split(r'(?<=[.!?])\s+', text) if len(s.split()) > 5]
        if len(sentences) <= num_sentences: return ' '.join(sentences)
        words = [w for w in re.findall(r'\b\w+\b', text.lower()) if w not in self.stop_words and len(w) > 2]
        freqs = Counter(words)
        scores = {
            s: sum(freqs.get(w, 0) for w in re.findall(r'\b\w+\b', s.lower()) if w not in self.stop_words) / len(s.split())
            for s in sentences
        }
        best = nlargest(num_sentences, scores, key=scores.get)
        return ' '.join(s for s in sentences if s in best)

def demo():
    articles = [
        {"title": "AI Revolution", "text": """Artificial intelligence has emerged..."""},
        {"title": "Climate Change Impact", "text": """Climate change represents one of..."""},
        {"title": "Space Exploration Future", "text": """Space exploration has entered a new era..."""}
    ]
    summarizer = TextSummarizer()
    for i, a in enumerate(articles, 1):
        print(f"\n📰 ARTICLE {i}: {a['title']}\n{'-'*50}")
        original = a['text'].strip()
        summary = summarizer.summarize(original)
        print(f"📄 Original ({len(original.split())} words):\n{original}")
        print(f"\n🎯 Summary ({len(summary.split())} words):\n{summary}\n")

def interactive():
    print("\n🎮 INTERACTIVE MODE — Enter text (empty line to finish):\n")
    lines = []
    while True:
        try:
            line = input()
            if not line.strip(): break
            lines.append(line)
        except KeyboardInterrupt: return print("\n⏹️  Interrupted.")
    text = ' '.join(lines).strip()
    if len(text.split()) < 20: return print("⚠️  Text too short to summarize.")
    summarizer = TextSummarizer()
    for n in [2, 3, 5]:
        print(f"\n🔹 {n}-Sentence Summary:\n{'-'*30}")
        print(summarizer.summarize(text, n))

def main():
    print("🧠 TEXT SUMMARIZATION TOOL\n" + "="*40)
    while True:
        print("\n1. 📰 Demo with sample articles\n2. ✍️  Summarize your own text\n3. ❌ Exit")
        try:
            choice = input("Choose (1-3): ").strip()
            if choice == "1": demo()
            elif choice == "2": interactive()
            elif choice == "3": return print("👋 Goodbye!")
            else: print("❌ Invalid option.")
        except KeyboardInterrupt: return print("\n👋 Interrupted.")

if __name__ == "__main__":
    main()
