"""Interactive sandbox for the Lucas (1978) / MSV profit-maximisation model.

Run with:  streamlit run projects/talent-misallocation/dashboard.py

Closed-form objects:
  H*(A) = (alpha * s * A / w) ** (1 / (1 - alpha))
  pi*(A) = (1 - alpha) * (alpha / w) ** (alpha / (1 - alpha)) * (s * A) ** (1 / (1 - alpha))
"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

NAVY = "#1a3e72"
GOLD = "#c47e1d"
GREY = "#999999"


def firm_size(A, alpha, s, w):
    return (alpha * s * A / w) ** (1.0 / (1.0 - alpha))


def profit(A, alpha, s, w):
    return (1.0 - alpha) * (alpha / w) ** (alpha / (1.0 - alpha)) * (s * A) ** (1.0 / (1.0 - alpha))


def revenue(A, alpha, s, w):
    H = firm_size(A, alpha, s, w)
    return s * A * H ** alpha


def wage_bill(A, alpha, s, w):
    return w * firm_size(A, alpha, s, w)


def conv_exp(a):
    return 1.0 / (1.0 - a)


def doubling(a):
    return 2.0 ** conv_exp(a)


def line_fig(x, ys, names, colors, title, y_label, log_y=True):
    fig = go.Figure()
    for y, name, color in zip(ys, names, colors):
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=name,
                                 line=dict(color=color, width=2.5)))
    fig.update_layout(
        title=title,
        xaxis_title="Manager ability A",
        yaxis_title=y_label,
        yaxis_type="log" if log_y else "linear",
        height=380,
        margin=dict(l=60, r=40, t=60, b=50),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        plot_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eee", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eee", zeroline=False)
    return fig


def safe_range(lo, hi, default_lo, default_hi, label):
    if lo >= hi:
        st.sidebar.warning(f"{label}: min ≥ max, using defaults ({default_lo}, {default_hi}).")
        return default_lo, default_hi
    return lo, hi


def clamp_default(default, lo, hi):
    return float(min(max(default, lo), hi))


# ============================================================
# Primer page — labour markets and the externality question
# Static page: two illustrative charts + prose + expandable explainers.
# ============================================================
FIGS_DIR = Path(__file__).parent / "figures"


def labour_market_primer_page():
    st.title("Labour markets, wages, and the externality question")
    st.caption("How wages are set, and why the market price may not reflect social value.")

    # ---- Section 1: McDonald's janitor ----
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

    # ---- Section 2: doctor vs lobbyist ----
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

    # ---- Explainers ----
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



# ============================================================
# Sandbox page
# ============================================================
def sandbox_page():
    st.title("Lucas (1978) / MSV profit-maximisation sandbox")
    st.caption(
        r"$\pi^*(A) = (1-\alpha)\left(\frac{\alpha}{w}\right)^{\alpha/(1-\alpha)} (sA)^{1/(1-\alpha)}$"
        r"$\quad\quad H^*(A) = \left(\frac{\alpha s A}{w}\right)^{1/(1-\alpha)}$"
    )

    # ---------- sidebar: range customisation ----------
    with st.sidebar.expander("Advanced: slider ranges", expanded=False):
        st.caption("Override the min/max of each slider below.")
        alpha_min = st.number_input("α min", value=0.10, min_value=0.01, max_value=0.99, step=0.01, format="%.2f")
        alpha_max = st.number_input("α max", value=0.95, min_value=0.01, max_value=0.99, step=0.01, format="%.2f")
        w_min = st.number_input("w min", value=0.5, min_value=0.01, step=0.1, format="%.2f")
        w_max = st.number_input("w max", value=5.0, min_value=0.02, step=0.1, format="%.2f")
        s_min = st.number_input("s min", value=0.5, min_value=0.01, step=0.1, format="%.2f")
        s_max = st.number_input("s max", value=5.0, min_value=0.02, step=0.1, format="%.2f")
        Amax_min = st.number_input("A range max — slider min", value=10, min_value=2, step=1)
        Amax_max = st.number_input("A range max — slider max", value=200, min_value=3, step=10)

    alpha_min, alpha_max = safe_range(alpha_min, alpha_max, 0.10, 0.95, "α range")
    w_min, w_max = safe_range(w_min, w_max, 0.5, 5.0, "w range")
    s_min, s_max = safe_range(s_min, s_max, 0.5, 5.0, "s range")
    Amax_min, Amax_max = safe_range(Amax_min, Amax_max, 10, 200, "A range")

    # ---------- sidebar: parameter inputs (typeable) ----------
    st.sidebar.markdown("### Parameters")
    st.sidebar.caption("Type a value or use the ± steppers. Bounds come from the Advanced expander.")

    def typed_number(label, lo, hi, default, step, fmt, key, is_int=False):
        """Full-width number input. Tolerates dynamic min/max by clamping the
        pre-existing session value into the current [lo, hi] range before render.
        """
        cast = int if is_int else float
        lo_c, hi_c = cast(lo), cast(hi)
        default_c = cast(min(max(default, lo_c), hi_c))

        if key not in st.session_state:
            st.session_state[key] = default_c
        else:
            cur = cast(st.session_state[key])
            clamped = max(lo_c, min(hi_c, cur))
            if clamped != cur:
                st.session_state[key] = clamped

        if is_int:
            return st.sidebar.number_input(label, min_value=lo_c, max_value=hi_c,
                                           step=int(step), key=key)
        return st.sidebar.number_input(label, min_value=lo_c, max_value=hi_c,
                                       step=float(step), format=fmt, key=key)

    alpha1 = typed_number("α₁  (sector 1 span of control)", alpha_min, alpha_max, 0.65, 0.01, "%.2f", "alpha1")
    alpha2 = typed_number("α₂  (sector 2 span of control)", alpha_min, alpha_max, 0.85, 0.01, "%.2f", "alpha2")
    w = typed_number("w  (wage)", w_min, w_max, 1.0, 0.1, "%.2f", "w")
    s = typed_number("s  (technology)", s_min, s_max, 1.0, 0.1, "%.2f", "s")
    A_max = typed_number("A range max", Amax_min, Amax_max, 100, 1, "%d", "A_max", is_int=True)

    st.sidebar.markdown("---")
    yscale = st.sidebar.radio("Y-axis scale", ["log", "linear"], horizontal=True, index=0,
                              help="Toggle the y-axis between log and linear scaling on the line charts.")
    log_y = (yscale == "log")

    # ---------- compute ----------
    A = np.linspace(1.0, float(A_max), 400)
    H1 = firm_size(A, alpha1, s, w)
    pi1 = profit(A, alpha1, s, w)
    H2 = firm_size(A, alpha2, s, w)
    pi2 = profit(A, alpha2, s, w)

    # ---------- metrics ----------
    st.markdown(f"##### Sector 1  (α₁ = {alpha1:.2f})")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Convexity exponent  1/(1−α₁)", f"{conv_exp(alpha1):.2f}")
    m2.metric("Doubling factor on π  2^(1/(1−α₁))", f"{doubling(alpha1):.2f}×")
    m3.metric("Labour share  α₁", f"{alpha1:.2f}")
    m4.metric("Manager share  1−α₁", f"{1.0 - alpha1:.2f}")

    st.markdown(f"##### Sector 2  (α₂ = {alpha2:.2f})")
    n1, n2, n3, n4 = st.columns(4)
    n1.metric("Convexity exponent  1/(1−α₂)", f"{conv_exp(alpha2):.2f}")
    n2.metric("Doubling factor on π  2^(1/(1−α₂))", f"{doubling(alpha2):.2f}×")
    n3.metric("Labour share  α₂", f"{alpha2:.2f}")
    n4.metric("Manager share  1−α₂", f"{1.0 - alpha2:.2f}")

    y_suffix = "(log scale)" if log_y else "(linear scale)"

    # ---------- profit chart ----------
    st.plotly_chart(
        line_fig(A,
                 [pi1, pi2],
                 [f"α₁ = {alpha1:.2f}", f"α₂ = {alpha2:.2f}"],
                 [NAVY, GOLD],
                 title=f"Profit  π*(A)   —   1/(1−α₁) = {conv_exp(alpha1):.2f}   ·   1/(1−α₂) = {conv_exp(alpha2):.2f}",
                 y_label=f"π*(A)  {y_suffix}",
                 log_y=log_y),
        width="stretch",
    )

    # ---------- firm size chart ----------
    st.plotly_chart(
        line_fig(A,
                 [H1, H2],
                 [f"α₁ = {alpha1:.2f}", f"α₂ = {alpha2:.2f}"],
                 [NAVY, GOLD],
                 title="Firm size  H*(A)",
                 y_label=f"H*(A)  {y_suffix}",
                 log_y=log_y),
        width="stretch",
    )

    # ---------- revenue split at median A ----------
    A_mid = float(A_max) / 2.0
    labour_1 = float(wage_bill(A_mid, alpha1, s, w))
    manager_1 = float(profit(A_mid, alpha1, s, w))
    rev_1 = float(revenue(A_mid, alpha1, s, w))
    labour_2 = float(wage_bill(A_mid, alpha2, s, w))
    manager_2 = float(profit(A_mid, alpha2, s, w))
    rev_2 = float(revenue(A_mid, alpha2, s, w))

    st.markdown(f"### Revenue split at A = {A_mid:.0f}")

    split_fig = go.Figure()
    split_fig.add_trace(go.Bar(name="Labour share",
                               x=[f"α₁ = {alpha1:.2f}", f"α₂ = {alpha2:.2f}"],
                               y=[labour_1, labour_2], marker_color=GREY))
    split_fig.add_trace(go.Bar(name="Manager share",
                               x=[f"α₁ = {alpha1:.2f}", f"α₂ = {alpha2:.2f}"],
                               y=[manager_1, manager_2], marker_color=NAVY))

    split_fig.update_layout(
        barmode="stack",
        height=380,
        margin=dict(l=60, r=40, t=20, b=50),
        plot_bgcolor="white",
        yaxis_title=f"Dollars at A = {A_mid:.0f}  {y_suffix}",
        yaxis_type="log" if log_y else "linear",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )
    split_fig.update_xaxes(showgrid=False)
    split_fig.update_yaxes(showgrid=True, gridcolor="#eee", zeroline=False)
    st.plotly_chart(split_fig, width="stretch")

    st.caption(
        f"At A = {A_mid:.0f}  ·  "
        f"α₁: revenue = {rev_1:.2f}, labour = {labour_1:.2f}, profit = {manager_1:.2f}  ·  "
        f"α₂: revenue = {rev_2:.2f}, labour = {labour_2:.2f}, profit = {manager_2:.2f}"
    )


# ============================================================
# Methodology page
# ============================================================
def methodology_page():
    st.title("Methodology — the model behind the dashboard")
    st.caption(
        "Lucas (1978) span-of-control model, used downstream by Murphy-Shleifer-Vishny (1991) "
        "to formalise the allocation of talent across sectors."
    )

    st.markdown("## 1. Setup")
    st.markdown(
        "A manager with ability **A** runs a firm. They hire **H** units of labour at wage **w**. "
        "Output is scaled by economy-wide technology **s** and by the production function **F(·)**. "
        "Revenue is the price of output (normalised to 1) times quantity."
    )
    st.latex(r"\pi(A; \alpha, s, w) \;=\; \underbrace{s \cdot A \cdot F(H)}_{\text{revenue}} \;-\; \underbrace{w \cdot H}_{\text{wage bill}}")

    st.markdown("## 2. Lucas's specialisation: F(H) = H^α")
    st.markdown(
        "Lucas (1978) showed that the **unique** functional form for F(·) consistent with "
        "**Gibrat's law** (firm growth rates independent of size) is the Cobb-Douglas form:"
    )
    st.latex(r"F(H) = H^{\alpha}, \quad 0 < \alpha < 1")
    st.markdown(
        "α is the **span of control parameter**. It measures how scalable a person's talent is — "
        "how much output one manager can amplify through the workforce they direct."
    )
    st.latex(r"\pi(A; \alpha, s, w) \;=\; s \cdot A \cdot H^{\alpha} \;-\; w \cdot H")

    st.markdown("## 3. First-order condition (firm size)")
    st.markdown("Maximise profit over H:")
    st.latex(r"\frac{\partial \pi}{\partial H} \;=\; s \cdot A \cdot \alpha \cdot H^{\alpha - 1} \;-\; w \;=\; 0")
    st.markdown("Solve for H:")
    st.latex(r"\boxed{\;H^{*}(A) \;=\; \left(\frac{\alpha \, s \, A}{w}\right)^{\!\!1/(1-\alpha)}\;}")
    st.markdown("This is plotted as the **firm-size curve** in the sandbox.")

    st.markdown("## 4. Closed-form profit")
    st.markdown("Plug H\\*(A) back into π. After algebra:")
    st.latex(
        r"\boxed{\;\pi^{*}(A) \;=\; (1 - \alpha) \cdot \left(\frac{\alpha}{w}\right)^{\!\!\alpha/(1-\alpha)} "
        r"\cdot (s \, A)^{\!1/(1-\alpha)}\;}"
    )
    st.markdown(
        "Three pieces, each with meaning:\n\n"
        "- **(1−α)** — the **manager's share of revenue**. Labour gets α; the manager keeps the residual.\n"
        "- **(α/w)^(α/(1−α))** — a **constant prefactor** depending on labour share and wages, but not on A. "
        "Sets the level of profits in the economy; cancels out when comparing two managers in the same economy.\n"
        "- **(sA)^(1/(1−α))** — the **convex core**. Profit scales as ability raised to the convexity exponent. "
        "This is what drives the convex-pay-in-A result and why high-α sectors capture the top tail."
    )

    st.markdown("## 5. Why labour gets share α")
    st.markdown(
        "Workers are paid their **marginal product** at the firm's optimum. For F(H) = H^α:"
    )
    st.latex(r"\text{MPL} \;=\; \frac{\partial y}{\partial H} \;=\; \alpha \cdot s \cdot A \cdot H^{\alpha-1} \;=\; \alpha \cdot \frac{y}{H}")
    st.markdown("Total wage bill:")
    st.latex(r"w \cdot H \;=\; \text{MPL} \cdot H \;=\; \alpha \cdot y")
    st.markdown(
        "So **labour collectively earns share α of revenue**. The manager keeps the residual — share **(1−α)**. "
        "It's mechanical: the exponent on the labour input becomes its revenue share."
    )

    st.markdown("## 6. The convexity exponent  1/(1−α)")
    st.markdown(
        "Profit scales as A^(1/(1−α)). Doubling A multiplies profit by 2^(1/(1−α))."
    )
    st.latex(
        r"\begin{array}{c|c|c|c} \alpha & 1/(1-\alpha) & \text{Doubling factor} & \text{Sector feel} \\ \hline "
        r"0.4 & 1.67 & 3.2\times & \text{Dentistry, plumbing} \\ "
        r"0.5 & 2.00 & 4.0\times & \text{Restaurants, retail} \\ "
        r"0.7 & 3.33 & 10.1\times & \text{Mid-sized firms} \\ "
        r"0.8 & 5.00 & 32\times & \text{Software, biotech} \\ "
        r"0.9 & 10.0 & 1024\times & \text{Hedge funds, top finance} "
        r"\end{array}"
    )

    st.markdown("## 7. What the sliders control")
    st.markdown(
        "- **α (span of control)** — the structural elasticity. The deepest parameter; Lucas-derived "
        "as the Cobb-Douglas exponent consistent with Gibrat's law. Sets convexity 1/(1−α), labour share α, "
        "and manager share (1−α).\n"
        "- **w (wage)** — the price of one efficiency unit of labour. Treated as exogenous here; in MSV's full "
        "model it's pinned down by labour-market clearing across all firms.\n"
        "- **s (technology)** — economy-wide tech level. Multiplies A in all expressions, so doubling s = "
        "doubling A in effect.\n"
        "- **A (ability range)** — the manager's individual talent. The x-axis on the line charts."
    )

    st.markdown("## 8. Empirical calibration of the defaults")
    st.markdown(
        "**α is the only parameter with a real empirical anchor.** w and s are normalisations — only "
        "the ratio sA/w shows up in the equations, so two of the three are free. We fix w = 1 and s = 1 "
        "by convention (this is what Lucas, MSV, and the calibration literature do)."
    )
    st.markdown(
        "**Defaults for α** are chosen to highlight the post's central contrast — productive economy vs "
        "rent-extracting/scalable sector:"
    )
    st.markdown(
        "| Param | Default | Empirical anchor |\n"
        "|---|---|---|\n"
        "| **α₁** | 0.65 | US aggregate labour share. \"Productive economy\" baseline. |\n"
        "| **α₂** | 0.85 | Lucas (1978) calibration; Restuccia-Rogerson (2008), Atkeson-Kehoe (2005). Finance, software, professional services. |\n"
        "| w | 1.00 | Normalisation. |\n"
        "| s | 1.00 | Normalisation. |\n"
        "| A_max | 100 | ~100× ratio of top-tail to median ability — consistent with Pareto talent distribution (Zipf, ξ ≈ 1). |"
    )
    st.markdown(
        "**Cross-sector α (rough estimates from the productivity / firm-size literature):**"
    )
    st.markdown(
        "| Sector | α | Convexity 1/(1−α) | Doubling factor |\n"
        "|---|---|---|---|\n"
        "| Dentistry, plumbing, restaurants | 0.40–0.50 | 1.7–2.0 | 3–4× |\n"
        "| Manufacturing, retail | 0.60–0.70 | 2.5–3.3 | 6–10× |\n"
        "| Software, biotech, prof. services | 0.80–0.85 | 5.0–6.7 | 32–100× |\n"
        "| Hedge funds, top consulting, PE | 0.90–0.95 | 10–20 | 1,000×+ |"
    )
    st.markdown(
        "The 2.3× ratio of convexity exponents between α₁ = 0.65 (2.86) and α₂ = 0.85 (6.67) is the "
        "wedge that drives MSV's \"top tail flows to high-α sector\" sorting result."
    )

    st.markdown("## 9. What's *not* in this dashboard (yet)")
    st.markdown(
        "- **Labour-market clearing** (MSV Eq 4): the integral that pins down w endogenously across the talent "
        "distribution.\n"
        "- **Two-sector model**: comparing a productive sector (high α) with rent-seeking (potentially also "
        "high α via a different concavity), MSV Eqs (5)–(6).\n"
        "- **Talent distribution**: Pareto f(A) integrated to get aggregate income, top-decile shares, etc.\n"
        "- **Technology growth**: s evolving over time (MSV Eq 5)."
    )

    st.markdown("## References")
    st.markdown(
        "- Lucas, R. E. (1978). \"On the Size Distribution of Business Firms.\" "
        "*Bell Journal of Economics* 9(2): 508–523.\n"
        "- Murphy, K. M., Shleifer, A., & Vishny, R. W. (1991). \"The Allocation of Talent: Implications for Growth.\" "
        "*Quarterly Journal of Economics* 106(2): 503–530.\n"
        "- Baumol, W. J. (1990). \"Entrepreneurship: Productive, Unproductive, and Destructive.\" "
        "*Journal of Political Economy* 98(5): 893–921."
    )


# ============================================================
# App entry
# ============================================================
st.set_page_config(page_title="Lucas / MSV sandbox", layout="wide")

pg = st.navigation([
    st.Page(labour_market_primer_page, title="Primer", icon=":material/school:", default=True),
    st.Page(sandbox_page, title="Sandbox", icon=":material/tune:"),
    st.Page(methodology_page, title="Methodology", icon=":material/menu_book:"),
])
pg.run()
