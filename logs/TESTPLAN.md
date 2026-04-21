# Experiment Test Plan
**CS4241 — Introduction to Artificial Intelligence**
**Student:** Farima Konaré | **Index:** 10012200004

> Follow this plan step by step. After each test, copy your results into `experiment_logs.md`.
> Run all tests with the app running (`streamlit run app.py`) and notebooks open side-by-side.

---

## BEFORE YOU START

Make sure:
- [ ] `streamlit run app.py` is running and loads without errors
- [ ] All 4 Jupyter notebooks are open in your browser
- [ ] You have your Groq API key entered in the sidebar

---

## TEST 1 — Chunking Analysis (Part A)
**Notebook:** `experiments/01_chunking_analysis.ipynb`

**Steps:**
1. Open the notebook, click **Run All**
2. Wait for all cells to complete
3. **Record in `experiment_logs.md` → Log 1:**
   - Write down the exact number printed: `Election chunks: ___`
   - Write down the exact number printed: `Budget chunks: ___`
   - Write down: `Mean election chunk length: ___ chars`
   - Write down: `Mean budget chunk length: ___ chars`
   - Save the chart image (`chunking_distributions.png`) — it will be in the `experiments/` folder
4. Look at 2–3 sample chunks printed in the output. Write 1–2 sentences on whether they look complete and meaningful.
5. Fill in the "Finding" and "Decision" sections in Log 1.

**What to look for:**
- Election chunks should be 1–3 sentences each (a full row of data)
- Budget chunks should be full paragraphs (50–200 words)
- If any chunk seems cut mid-sentence, note it

---

## TEST 2 — Retrieval Failure Cases (Part B)
**Notebook:** `experiments/02_retrieval_failures.ipynb`

**Steps:**
1. Run all cells in order
2. **For the vague query "What happened in the north?":**
   - **Before fix:** Write down the top chunk's combined score and first 50 chars of text
   - **After fix:** Write down the new top chunk's score and source (election/budget)
   - Was the "after" result more relevant to northern Ghana election data? (Y/N — explain briefly)
3. **For the out-of-domain query "What is the capital of France?":**
   - Write down: `Is relevant (threshold ≥ 0.25): True/False`
   - Write down the top combined score — it should be very low (< 0.25)
4. Fill in Log 2 in `experiment_logs.md`

**What to look for:**
- Before fix: top result may be from budget (irrelevant to a "north" election query)
- After fix: top results should be from election data mentioning northern region
- Out-of-domain: `is_relevant` should print `False`

---

## TEST 3 — Prompt Template Comparison (Part C)
**Notebook:** `experiments/03_prompt_comparison.ipynb`

**Steps:**
1. Run all cells (this makes 3 separate LLM calls — takes ~30 seconds)
2. For query `"Who won the 2020 presidential election in Ghana?"`:
   - Copy the first 2 sentences of each template's response
   - **Template 1:** Does it add facts beyond the retrieved context? (Y/N)
   - **Template 2:** Does it explicitly say it only uses the context? (Y/N)
   - **Template 3:** Does the memory history (prior question about 2020 issues) affect the tone? (Y/N)
3. Run the context window cell — record: `Chunks before: ___`, `Chunks after: ___`, `Total chars: ___`
4. Fill in Log 3 in `experiment_logs.md`

**What to look for:**
- Template 1 may say things like "Nana Akufo-Addo won with approximately X%" — check if that exact number came from the context chunk
- Template 2 should be more cautious and stick strictly to what the chunk says
- Template 3 should reference or build on the prior turn about 2020 issues

---

## TEST 4 — Adversarial Tests (Part E)
**Notebook:** `experiments/04_adversarial_tests.ipynb`

### Query 1: "Who won?" (Ambiguous)

**Steps:**
1. Run the RAG cells for Q1
2. Record the RAG response (copy/paste first 3 sentences)
3. Record the pure LLM response (copy/paste first 3 sentences)
4. Answer these questions for Log 4:
   - RAG: Did it ask for clarification, refuse, or hallucinate a specific winner? ___
   - RAG: What was the top chunk score? ___
   - Pure LLM: Did it pick a specific winner without being asked about a year? ___
   - Pure LLM: Did it name a specific person/party without evidence? ___

**Expected behavior:**
- RAG should either return a low-confidence warning OR retrieve multiple possible "winners" from different years and present them
- Pure LLM will likely pick a recent winner (Mahama 2024 or Akufo-Addo 2020) from general knowledge — this is hallucination in the context of this application

### Query 2: "Free healthcare in the budget" (Misleading)

**Steps:**
1. Run the RAG cells for Q2
2. Record the RAG response
3. Record the pure LLM response
4. Answer these questions for Log 4:
   - RAG: Did the confidence threshold trigger (score < 0.25)? ___
   - RAG: Did it correctly say it has no information? ___
   - Pure LLM: Did it fabricate a quote from the president? ___
   - Pure LLM: Did it mention specific healthcare policies that aren't in the budget? ___

**Expected behavior:**
- RAG should refuse (confidence threshold) or retrieve budget chunks that don't mention healthcare, then say "insufficient information"
- Pure LLM will almost certainly hallucinate — it may invent a specific budget allocation for healthcare

---

## TEST 5 — Memory-based RAG (Part G Innovation)
**Run in the Streamlit UI app**

**Steps:**
1. Open the app in your browser
2. Make sure Template 3 is selected in the sidebar
3. Ask: `"Who won the 2020 presidential election?"`
4. Wait for the full response
5. Now ask: `"What about 2016?"`
6. Click the **📝 Final Prompt** expander on the second response
7. Scroll up in the prompt — you should see the first Q&A listed under "Conversation History:"

**Record in Log 5:**
- First response (first sentence): ___
- Second response (first sentence): ___
- Did the second prompt show the first Q&A in "Conversation History"? (Y/N) ___
- Did the second response correctly understand "2016" in the context of elections? (Y/N) ___

---

## TEST 6 — Adversarial Query in UI (optional, for video demo)
**Run in the Streamlit UI app**

Ask: `"What did the president say about free healthcare in the 2025 budget?"`

In the 📄 Retrieved Chunks panel:
- Note the combined scores — are they all below 0.25?
- Does the response say "I don't have enough information"?

This is a good clip for the 2-minute video.

---

## After All Tests Are Done

1. Go to `logs/experiment_logs.md` — fill in every `[Fill in]` with your actual observations
2. Make sure the tables have real numbers (chunk scores, counts)
3. Write the Summary table at the bottom
4. Apply the Humanize skill to the logs file before submitting:
   ```
   use humanizer skill to rewrite this academic documentation: [paste your log text]
   ```
5. Save everything and push to GitHub

---

## Checklist Before Submission

- [ ] `logs/experiment_logs.md` has real numbers from your runs (not placeholders)
- [ ] All 4 notebooks have **saved cell outputs** (run all + save in Jupyter)
- [ ] `experiments/chunking_distributions.png` exists
- [ ] App runs cleanly from `streamlit run app.py`
- [ ] GitHub repo is named `ai_10012200004`
- [ ] `godwin.danso@acity.edu.gh` added as collaborator on GitHub
- [ ] Deployed to Streamlit Community Cloud
- [ ] Email sent to godwin.danso@acity.edu.gh with subject: `CS4241-Introduction to Artificial Intelligence-2026:10012200004 Farima Konaré`
