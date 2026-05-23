# Talent misallocation — Lucas / MSV model sandbox

Interactive companion to the Substack post *The Great Talent Misallocation*. Lets a reader
play with the Lucas (1978) span-of-control parameter α and watch how convexity in talent
drives firm size, profit, and the labour/manager revenue split.

Two pages:

- **Sandbox** — sliders for α₁, α₂, w, s. Live charts of π*(A) and H*(A) in talent, plus
  the labour-vs-manager revenue split bar chart.
- **Methodology** — Setup → Lucas's F(H) = H^α → FOC for firm size → closed-form profit.
  Math derivation only; sections 1–4.

## Run locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
