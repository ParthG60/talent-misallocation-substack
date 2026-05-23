"""Simple labour market supply & demand (MPC / MPB) figure."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

NAVY = "#1a3e72"
GREY = "#999999"

fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# Linear supply and demand
L = np.linspace(0, 10, 200)
supply = 1 + 0.6 * L        # MPC — upward sloping
demand = 7 - 0.6 * L        # MPB — downward sloping

# Equilibrium
L_star = (7 - 1) / (0.6 + 0.6)   # = 5
W_star = 1 + 0.6 * L_star         # = 4

W_high = 6.0
W_low = 2.0

# Supply & demand
ax.plot(L, supply, color=NAVY, linewidth=2.5)
ax.plot(L, demand, color=NAVY, linewidth=2.5)

# Equilibrium guides (light)
ax.plot([L_star, L_star], [0, W_star], color=GREY, linestyle="--", linewidth=1, zorder=1)
ax.plot([0, L_star], [W_star, W_star], color=GREY, linestyle="--", linewidth=1, zorder=1)

# W_high and W_low guides (light) — only span to where they hit the nearer curve
L_high_s = (W_high - 1) / 0.6    # supply
L_low_d = (7 - W_low) / 0.6      # demand
ax.plot([0, L_high_s], [W_high, W_high], color=GREY, linestyle="--", linewidth=1, zorder=1)
ax.plot([0, L_low_d], [W_low, W_low], color=GREY, linestyle="--", linewidth=1, zorder=1)

# Equilibrium point
ax.plot(L_star, W_star, "o", color=NAVY, markersize=9,
        markeredgecolor="white", markeredgewidth=1.5, zorder=5)

# Curve labels — short; full forms defined in footnote
ax.text(10.3, supply[-1], "Supply (MPC)", color=NAVY, fontsize=11, va="center")
ax.text(10.3, demand[-1], "Demand (MPB)", color=NAVY, fontsize=11, va="center")

# Wage tick labels on y-axis
ax.text(-0.25, W_star, "W*", color=NAVY, fontsize=12, va="center", ha="right", fontweight="600")
ax.text(-0.25, W_high, r"$W_{high}$", color=NAVY, fontsize=12, va="center", ha="right", fontweight="600")
ax.text(-0.25, W_low, r"$W_{low}$", color=NAVY, fontsize=12, va="center", ha="right", fontweight="600")

# L* label on x-axis
ax.text(L_star, -0.35, "L*", color=NAVY, fontsize=12, ha="center", fontweight="600")

# Axes
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

# Two-line footnote: full definitions of MPB and MPC
fig.text(0.5, 0.04,
         "MPB (Marginal Private Benefit) = firm's value of the marginal worker",
         ha="center", fontsize=10, color="#444")
fig.text(0.5, 0.015,
         "MPC (Marginal Private Cost) = worker's opportunity cost of the marginal hour",
         ha="center", fontsize=10, color="#444")

plt.tight_layout(rect=[0, 0.08, 1, 1])

out = Path(__file__).parent / "figures" / "labour-market-simple.png"
fig.savefig(out, dpi=150, facecolor="white")
print(f"saved: {out}")
