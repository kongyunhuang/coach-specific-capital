"""
abstract_fig2_fullpage.py — 摘要图 2：装机工期，整页版
============================
内容与正稿图 4（fig4_installation.py）相同，数据逐行照搬，只改版式。摘要 PDF 里图 2 独占一页，所以画布拉到整页，
a 放大占满上方整宽，b、c 在左下，d（21 次换帅逐个）在右下占两行高。所有文字标注移出数据区，改成图例或放在
没有数据的位置（a 的 +0.49 放在换帅竖线与第 1 场之间的空白里），不再压住线条和柱子；图注只剩标题，
所以把 0 和 1 的含义、虚线的含义都写进坐标轴标题和图例。不写任何 results 文件。

输入: results/adoption_index_FINAL.csv, adoption_index_FINAL.json, install_event_curves.csv, install_jump_placebo.json,
      install_jump_placebo_null.npz, install_curve_diagnostics.json, sensitivity_install.csv, sensitivity_install.json
输出: figures/abstract_fig2_fullpage.png

Usage: conda activate kronos && python code/abstract_fig2_fullpage.py
Last modified: 2026-09-28（c 的两条虚线分开线型并在图例写明是前 5 场、前 10 场平均的跳变）
"""
import json, sys
import numpy as np, pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
RES, FIG = ROOT/"results", ROOT/"figures"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"], "mathtext.fontset": "cm",
    "font.size": 9.5, "axes.labelsize": 9.5, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8, "axes.edgecolor": "black",
    "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.major.size": 3.5, "ytick.major.size": 3.5,
    "xtick.direction": "out", "ytick.direction": "out", "axes.grid": False, "legend.frameon": False,
    "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.06, "axes.unicode_minus": False,
})
BLUE, RED, GREY, LGREY, BLACK = "#1F4E8C", "#C0392B", "#7F7F7F", "#D3D3D3", "black"
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

adopt = pd.read_csv(RES/"adoption_index_FINAL.csv"); fin = json.load(open(RES/"adoption_index_FINAL.json"))
ev = pd.read_csv(RES/"install_event_curves.csv"); plc = json.load(open(RES/"install_jump_placebo.json"))
null = np.load(RES/"install_jump_placebo_null.npz")["null_jump"]; dg = json.load(open(RES/"install_curve_diagnostics.json"))
grid = pd.read_csv(RES/"sensitivity_install.csv"); sens = json.load(open(RES/"sensitivity_install.json"))
pre, post = adopt[adopt.k < 0], adopt[(adopt.k > 0) & (adopt.k <= 10)]
pre_m, jump, ceil = pre.s.mean(), fin["jump"], dg["ceiling"]["ceiling_jump"]; lo, hi = fin["jump_ci95"]

fig = plt.figure(figsize=(7.2, 9.4))
gs = fig.add_gridspec(3, 2, height_ratios=[1.35, 1, 1], width_ratios=[1.25, 1], left=0.09, right=0.98, top=0.93, bottom=0.06, wspace=0.34, hspace=0.62)
axA = fig.add_subplot(gs[0, :]); axB = fig.add_subplot(gs[1, 0]); axC = fig.add_subplot(gs[2, 0]); axD = fig.add_subplot(gs[1:, 1])
def letter(ax, L, dx=-0.09): ax.text(dx, 1.03, L, transform=ax.transAxes, fontsize=12, fontweight="bold", va="bottom", ha="left")

# ---- a 逐场采纳指数 ----
for _, g in ev.groupby("event"):
    g = g.sort_values("k"); axA.plot(g[g.k < 0].k, g[g.k < 0].s, color=LGREY, lw=0.6, zorder=1); axA.plot(g[g.k > 0].k, g[g.k > 0].s, color=LGREY, lw=0.6, zorder=1)
for yv in (0, 1): axA.axhline(yv, color=GREY, lw=0.7, ls=":", zorder=2)
axA.axhline(pre_m + ceil, color=RED, lw=1.1, ls="--", zorder=3)
axA.axvline(0, color=BLACK, lw=0.9, zorder=3)
axA.plot(pre.k, pre.s, "o-", color=BLACK, lw=1.7, ms=4.5, zorder=5)
axA.plot(post.k, post.s, "o-", color=BLUE, lw=1.8, ms=4.5, zorder=5)
axA.annotate("", xy=(1, post.s.iloc[0]), xytext=(1, pre_m), arrowprops=dict(arrowstyle="<->", color=BLACK, lw=0.9, shrinkA=3, shrinkB=3), zorder=6)
axA.text(0.88, (post.s.iloc[0] + pre_m)/2, f"+{jump:.2f}", fontsize=9.5, ha="right", va="center", zorder=7)   # 换帅竖线与第 1 场之间没有数据
axA.set_xlim(-5.6, 10.6); axA.set_ylim(-1.25, 2.25); axA.set_xticks([-5, -3, -1, 1, 3, 5, 7, 9]); axA.set_yticks([-1, 0, 1, 2])
axA.set_xlabel("Match relative to the coaching change"); axA.set_ylabel("Adoption index\n0 = outgoing coach, 1 = new coach")
axA.legend(handles=[Line2D([], [], color=LGREY, lw=1.2, label="each of 21 in-season changes"),
                    Line2D([], [], color=BLACK, lw=1.7, marker="o", ms=4.5, label="mean before"),
                    Line2D([], [], color=BLUE, lw=1.8, marker="o", ms=4.5, label="mean after"),
                    Line2D([], [], color=RED, lw=1.1, ls="--", label="largest jump measurable given single-match noise")],
           loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=2, handlelength=2.2, columnspacing=1.6, borderaxespad=0)
