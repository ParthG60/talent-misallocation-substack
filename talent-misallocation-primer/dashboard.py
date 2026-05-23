"""Substack primer — labour markets and the externality question.

Static single-page Streamlit app. Two illustrative charts (McDonald's janitor +
doctor vs. lobbyist) embedded as PNGs, plain-English prose, three expandable
explainers underneath.

Run with:  streamlit run dashboard.py
"""
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Labour market primer", layout="wide",
                   page_icon=":material/school:")

FIGS_DIR = Path(__file__).parent / "figures"

st.title("Labour markets, wages, and the externality question")
st.caption("How wages are set, and why the market price may not reflect social value.")

# ============================================================
# Section 1: McDonald's janitor
# ============================================================
st.markdown("## 1. How the market sets wages — a McDonald's janitor")

st.markdown(
    "Imagine McDonald's is hiring janitors. The wage they end up paying — and the number of people "
    "they hire — comes out of two opposing forces: a firm's *demand* for workers, and workers' "
    "*supply* of their time. Walk through each one in turn."
)

st.markdown(
    "**Demand comes from the firm.** McDonald's hires the *first* janitor for the dirtiest, most "
    "valuable work — the broken toilets, the spilled fryer oil. They'll pay quite a lot for that one. "
    "The *second* janitor does slightly less valuable work. By the *fifteenth* janitor, the floors are "
    "already clean — the next one is barely worth £8/hour. So as McDonald's hires more janitors, the "
    "value of each new one falls. Economists call this **diminishing marginal product**, and it's why "
    "**demand slopes down**."
)

st.markdown(
    "**Supply comes from workers.** Now flip the picture. A 16-year-old with no other option will "
    "work for **£8/hour** — it beats sitting at home. An experienced cleaner who could earn **£14/hour** "
    "at a hotel needs at least that much to switch. A trained electrician earning **£25/hour** "
    "elsewhere won't take the job at all. As the wage on offer rises, **more people are willing to be "
    "a janitor**. That's the **supply curve**, sloping up."
)

st.markdown(
    "Put both sides on the same chart and they cross at a single point. That crossing point is the "
    "**market wage W\\*** and the **number hired L\\***. Pay below W\\* and no one shows up; pay "
    "above it and too many people compete for too few slots."
)

st.image(str(FIGS_DIR / "janitor-market.png"), width="stretch")

# ============================================================
# Section 2: doctor vs lobbyist
# ============================================================
st.markdown("## 2. The market clears. But does it clear at the *right* number?")

st.markdown(
    "A market in equilibrium is not the same thing as a market in alignment with what's good for "
    "**society**. The supply and demand curves above only encode what the firm will pay and what "
    "workers will accept. They don't capture the value the work creates — or destroys — for everyone "
    "else. And that gap matters a lot. Two examples make it concrete."
)

st.markdown(
    "**A doctor** creates value far beyond what the hospital pays them. Each patient they vaccinate "
    "prevents downstream illness; the herd protection benefits everyone, including people who never "
    "stepped into the hospital. Society values the doctor's work at *more* than the hospital does, so "
    "**the market hires fewer doctors than society would**. That's a **positive externality**."
)

st.markdown(
    "**A corporate lobbyist** earns a high wage writing policy that quietly shifts profit from the "
    "public to one corporation. The corporation captures the gain — that's why they pay so well — but "
    "the public typically loses **more** than the corporation gains, once you count higher consumer "
    "prices, lost tax revenue, and worse regulation. Society values the lobbyist's work at *less* "
    "than the corporation does, so **the market hires more lobbyists than society would**. That's a "
    "**negative externality**."
)

st.image(str(FIGS_DIR / "externality-examples.png"), width="stretch")

st.markdown(
    "The two markers on the x-axis make the gap visible. The arrows tell you the direction: "
    "**society would want more doctors** than the market provides, and **fewer lobbyists** than it "
    "gets. Multiply that pattern across the whole economy and you get what we'll call **talent "
    "misallocation** — the central question of this post: which sectors are pulling the best minds "
    "of a generation toward work that creates value for society, and which are pulling them toward "
    "work that simply redistributes it?"
)

# ============================================================
# Explainers
# ============================================================
st.markdown("---")
st.markdown("### Dig deeper")

with st.expander("Why does demand for workers slope down? (more formally)"):
    st.markdown(
        "A firm hires the **most valuable** worker first — the one filling the obvious gap. "
        "The next worker is doing slightly less valuable work, the next slightly less, and so on. "
        "Each new worker adds a bit less revenue than the last (this is **diminishing marginal "
        "product**). So firms only hire more workers if the wage *falls* enough to make each new hire "
        "worthwhile. Demand slopes down."
    )

with st.expander("Why does supply of workers slope up? (more formally)"):
    st.markdown(
        "Different people have different **next-best options**. Someone whose alternative is "
        "unemployment will accept a low wage. Someone earning £100k elsewhere needs £100k+ to switch. "
        "As the wage rises, more people give up their alternatives and supply their labour. Supply "
        "slopes up."
    )

with st.expander("What's an externality, exactly?"):
    st.markdown(
        "An **externality** is a gap between the *private* value of an action and its *social* "
        "value — costs or benefits that fall on people who weren't part of the transaction.\n\n"
        "- **Negative externality**: a factory's pollution lands on the village downstream. The firm "
        "captures the revenue; the village pays the cost. Society values the output at less than the "
        "firm does.\n"
        "- **Positive externality**: a vaccine researcher's work benefits people who never paid for "
        "it. Society values the output at more than the firm does.\n\n"
        "When externalities exist, the market wage only reflects the firm's view. Society's view is "
        "different — and that gap drives the **misallocation** of workers between industries."
    )
