"""
CS4241 — Introduction to Artificial Intelligence
Student: Farima Konaré | Index: 10012200004
Module: csv_loader.py — Load and clean the Ghana Election Results CSV.
"""

import os
import re
import pandas as pd
from typing import List, Dict, Any


RAW_CSV = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "Ghana_Election_Result.csv")


def _normalize_col(name: str) -> str:
    return re.sub(r"[\s\-]+", "_", name.strip().lower())


def load_and_clean(path: str = RAW_CSV) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    df.columns = [_normalize_col(c) for c in df.columns]

    critical = [c for c in df.columns if any(k in c for k in ("year", "party", "vote", "region", "seat"))]
    df = df.dropna(subset=critical if critical else df.columns[:3])
    df = df.reset_index(drop=True)

    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
    return df


def _row_to_text(row: pd.Series, columns: List[str]) -> str:
    """Convert a DataFrame row into a natural-language sentence for embedding."""
    def _get(keys):
        for k in keys:
            for col in columns:
                if col.lower().replace(" ", "_") == k or col.lower() == k:
                    val = row[col]
                    if not pd.isna(val) and str(val).strip():
                        return str(val).strip()
        return None

    year      = _get(["year"])
    candidate = _get(["candidate"])
    party     = _get(["party"])
    votes     = _get(["votes"])
    votes_pct = _get(["votes(%)"])
    region    = _get(["old_region", "new_region", "region"])

    if candidate and year and party:
        return (
            f"In the {year} Ghana presidential election, {candidate} of the {party} party"
            f" received {votes} votes ({votes_pct}) in {region}."
        )

    # Fallback: generic key-value format
    parts = []
    for col in columns:
        val = row[col]
        if pd.isna(val) or str(val).strip() == "":
            continue
        parts.append(f"{col.replace('_', ' ').title()}: {val}")
    return " | ".join(parts)


def to_documents(df: pd.DataFrame) -> List[Dict[str, Any]]:
    docs = []
    cols = list(df.columns)
    for idx, row in df.iterrows():
        text = _row_to_text(row, cols)
        if not text.strip():
            continue
        meta: Dict[str, Any] = {"source": "election", "row_id": int(idx)}
        for key in ("year", "region", "constituency", "party"):
            match = next((c for c in cols if key in c), None)
            if match and not pd.isna(row[match]):
                meta[key] = row[match]
        docs.append({"text": text, "metadata": meta})
    return docs


def _national_summaries(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Add one national-total summary document per election year."""
    docs = []
    df2 = df.copy()
    # normalise column names for aggregation
    vote_col = next((c for c in df2.columns if "vote" in c and "%" not in c), None)
    year_col  = next((c for c in df2.columns if "year" in c), None)
    party_col = next((c for c in df2.columns if "party" in c), None)
    cand_col  = next((c for c in df2.columns if "candidate" in c), None)
    if not all([vote_col, year_col, party_col, cand_col]):
        return docs

    df2[vote_col] = pd.to_numeric(df2[vote_col], errors="coerce")
    totals = (
        df2.groupby([year_col, party_col, cand_col])[vote_col]
        .sum()
        .reset_index()
        .sort_values([year_col, vote_col], ascending=[True, False])
    )

    # Known winners (handles 2008 run-off which CSV first-round data misrepresents)
    known_winners = {
        1992: "Jerry John Rawlings", 1996: "J. J. Rawlings",
        2000: "J. A. Kuffour",       2004: "J. A. Kuffour",
        2008: "J. A Mills",          2012: "John Dramani Mahama",
        2016: "Nana Akufo Addo",     2020: "Nana Akufo Addo",
    }

    for year, grp in totals.groupby(year_col):
        rows = grp.reset_index(drop=True)
        winner_name = known_winners.get(int(year))
        if winner_name:
            winner_row = rows[rows[cand_col].str.contains(winner_name.split()[0], case=False, na=False)]
            if winner_row.empty:
                winner_row = rows.iloc[[0]]
        else:
            winner_row = rows.iloc[[0]]

        winner = winner_row.iloc[0]
        lines = [
            f"In the {year} Ghana presidential election, {winner[cand_col]} of the "
            f"{winner[party_col]} party won the election nationally with "
            f"{int(winner[vote_col]):,} total votes."
        ]
        # Add all candidates' national totals
        for _, r in rows.iterrows():
            lines.append(
                f"{r[cand_col]} ({r[party_col]}) received {int(r[vote_col]):,} total votes nationwide in {year}."
            )
        text = " ".join(lines)
        docs.append({
            "text": text,
            "metadata": {"source": "election", "year": int(year), "summary": True},
        })
    return docs


def load_election_documents(path: str = RAW_CSV) -> List[Dict[str, Any]]:
    df = load_and_clean(path)
    return to_documents(df) + _national_summaries(df)


if __name__ == "__main__":
    docs = load_election_documents()
    print(f"Loaded {len(docs)} election documents")
    if docs:
        print("Sample:", docs[0])
