"""Two-panel externality figure for the dashboard Primer.

Left: Doctor — positive externality (society values their work above what hospitals pay).
Right: Lobbyist — negative externality (society loses what the corporation gains).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

NAVY = "#1a3e72"
GREY = "#999999"
GREEN = "#3a7d44"
RED = "#a03030"

fig, (ax_doc, ax_lob) = plt.subplots(1, 2, figsize=(13.5, 6), dpi=150,
                                      gridspec_kw={"wspace": 0.22})

# --- Common ---
L = np.linspace(0, 10, 200)
supply = 1 + 0.6 * L
demand = 7 - 0.6 * L   # private demand for either sector
L_priv = (7 - 1) / (0.6 + 0.6)  # = 5
W_priv = 1 + 0.6 * L_priv        # = 4


def social_eq(ext, a=7.0, c=1.0, b=0.6, d=0.6):
    L_soc = ((1 + ext) * a - c) / ((1 + ext) * b + d)
    W_soc = c + d * L_soc
    return L_soc, W_soc


def panel(ax, ext, social_colour, sector_lower, demand_label, social_label,
          gap_phrase, title):
    social_demand = (1 + ext) * (7 - 0.6 * L)
    L_soc, W_soc = social_eq(ext)

    # Curves
    ax.plot(L, supply, color=GREY, linewidth=2.5, label="Supply (workers)")
    ax.plot(L, demand, color=NAVY, linewidth=2.5, label=demand_label)
    ax.plot(L, social_demand, color=social_colour, linewidth=2.5, linestyle="--",
            label=social_label)

    # Equilibrium dots
    ax.plot(L_priv, W_priv, "o", color=NAVY, markersize=12,
            markeredgecolor="white", markeredgewidth=1.5, zorder=5)
    ax.plot(L_soc, W_soc, "o", color=social_colour, markersize=12,
            markeredgecolor="white", markeredgewidth=1.5, zorder=5)

    # Vertical dotted guides from each equilibrium dot to the x-axis — lets the
    # eye trace each dot down to "how many workers"
    ax.plot([L_priv, L_priv], [0, W_priv], color=NAVY, linestyle=":",
            linewidth=1.4, alpha=0.65, zorder=2)
    ax.plot([L_soc, L_soc], [0, W_soc], color=social_colour, linestyle=":",
            linewidth=1.4, alpha=0.65, zorder=2)

    # Sit two coloured downward-triangle markers ON the x-axis directly under each
    # equilibrium dot — these are the "points on the graph" the reader anchors to.
    # Navy = market hires; the social colour (green/red) = society wants.
    ax.plot(L_priv, 0, "v", color=NAVY, markersize=14,
            markeredgecolor="white", markeredgewidth=1.5,
            clip_on=False, zorder=6)
    ax.plot(L_soc, 0, "v", color=social_colour, markersize=14,
            markeredgecolor="white", markeredgewidth=1.5,
            clip_on=False, zorder=6)

    # Gap arrow: single-headed, pointing FROM the market triangle TO the society
    # triangle. Direction encodes "society wants more" (rightward) or "fewer"
    # (leftward) — no need for the units in the text label.
    bracket_y = 1.8
    ax.annotate("", xy=(L_soc, bracket_y), xytext=(L_priv, bracket_y),
                arrowprops=dict(arrowstyle="-|>", color=social_colour, lw=2,
                                shrinkA=8, shrinkB=8,
                                mutation_scale=22))
    ax.text((L_priv + L_soc) / 2, bracket_y + 0.25, gap_phrase, color=social_colour,
            fontsize=11, ha="center", va="bottom", fontweight="700")

    # Axes
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(f"Number of {sector_lower}s hired", fontsize=11, labelpad=16)
    ax.set_ylabel("Wage", fontsize=11, labelpad=15)
    ax.set_title(title, fontsize=12.5, fontweight="600", pad=12)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#222")
    ax.spines["bottom"].set_color("#222")
    ax.legend(loc="upper right", frameon=False, fontsize=9.5)


# --- Doctor panel ---
panel(
    ax=ax_doc,
    ext=0.5,
    social_colour=GREEN,
    sector_lower="doctor",
    demand_label="Hospital pays (private)",
    social_label="Society values (social)",
    gap_phrase="missing doctors",
    title="Doctor — positive externality\n(society gains more than the hospital pays)",
)

# --- Lobbyist panel ---
panel(
    ax=ax_lob,
    ext=-0.5,
    social_colour=RED,
    sector_lower="lobbyist",
    demand_label="Corporation pays (private)",
    social_label="Society values (social)",
    gap_phrase="excess lobbyists",
    title="Lobbyist — negative externality\n(society loses what the corporation gains)",
)

fig.text(0.5, 0.03,
         "Each chart uses the same private market (navy line = what the firm pays, grey = workers willing). The dashed line is what society values per worker — higher for doctors, lower for lobbyists.",
         ha="center", fontsize=9.5, color="#444")

plt.tight_layout(rect=[0, 0.06, 1, 1])

out = Path(__file__).parent / "figures" / "externality-examples.png"
fig.savefig(out, dpi=150, facecolor="white")
fig.savefig(out.with_suffix(".svg"), facecolor="white")
print(f"saved: {out}")
print(f"saved: {out.with_suffix('.svg')}")
