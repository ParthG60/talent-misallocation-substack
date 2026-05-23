"""Lucas (1978) / MSV profit-maximisation model — interactive sandbox + methodology.

Two pages:
- **Sandbox** — compare two sectors by their α parameter; live charts of profit and
  firm-size in talent; revenue-split breakdown.
- **Methodology** — setup, FOC, closed-form profit derivation.

Run with:  streamlit run dashboard.py
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

NAVY = "#1a3e72"
GOLD = "#c47e1d"
GREY = "#999999"


# ============================================================
# Helpers — closed-form objects from Lucas (1978)
# ============================================================
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


# ============================================================
# Sandbox page
# ============================================================
def sandbox_page():
    st.title("Lucas (1978) profit-maximisation sandbox")

    # --- Intro: explain what's on the page, write the equation, point to Methodology ---
    st.markdown(
        "A manager of ability **A** runs a firm and hires **H** workers at wage **w**. With a "
        "Cobb-Douglas production function $y = sAH^{\\alpha}$, the firm's profit-maximised value "
        "collapses to a closed form:"
    )
    st.latex(
        r"\pi^{*}(A) \;=\; (1 - \alpha)\,\left(\frac{\alpha}{w}\right)^{\!\alpha/(1-\alpha)}\,(sA)^{\!1/(1-\alpha)}"
    )
    st.markdown(
        "The exponent on talent **A** is **1/(1−α)**, so profit is *convex* in talent — and the "
        "steepness depends on α. The sliders in the sidebar let you compare two sectors with "
        "different α values and watch how that convexity drives the gap in top-tail pay."
    )
    st.markdown(
        "*For the derivation (FOC, closed-form algebra), see the **Methodology** page.*"
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
# Methodology page  (sections 1–4 only, plus references)
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

    st.markdown("---")
    st.markdown("### References")
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
    st.Page(sandbox_page, title="Sandbox", icon=":material/tune:", default=True),
    st.Page(methodology_page, title="Methodology", icon=":material/menu_book:"),
])
pg.run()
