from pathlib import Path
import matplotlib.pyplot as plt

labels = [
    "Policy-check\ncoverage",
    "Typed-tool\ncoverage",
    "Replayable\nrun coverage",
    "Failure traceability\nimprovement",
    "Audit-event\ndelivery target",
]
values = [95, 90, 80, 70, 99.5]
colors = ["#ff7a00", "#ff963d", "#9d72ff", "#35d0ba", "#ffd166"]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titleweight": "bold",
})
fig, ax = plt.subplots(figsize=(10, 5.4), dpi=180)
fig.patch.set_facecolor("#0d1016")
ax.set_facecolor("#0d1016")
bars = ax.bar(labels, values, color=colors, width=0.64)
ax.set_ylim(0, 110)
ax.set_ylabel("Target (%)", color="#f6f7fb")
ax.set_title("ZK Theta reference implementation — illustrative design targets", color="#f6f7fb", pad=18)
ax.grid(axis="y", color="#303642", linewidth=0.7, alpha=0.7)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_color("#3a404c")
ax.tick_params(colors="#d6d9e0")
ax.yaxis.label.set_color("#d6d9e0")
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, value + 2, f"{value:g}%", ha="center", va="bottom", color="#f6f7fb", fontweight="bold")
fig.text(0.01, 0.01, "Illustrative targets for evaluation planning; not measured production results.", color="#9da5b4", fontsize=8)
fig.tight_layout(rect=[0, 0.04, 1, 1])
out = Path(__file__).parent / "illustrative-targets.png"
fig.savefig(out, facecolor=fig.get_facecolor(), bbox_inches="tight")