letter(axA, "a", dx=-0.075)

# ---- b 安慰剂 ----
axB.hist(null, bins=36, color=LGREY, edgecolor="none", zorder=2)
axB.axvline(jump, color=BLUE, lw=1.6, zorder=4)
axB.set_xlabel("First-match jump at placebo changes"); axB.set_ylabel("Placebo draws (of 1,000)"); axB.set_xticks([-0.4, -0.2, 0, 0.2, 0.4, 0.6])
axB.set_xlim(-0.45, 0.68)
axB.text(jump + 0.02, axB.get_ylim()[1]*0.97, f"observed\n$p$ = {plc['p_greater']:.3f}", fontsize=9, ha="left", va="top", color=BLUE)
letter(axB, "b", dx=-0.2)

# ---- c 36 组参数 ----
gj = grid.jump.sort_values().to_numpy(); xs = np.arange(len(gj)); main_j = sens["primary"]["jump"]
axC.bar(xs, gj, color=LGREY, width=0.75, zorder=2); im = int(np.argmin(np.abs(gj - main_j))); axC.bar([im], [gj[im]], color=BLUE, width=0.75, zorder=3)
axC.axhline(plc["null_ci95"][1], color=RED, lw=1.1, ls="--", zorder=4)
a5, a10 = dg["curve"]["jump_alt_mean_k1_5"], dg["curve"]["jump_alt_mean_k1_10"]   # 另两种跳变定义，用前 5 场、前 10 场的平均代替第 1 场
axC.axhline(a5, color=BLUE, lw=1.0, ls=":", zorder=4); axC.axhline(a10, color=BLUE, lw=1.0, ls="-.", zorder=4)
axC.set_xticks([]); axC.set_xlim(-0.8, len(gj) - 0.2); axC.set_ylim(0, 0.75); axC.set_yticks([0, 0.25, 0.5, 0.75])
axC.set_xlabel("36 parameter settings, sorted"); axC.set_ylabel("First-match jump")
axC.legend(handles=[Patch(color=BLUE, label=f"match 1, main ({gj[im]:.2f})"),
                    Line2D([], [], color=BLUE, lw=1.0, ls=":", label=f"avg. of first 5 matches ({a5:.2f})"),
                    Line2D([], [], color=BLUE, lw=1.0, ls="-.", label=f"avg. of first 10 matches ({a10:.2f})"),
                    Line2D([], [], color=RED, lw=1.1, ls="--", label=f"placebo 95% bound ({plc['null_ci95'][1]:.2f})")],
           loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=2, fontsize=7.8, handlelength=1.6, columnspacing=0.8, borderaxespad=0)
letter(axC, "c", dx=-0.2)

# ---- d 逐次换帅 ----
ej = pd.Series(dg["heterogeneity"]["event_jump"]).sort_values(); yy = np.arange(len(ej))
cols = [BLUE if v > 0 else RED for v in ej.values]
axD.hlines(yy, 0, ej.values, color=cols, lw=1.3, zorder=2); axD.scatter(ej.values, yy, color=cols, s=16, zorder=3)
axD.axvline(0, color=BLACK, lw=0.8); axD.axvline(jump, color=BLUE, lw=0.9, ls="--", zorder=1)
axD.set_yticks(yy); axD.set_yticklabels([k.split(" / ")[1].split()[-1] for k in ej.index], fontsize=8.3)
axD.set_xlabel("First-match jump, each change"); axD.set_xlim(-1.1, 1.5); axD.set_ylim(-0.8, len(ej) - 0.2); axD.set_xticks([-1, -0.5, 0, 0.5, 1, 1.5])
axD.legend(handles=[Line2D([], [], color=BLUE, lw=0.9, ls="--", label=f"pooled jump {jump:.2f}"),
                    Line2D([], [], ls="none", label=f"median of changes {np.median(ej.values):.2f}")],
           loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=1, fontsize=8, handlelength=1.8, borderaxespad=0)
letter(axD, "d", dx=-0.3)

plt.savefig(FIG/"abstract_fig2_fullpage.png"); print("saved figures/abstract_fig2_fullpage.png")
