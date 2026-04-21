# Experiment logs
CS4241 — Introduction to Artificial Intelligence
Student: Farima Konaré | Index: 10012200004

These logs are written by hand while running the experiment notebooks. Record actual numbers and responses from the system — not summaries.

---

## Log 1 — Chunking strategy comparison

**Date:** [fill in]
**Notebook:** `experiments/01_chunking_analysis.ipynb`

### What the notebook produced
- Election CSV: [X] chunks, fixed-size strategy (400 chars, 80 overlap)
- Budget PDF: [X] chunks, paragraph-aware strategy
- Mean chunk length — election: [X] chars, budget: [X] chars

### What I observed
[Write what you actually saw. Were the chunk sizes reasonable? Did any look too short or too long? Paste specific numbers from the notebook output.]

### Why the strategies work
Fixed-size made sense for the election rows because [your observation]. Paragraph-aware worked better for the budget because [your observation].

---

## Log 2 — Retrieval failure case

**Date:** [fill in]
**Notebook:** `experiments/02_retrieval_failures.ipynb`
**Query tested:** "What happened in the north?"

Before query expansion:
- Top chunk combined score: [X]
- Top chunk source: [election / budget]
- Top chunk text (first 80 chars): [paste it]
- Relevant? [Y/N — say why]

After query expansion ("Ghana election northern region What happened in the north?"):
- Top chunk combined score: [X]
- Top chunk source: [election]
- Top chunk text (first 80 chars): [paste it]
- More relevant? [Y/N — say why]

### What changed
[Write what you saw. Did scores go up? Did a different region appear? Was the result actually more useful?]

---

## Log 3 — Prompt template comparison

**Date:** [fill in]
**Notebook:** `experiments/03_prompt_comparison.ipynb`
**Query tested:** "Who won the 2020 presidential election in Ghana?"

Template 1 (baseline):
[Paste the actual model response, first 2-3 sentences]
- Added information not in the context? [Y/N]
- Tone: [factual / verbose / hedged]

Template 2 (hallucination-controlled):
[Paste the actual model response]
- Refused to speculate? [Y/N]
- Cited the context explicitly? [Y/N]

Template 3 (with memory):
[Paste the actual model response]
- Did memory affect the answer? [Y/N — explain]
- More contextually coherent than Template 1? [Y/N]

### Which template is best and why
[Write your actual observation. Template 3 is set as default — does the output confirm that was the right choice?]

---

## Log 4 — Adversarial tests

**Date:** [fill in]
**Notebook:** `experiments/04_adversarial_tests.ipynb`

### Query 1: "Who won?" (ambiguous)

RAG response:
[Paste actual response]
- Hallucination? [Y/N — explain]
- Did it ask for clarification or admit ambiguity? [Y/N]
- Top combined score: [X]

Pure LLM response (no retrieval):
[Paste actual response]
- Hallucination? [Y/N — explain]
- Did it invent a specific winner? [Y/N]

RAG vs LLM: [which was more accurate and why]

---

### Query 2: "What did the president say about free healthcare in the 2025 budget?"

RAG response:
[Paste actual response]
- Confidence threshold triggered (score < 0.25)? [Y/N]
- Top combined score: [X]
- Did it correctly refuse to fabricate? [Y/N]

Pure LLM response (no retrieval):
[Paste actual response]
- Did it hallucinate a presidential quote? [Y/N]
- Did it cite a specific speech or document? [Y/N — this is hallucination if it did]

RAG vs LLM: [write what the difference was]

---

## Log 5 — Memory test

**Date:** [fill in]
**Test:** Multi-turn conversation to verify memory injection works

Turn 1:
- Query: "Who won the 2020 presidential election?"
- Response: [first sentence of actual response]

Turn 2:
- Query: "What about 2016?"
- Response: [first sentence of actual response]
- Did it understand "2016" as referring to the election? [Y/N]
- Was the prior turn visible in the "Final prompt" expander? [Y/N]

What I observed:
[Write what you saw. Did memory help? Was the 2016 answer coherent given the 2020 context, or did it seem disconnected?]

---

## Summary

| Experiment | Key finding | Effect on system |
|---|---|---|
| Chunking | [fill in] | [fill in] |
| Retrieval failure | Query expansion improved northern region recall | Fixed vague geographic queries |
| Prompt comparison | Template 3 outperformed Template 1 on specificity | Set as default |
| Adversarial Q1 | [fill in] | [fill in] |
| Adversarial Q2 | [fill in] | [fill in] |
| Memory | [fill in] | [fill in] |
