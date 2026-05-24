"""Knowledge-work model of the economy — interactive sandbox + methodology.

Two pages:
- **Sandbox** — compare two sectors by their α parameter; live charts of profit
  and workforce-size in talent; revenue-split breakdown at two ability levels.
- **Methodology** — setup, solve for the workforce, plug back to get profit.

Run with:  streamlit run dashboard.py
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

NAVY = "#1a3e72"
GOLD = "#c47e1d"
GREY = "#999999"


# ============================================================
# Helpers — closed-form objects from the model
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


def line_fig(x, ys, names, colors, title, y_label):
    """Two-line log-y chart for π*(A) or H*(A) comparison across sectors."""
    fig = go.Figure()
    for y, name, color in zip(ys, names, colors):
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=name,
                                 line=dict(color=color, width=2.5)))
    fig.update_layout(
        title=title,
        xaxis_title="Manager ability A",
        yaxis_title=y_label,
        yaxis_type="log",
        height=380,
        margin=dict(l=60, r=40, t=60, b=50),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        plot_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eee", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eee", zeroline=False)
    return fig


def split_bar_fig(A_val, alpha1, alpha2, s, w):
    """Stacked-bar chart at a fixed A value: two bars (one per sector).
    Workforce (grey) on bottom, Manager (navy) on top. Linear scale.
    Annotates each bar with manager $ and manager share %.
    """
    labels = [f"Low-scalability<br>α = {alpha1:.2f}",
              f"High-scalability<br>α = {alpha2:.2f}"]
    wb1 = float(wage_bill(A_val, alpha1, s, w))
    mp1 = float(profit(A_val, alpha1, s, w))
    wb2 = float(wage_bill(A_val, alpha2, s, w))
    mp2 = float(profit(A_val, alpha2, s, w))
    rev1, rev2 = wb1 + mp1, wb2 + mp2
    share1 = mp1 / rev1 * 100.0 if rev1 > 0 else 0.0
    share2 = mp2 / rev2 * 100.0 if rev2 > 0 else 0.0

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Workforce", x=labels, y=[wb1, wb2],
                         marker_color=GREY))
    fig.add_trace(go.Bar(name="Manager", x=labels, y=[mp1, mp2],
                         marker_color=NAVY))

    annotations = [
        dict(x=labels[0], y=rev1,
             text=f"<b>Manager:</b> ${mp1:,.2f}<br>(share = {share1:.0f}%)",
             showarrow=False, yshift=24, font=dict(size=11, color="#222")),
        dict(x=labels[1], y=rev2,
             text=f"<b>Manager:</b> ${mp2:,.2f}<br>(share = {share2:.0f}%)",
             showarrow=False, yshift=24, font=dict(size=11, color="#222")),
    ]
    y_top = max(rev1, rev2) * 1.32 if max(rev1, rev2) > 0 else 1.0

    fig.update_layout(
        barmode="stack",
        title=f"At talent A = {A_val:g}",
        height=420,
        margin=dict(l=60, r=40, t=70, b=70),
        plot_bgcolor="white",
        yaxis_title="Dollars",
        yaxis=dict(range=[0, y_top]),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        annotations=annotations,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eee", zeroline=False)
    return fig


# ============================================================
# Sandbox page
# ============================================================
def sandbox_page():
    st.title("Knowledge work model of the economy")

    # --- Intro ---
    st.markdown(
        "A sector hires workers, and one talented person — call them the **manager** — runs the "
        "operation. We measure how scalable that talent is via a parameter **α**: how much output "
        "one talented person can be leveraged through their workforce."
    )
    st.markdown(
        "α also equals the **share of revenue that goes to the workforce**. The manager keeps the "
        "rest, **1 − α**. So a high-α sector means workers capture a big slice — but the operation "
        "scales hard around the rare talent."
    )
    st.markdown("The model gives two clean proportionalities:")
    st.latex(
        r"H^{*}(A) \;\propto\; A^{\,1/(1-\alpha)} \qquad \text{(workforce hired)}"
    )
    st.latex(
        r"\pi^{*}(A) \;\propto\; A^{\,1/(1-\alpha)} \qquad \text{(manager's profit)}"
    )
    st.markdown(
        "Both grow faster than the talent itself. The bigger α is, the more convex the growth — "
        "so high-scalability sectors capture the top of the talent distribution. The catch: even "
        "though workers keep a *bigger* share of revenue in those sectors, **the manager still earns "
        "more in absolute dollars**, because the pie itself is much larger."
    )
    st.markdown(
        "*Use the two sliders to compare a low-scalability sector and a high-scalability sector. "
        "For the algebra, see the Methodology page.*"
    )

    # --- Sidebar (two sliders only) ---
    st.sidebar.markdown("### Compare two sectors")
    alpha1 = st.sidebar.slider("Low-scalability sector  α₁",
                               min_value=0.10, max_value=0.95, value=0.70, step=0.01)
    alpha2 = st.sidebar.slider("High-scalability sector  α₂",
                               min_value=0.10, max_value=0.95, value=0.80, step=0.01)

    # Internal fixed parameters
    w = 1.0
    s = 1.0
    A_max = 100.0

    # --- Metric panels ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"##### Low-scalability sector  (α₁ = {alpha1:.2f})")
        m1, m2, m3 = st.columns(3)
        m1.metric("Workforce share α₁", f"{alpha1:.2f}")
        m2.metric("Manager share 1−α₁", f"{1.0 - alpha1:.2f}")
        m3.metric("Convexity 1/(1−α₁)", f"{conv_exp(alpha1):.2f}")
    with col_b:
        st.markdown(f"##### High-scalability sector  (α₂ = {alpha2:.2f})")
        n1, n2, n3 = st.columns(3)
        n1.metric("Workforce share α₂", f"{alpha2:.2f}")
        n2.metric("Manager share 1−α₂", f"{1.0 - alpha2:.2f}")
        n3.metric("Convexity 1/(1−α₂)", f"{conv_exp(alpha2):.2f}")

    # --- Compute curves ---
    A = np.linspace(1.0, A_max, 400)
    H1 = firm_size(A, alpha1, s, w)
    pi1 = profit(A, alpha1, s, w)
    H2 = firm_size(A, alpha2, s, w)
    pi2 = profit(A, alpha2, s, w)

    label_low = f"Low-scalability (α₁ = {alpha1:.2f})"
    label_high = f"High-scalability (α₂ = {alpha2:.2f})"

    # --- Profit line chart ---
    st.plotly_chart(
        line_fig(A, [pi1, pi2], [label_low, label_high],
                 [NAVY, GOLD],
                 title="Manager's profit as talent grows",
                 y_label="π*(A)  (log scale)"),
        width="stretch",
    )

    # --- Workforce line chart ---
    st.plotly_chart(
        line_fig(A, [H1, H2], [label_low, label_high],
                 [NAVY, GOLD],
                 title="Workforce hired as talent grows",
                 y_label="H*(A)  (log scale)"),
        width="stretch",
    )

    # --- Revenue split: two panels at low and high A ---
    st.markdown("### Where does the revenue go? Workforce vs. manager")

    A_low = 2.0
    A_high = 5.0
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(split_bar_fig(A_low, alpha1, alpha2, s, w), width="stretch")
    with c2:
        st.plotly_chart(split_bar_fig(A_high, alpha1, alpha2, s, w), width="stretch")

    st.caption(
        f"At A = {A_low:g} the two sectors are comparable. At A = {A_high:g} the high-scalability "
        "sector's pie is much larger — and even though workers keep a bigger share, the manager's "
        "absolute take is far bigger too."
    )


# ============================================================
# Methodology page
# ============================================================
def methodology_page():
    st.title("Methodology — the math behind the model")
    st.caption("This page derives the two proportionalities used on the Sandbox page.")

    st.markdown("## 1. The setup")
    st.markdown(
        "A manager with talent **A** runs a firm. They hire **H** workers at wage **w**. "
        "Output is scaled by economy-wide productivity **s** and by a production function **F(·)**. "
        "Revenue is the price of output (normalised to 1) times quantity, and profit is revenue "
        "minus the wage bill:"
    )
    st.latex(r"\pi(A; \alpha, s, w) \;=\; \underbrace{s \cdot A \cdot F(H)}_{\text{revenue}} \;-\; \underbrace{w \cdot H}_{\text{wage bill}}")

    st.markdown("## 2. Production function")
    st.markdown(
        "We assume diminishing returns to adding workers — one manager can run only so many people "
        "before each extra worker contributes less. The standard form is:"
    )
    st.latex(r"F(H) = H^{\alpha}, \quad 0 < \alpha < 1")
    st.markdown(
        "α is the **talent-scalability** parameter. It measures how much output one talented "
        "manager can amplify through the workforce they direct. α also turns out to equal the "
        "**workforce's share of revenue** — see §4."
    )
    st.latex(r"\pi(A; \alpha, s, w) \;=\; s \cdot A \cdot H^{\alpha} \;-\; w \cdot H")

    st.markdown("## 3. Solve for the workforce")
    st.markdown("The firm picks H to maximise profit. Differentiate π with respect to H and set to zero:")
    st.latex(r"\frac{\partial \pi}{\partial H} \;=\; s \cdot A \cdot \alpha \cdot H^{\alpha - 1} \;-\; w \;=\; 0")
    st.markdown("Solve for H:")
    st.latex(r"\boxed{\;H^{*}(A) \;=\; \left(\frac{\alpha \, s \, A}{w}\right)^{\!\!1/(1-\alpha)}\;}")
    st.markdown("This is plotted as the **workforce curve** in the sandbox.")

    st.markdown("## 4. Plug back to get profit")
    st.markdown("Substitute H\\*(A) into π. After algebra:")
    st.latex(
        r"\boxed{\;\pi^{*}(A) \;=\; (1 - \alpha) \cdot \left(\frac{\alpha}{w}\right)^{\!\!\alpha/(1-\alpha)} "
        r"\cdot (s \, A)^{\!1/(1-\alpha)}\;}"
    )
    st.markdown(
        "Three pieces, each with meaning:\n\n"
        "- **(1−α)** — the **manager's share of revenue**. Workforce gets α; manager keeps the rest.\n"
        "- **(α/w)^(α/(1−α))** — a **constant prefactor** depending on workforce share and wages, "
        "but not on A. Sets the level of profits in the economy; cancels out when comparing two "
        "managers in the same economy.\n"
        "- **(sA)^(1/(1−α))** — the **convex core**. Profit scales as talent raised to the convexity "
        "exponent. This is what drives the convex-pay-in-A result and why high-scalability sectors "
        "capture the top of the talent distribution."
    )

    st.markdown("---")
    st.markdown("*Original sources: Lucas (1978), Murphy-Shleifer-Vishny (1991), Baumol (1990).*")


# ============================================================
# App entry
# ============================================================
st.set_page_config(page_title="Knowledge work model", layout="wide")

pg = st.navigation([
    st.Page(sandbox_page, title="Sandbox", icon=":material/tune:", default=True),
    st.Page(methodology_page, title="Methodology", icon=":material/menu_book:"),
])
pg.run()
