"""
Day 8: SEE chunking failures, don't just read about them.
Run this as-is - no TODOs today, this is observation, not implementation.
"""

SAMPLE_TEXT = (
    "WebLens is a research assistant project. The company behind the original "
    "inspiration for this kind of tool, OpenAI, was founded in December 2015 "
    "in San Francisco. It started as a non-profit before restructuring in "
    "2019. The project you are building today has nothing to do with that "
    "company directly - it is a learning exercise. Still, the founding date "
    "fact above is a good test case: watch what happens to it below."
)


def naive_character_chunk(text: str, chunk_size: int) -> list[str]:
    """The naive approach: cut every N characters, no awareness at all."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def sentence_aware_chunk(text: str, max_size: int) -> list[str]:
    """A step up: never cut mid-sentence. Greedily pack whole sentences
    into a chunk until adding the next one would exceed max_size."""
    sentences = [s.strip() + "." for s in text.split(". ") if s.strip()]
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) <= max_size:
            current += (" " if current else "") + sentence
        else:
            if current:
                chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


print("=" * 70)
print("NAIVE CHARACTER-BASED CHUNKING (chunk_size=80, no awareness)")
print("=" * 70)
for i, chunk in enumerate(naive_character_chunk(SAMPLE_TEXT, 80)):
    print(f"[chunk {i}] {chunk!r}")

print()
print("=" * 70)
print("SENTENCE-AWARE CHUNKING (max_size=150, never cuts mid-sentence)")
print("=" * 70)
for i, chunk in enumerate(sentence_aware_chunk(SAMPLE_TEXT, 150)):
    print(f"[chunk {i}] {chunk!r}")
