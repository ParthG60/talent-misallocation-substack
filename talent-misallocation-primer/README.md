# Talent misallocation — labour-market primer

Static companion page to the Substack post *The Great Talent Misallocation*. Aimed at
non-economist readers — explains how supply and demand set wages (via a McDonald's
janitor example) and introduces the externality concept (doctor vs. lobbyist).

Single page, no interactive controls. The visual story does the heavy lifting via two
embedded charts.

## Run locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Regenerating the figures

The `make_*.py` scripts produce the PNGs in `figures/` using matplotlib. Edit and re-run
them if you want to tweak labels or styling.
