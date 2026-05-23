"""Static labour-market figure for the dashboard Primer — McDonald's janitor example.

Section 1 of the Primer page uses this to show how demand and supply set the wage,
with intuitive annotations on each curve.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

NAVY = "#1a3e72"
GREY = "#999999"

fig, ax = plt.subplots(figsize=(9, 5.8), dpi=150)

L = np.linspace(0, 16, 200)
supply = 8 + 0.6 * L      # workers' opportunity cost
demand = 22 - 0.8 * L     # McDonald's' value of an extra janitor

L_star = (22 - 8) / (0.6 + 0.8)   # = 10
W_star = 8 + 0.6 * L_star          # = 14

ax.plot(L, supply, color=NAVY, linewidth=2.5)
ax.plot(L, demand, color=NAVY, linewidth=2.5)

# Equilibrium guides
ax.plot([L_star, L_star], [0, W_star], color=GREY, linestyle="--", linewidth=1, zorder=1)
ax.plot([0, L_star], [W_star, W_star], color=GREY, linestyle="--", linewidth=1, zorder=1)

# Equilibrium dot
ax.plot(L_star, W_star, "o", color=NAVY, markersize=11,
        markeredgecolor="white", markeredgewidth=1.5, zorder=5)

# Curve labels — at the right edge
ax.text(16.4, supply[-1], "Workers willing\nto take the job\n(Supply)",
        color=NAVY, fontsize=10, va="center")
ax.text(16.4, demand[-1], "McDonald's value\nof another janitor\n(Demand)",
        color=NAVY, fontsize=10, va="center")

# --- Supply side annotations ---
# Low-end: teenager
ax.annotate("Teenager with no other\njob — works for £8/hr",
            xy=(0.6, 8.4), xytext=(2.5, 3.5),
            color="#555", fontsize=9.5, ha="center",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))

# High-end: skilled worker needs more pay
ax.annotate("Experienced cleaner —\nneeds higher pay to switch",
            xy=(13.5, 16.1), xytext=(14.5, 12.0),
            color="#555", fontsize=9.5, ha="center",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))

# --- Demand side annotations ---
# Low-L: first janitor cleans most valuable mess
ax.annotate("1st janitor cleans the\ndirtiest, most valuable mess",
            xy=(0.6, 21.5), xytext=(4.0, 23.4),
            color="#555", fontsize=9.5, ha="center",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))

# High-L: 15th janitor cleans clean floors
ax.annotate("15th janitor cleans floors\nthat are already clean",
            xy=(15.0, 10.0), xytext=(13.5, 5.3),
            color="#555", fontsize=9.5, ha="center",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))

# Axis tick labels (sit clear of the y-axis label thanks to larger labelpad below)
ax.text(-0.8, W_star, "W*", color=NAVY, fontsize=12, va="center", ha="right", fontweight="600")
ax.text(L_star, -0.9, "L*", color=NAVY, fontsize=12, ha="center", fontweight="600")

# Equilibrium wage callout next to the dot
ax.text(L_star + 0.5, W_star + 0.4, "£14/hr",
        color=NAVY, fontsize=11, va="bottom", fontweight="600")

# Axes
ax.set_xlim(0, 21)
ax.set_ylim(0, 26)
ax.set_xlabel("Number of janitors hired", fontsize=11, labelpad=10)
ax.set_ylabel("Wage", fontsize=11, labelpad=32)
ax.set_xticks([])
ax.set_yticks([])
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color("#222")
ax.spines["bottom"].set_color("#222")

ax.set_title("Janitor market at McDonald's", fontsize=14, fontweight="600", pad=12)

fig.text(0.5, 0.04,
         "Equilibrium: supply meets demand. Below £14/hr no one shows up; above £14/hr McDonald's has too many applicants.",
         ha="center", fontsize=9.5, color="#444")

plt.tight_layout(rect=[0, 0.08, 1, 1])

out = Path(__file__).parent / "figures" / "janitor-market.png"
fig.savefig(out, dpi=150, facecolor="white")
fig.savefig(out.with_suffix(".svg"), facecolor="white")
print(f"saved: {out}")
print(f"saved: {out.with_suffix('.svg')}")
