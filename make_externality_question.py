"""Static 'Market for a job — is this socially efficient?' figure for the Substack post.

Replaces the four-curve `labour-market-private-vs-social` chart with a deliberately
unresolved single-equilibrium chart: standard supply/demand, private equilibrium W*/L*
marked, and a literal `?` callout asking whether the market wage reflects social value.

The dashboard primer page (Primer tab in `dashboard.py`) is where the question gets
answered interactively.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

NAVY = "#1a3e72"
GREY = "#999999"

fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# Linear supply and demand — same parameters as make_labour_market_simple.py
L = np.linspace(0, 10, 200)
supply = 1 + 0.6 * L
demand = 7 - 0.6 * L

L_star = (7 - 1) / (0.6 + 0.6)   # 5
W_star = 1 + 0.6 * L_star         # 4

# Curves
ax.plot(L, supply, color=NAVY, linewidth=2.5)
ax.plot(L, demand, color=NAVY, linewidth=2.5)

# Equilibrium guide lines
ax.plot([L_star, L_star], [0, W_star], color=GREY, linestyle="--", linewidth=1, zorder=1)
ax.plot([0, L_star], [W_star, W_star], color=GREY, linestyle="--", linewidth=1, zorder=1)

# Equilibrium dot
ax.plot(L_star, W_star, "o", color=NAVY, markersize=10,
        markeredgecolor="white", markeredgewidth=1.5, zorder=5)

# Curve labels at right edge
ax.text(10.3, supply[-1], "Supply\n(workers)", color=NAVY, fontsize=11, va="center")
ax.text(10.3, demand[-1], "Demand\n(firm)", color=NAVY, fontsize=11, va="center")

# Axis tick labels
ax.text(-0.25, W_star, "W*", color=NAVY, fontsize=12, va="center", ha="right", fontweight="600")
ax.text(L_star, -0.35, "L*", color=NAVY, fontsize=12, ha="center", fontweight="600")

# === The hook: big question mark + callout ===
# Big translucent "?" in the empty upper-right area (above both curves), with
# a curving arrow back down to the equilibrium dot.
ax.text(8.6, 7.4, "?", color="#a8a8a8", fontsize=120, ha="center", va="center",
        alpha=0.55, fontweight="bold", zorder=4)

# Caption under the "?"
ax.text(8.6, 6.1, "Is this socially\nefficient?", color=NAVY, fontsize=13,
        ha="center", va="center", style="italic", zorder=4)

# Curved arrow from the caption back down to the equilibrium dot
ax.annotate("",
            xy=(L_star + 0.18, W_star + 0.18),         # arrow head — near the dot
            xytext=(7.85, 5.75),                       # arrow tail — under the "?"
            arrowprops=dict(arrowstyle="->",
                            color=NAVY,
                            connectionstyle="arc3,rad=0.3",
                            lw=1.5),
            zorder=4)

# Axes housekeeping
ax.set_xlim(0, 14.5)
ax.set_ylim(0, 8.5)
ax.set_xlabel("Labour", fontsize=12, labelpad=10)
ax.set_ylabel("Wage", fontsize=12, labelpad=30)
ax.set_xticks([])
ax.set_yticks([])
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color("#222")
ax.spines["bottom"].set_color("#222")

ax.set_title("Market for a job", fontsize=14, fontweight="600", pad=14)

# Footnote
fig.text(0.5, 0.06,
         "Demand = firm's value of the marginal worker.   Supply = worker's opportunity cost.",
         ha="center", fontsize=10, color="#444")
fig.text(0.5, 0.025,
         "W* is the market wage — but it only reflects private value (what the firm captures, what the worker accepts).",
         ha="center", fontsize=10, color="#444", style="italic")

plt.tight_layout(rect=[0, 0.1, 1, 1])

out_dir = Path(__file__).parent / "figures"
out_dir.mkdir(exist_ok=True)
out_png = out_dir / "labour-market-externality-question.png"
out_svg = out_dir / "labour-market-externality-question.svg"
fig.savefig(out_png, dpi=150, facecolor="white")
fig.savefig(out_svg, facecolor="white")
print(f"saved: {out_png}")
print(f"saved: {out_svg}")
