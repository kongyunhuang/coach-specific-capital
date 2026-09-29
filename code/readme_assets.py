"""
readme_assets.py — 公开仓库 README 用的装机动画、招聘卡动画与发现 2 配图
============================
README 顶部放装机动画 installation.gif（逐场揭示，第 1 场打出跳变，第 10 场打出"此后不再增长"，即摘要图 2 的 a 面板的动态版）；
发现 1 直接用整张摘要图 1；发现 2 用 finding2.png（摘要图 2 其余的 b、c、d 面板，从整页图裁出）；发现 3 用 hiring_card.gif
（Iraola 的招聘预期卡，依次出前任、旧签名、预测、实际）。原深蓝横幅 2026-09-29 撤下。每张图在 README 里只出现一次。

输入: results/install_event_curves.csv, results/adoption_index_FINAL.csv, results/install_jump_placebo.json,
      results/install_curve_diagnostics.json, results/hiring_cards.json, figures/abstract_fig2_fullpage.png
输出: assets/installation.gif, assets/finding2.png, assets/hiring_card.gif（另存各自的 *_last.png 供静态预览）

Usage:
  conda activate kronos
  python code/readme_assets.py

Last modified: 2026-09-29（顶部改为装机动画，撤下横幅；发现 2 改用图 2 的 b、c、d 裁片，避免同图重复；2026-09-28 动图第一帧改为完整终态、跳变标注不压线、招聘卡图例修正）
"""
import json, io
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RES, OUT = ROOT / "results", ROOT / "assets"
OUT.mkdir(exist_ok=True)
NAVY, BLUE, BLACK, RED, GREY, LGREY, WHITE = "#0f2440", "#1f4e96", "#111111", "#c0392b", "#7f7f7f", "#c8c8c8", "#ffffff"
plt.rcParams.update({"font.family": "Helvetica Neue", "font.size": 15, "axes.spines.top": False, "axes.spines.right": False})

def fig_to_frame(fig, colors=128):
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=100); plt.close(fig); buf.seek(0)
    return Image.open(buf).convert("P", palette=Image.ADAPTIVE, colors=colors)

def save_gif(frames, durs, path):
    # 第一帧放完整终态（停 2.5 秒）再逐帧重演：关闭动图自动播放的读者、缩略图和静态预览看到的都是完整图
    frames, durs = [frames[-1]] + frames, [2500] + list(durs)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True)
    frames[-1].convert("RGB").save(str(path).replace(".gif", "_last.png"))
    print("saved", path, len(frames), "frames")

# ---------------------------------------------------------------- 1. 合并均值（原横幅已于 2026-09-29 撤下，README 不再用横幅）
pooled = pd.read_csv(RES / "adoption_index_FINAL.csv")
pre, post = pooled[pooled.k < 0], pooled[(pooled.k > 0) & (pooled.k <= 10)]

# ---------------------------------------------------------------- 2. installation.gif
ev = pd.read_csv(RES / "install_event_curves.csv")
plc = json.load(open(RES / "install_jump_placebo.json")); dg = json.load(open(RES / "install_curve_diagnostics.json"))
pre_m = pre.s.mean(); jump = plc["observed_jump"]; ceil = dg["ceiling"]["ceiling_jump"]; p_slope = dg["curve"]["p_k1_10"]

def install_frame(k_now):
    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100); fig.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.14)
    for _, g in ev.groupby("event"):
        g = g.sort_values("k")
        for part in (g[g.k < 0], g[g.k > 0]):
            part = part[part.k <= k_now]
            if len(part): ax.plot(part.k, part.s, color=LGREY, lw=1.0, zorder=1)
    for yv in (0, 1): ax.axhline(yv, color=GREY, lw=0.8, ls=":", zorder=2)
    ax.axvline(0, color=BLACK, lw=1.2, zorder=3)
    pp = pre[pre.k <= k_now]; ax.plot(pp.k, pp.s, "o-", color=BLACK, lw=2.6, ms=7, zorder=5)
    if k_now >= 1:
        qq = post[post.k <= k_now]; ax.plot(qq.k, qq.s, "o-", color=BLUE, lw=2.8, ms=7, zorder=5)
        ax.axhline(pre_m + ceil, color=RED, lw=1.4, ls="--", zorder=3)
        ax.text(-5.4, pre_m + ceil + 0.06, "ceiling set by measurement noise", color=RED, fontsize=13, va="bottom")
        ax.annotate("", xy=(1, post.s.iloc[0]), xytext=(1, pre_m), arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.4, shrinkA=2, shrinkB=2), zorder=6)
        # 标注放在箭头下半段右侧（顶端低于第 1 到 3 场的蓝线），白底只盖灰线
        ax.text(1.3, pre_m + 0.14, f"+{jump:.2f} in match one\nplacebo p = {plc['p_greater']:.3f}", fontsize=14, va="top", fontweight="bold", zorder=7, bbox=dict(fc="white", ec="none", pad=2))
    if k_now >= 10:
        ax.text(5.5, 1.75, f"and no further growth over matches 1 to 10\n(slope p = {p_slope:.2f})", fontsize=14, ha="center", color=BLUE, fontweight="bold")
    ax.set_xlim(-5.6, 10.6); ax.set_ylim(-1.25, 2.25); ax.set_xticks([-5, -3, -1, 1, 3, 5, 7, 9]); ax.set_yticks([-1, 0, 1, 2])
    ax.set_xlabel("Match relative to the coaching change", fontsize=15); ax.set_ylabel("Adoption index   0 = predecessor,  1 = new coach", fontsize=14)
    ax.text(10.5, -1.15, "21 in-season changes, Premier League and LaLiga 2022-23 to 2024-25", ha="right", va="bottom", fontsize=12, color=GREY)
    fig.text(0.09, 0.93, "How fast does a new head coach's style arrive?", fontsize=24, fontweight="bold", va="top")
    fig.text(0.09, 0.855, "Every grey line is one club. Black and blue are the average. Style is measured on 33 tactical choices, not results.", fontsize=13.5, color=GREY, va="top")
    fig.text(0.97, 0.93, "before the change" if k_now < 0 else f"match {k_now}", fontsize=20, ha="right", va="top", color=BLUE if k_now >= 1 else BLACK, fontweight="bold")
    return fig_to_frame(fig)

ks = [-5, -4, -3, -2, -1] + list(range(1, 11))
frames = [install_frame(k) for k in ks]; durs = [700 if k in (-5, 1, 10) else 380 for k in ks]; durs[-1] = 3500
save_gif(frames, durs, OUT / "installation.gif")

# ---------------------------------------------------------------- 2b. finding2.png（摘要图 2 的下半部分）
# README 顶部是装机动画（即摘要图 2 的 a），发现 2 只放图 2 其余的 b、c、d，避免同一张图出现两次。
def _crop_lower(path, after_band):
    im = Image.open(path).convert("RGB"); a = np.asarray(im.convert("L")) > 245; blank = a.all(axis=1)
    bands, st = [], None
    for i, v in enumerate(blank):
        if v and st is None: st = i
        if not v and st is not None:
            if i - st > 25: bands.append((st, i))
            st = None
    top = bands[after_band][1] - 10
    rows = np.where(~a[top:].all(axis=1))[0]; bottom = min(top + rows[-1] + 20, im.height)
    cols = np.where(~a[top:bottom].all(axis=0))[0]
    return im.crop((max(cols[0] - 20, 0), top, min(cols[-1] + 20, im.width), bottom))
_crop_lower(ROOT / "figures/abstract_fig2_fullpage.png", 2).save(OUT / "finding2.png", optimize=True)   # 图 2 的 b（安慰剂）、c（36 组参数）、d（逐次换帅）
print("saved finding2")

# ---------------------------------------------------------------- 3. hiring_card.gif
hc = json.load(open(RES / "hiring_cards.json"))
card = next(c for c in hc["cards"] if c["coach"] == "Andoni Iraola")
FAM = [("OUT", "Pressing and defensive line"), ("CONCEDED", "What the opponent is allowed"),
       ("POSS", "Retention and build-up"), ("PROG", "Progression and chance creation")]
rob = hc["robustness"]; n_hit = sum(int(round(rob[f]["direction_correct_coach"] * 7)) for f in ("OUT", "CONCEDED", "POSS", "PROG"))
n_mr = sum(int(round(rob[f]["direction_correct_mean_reversion"] * 7)) for f in ("OUT", "CONCEDED", "POSS", "PROG"))

def card_frame(stage):
    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100); fig.subplots_adjust(left=0.30, right=0.80, top=0.70, bottom=0.19)
    ys = np.arange(len(FAM))[::-1]
    ax.axvline(0, color=GREY, lw=0.8, ls=":")
    for y, (key, label) in zip(ys, FAM):
        f = card["families"][key]
        ax.text(-1.55, y, label, ha="right", va="center", fontsize=15, fontweight="bold" if f["off_ball"] else "normal", color=BLACK)
        ax.plot([f["predecessor"]], [y], "o", ms=13, color=GREY, zorder=4)
        if stage >= 1: ax.plot([f["coach_prior"]], [y], "o", ms=13, mfc="white", mec=BLUE, mew=2.2, zorder=4)
        if stage >= 2:
            ax.plot([f["predecessor"], f["predicted_blend"]], [y, y], color=BLUE, lw=2.2, zorder=3)
            ax.plot([f["predicted_blend"]], [y], "D", ms=12, color=BLUE, zorder=5)
        if stage >= 3:
            ax.plot([f["actual_first10"]], [y], "*", ms=22, color=BLACK, zorder=6)
            ok = f["direction_vs_predecessor"]["correct"]
            ax.text(1.58, y, "direction right" if ok else "direction wrong", ha="left", va="center", fontsize=14, color=BLUE if ok else RED, fontweight="bold", clip_on=False)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-0.7, len(FAM) - 0.3); ax.set_yticks([])
    ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_xticklabels(["−1 SD", "", "league average", "", "+1 SD"], fontsize=13)
    ax.text(-1.5, -1.05, "less pressing, less possession", ha="left", va="top", fontsize=12.5, color=GREY, clip_on=False); ax.text(1.5, -1.05, "more pressing, more possession", ha="right", va="top", fontsize=12.5, color=GREY, clip_on=False)
    for s in ax.spines.values(): s.set_visible(False)
    # legend, revealed step by step; markers drawn exactly as in the plot. All four entries are always laid out
    # (unrevealed ones transparent) so the legend does not reflow between frames; ncol=2 fills column-first,
    # hence the order 0, 2, 1, 3 for rows (outgoing, signature) and (predicted, actual).
    from matplotlib.lines import Line2D
    items = [Line2D([], [], ls="none", marker="o", ms=11, color=GREY, label="outgoing coach (Gary O'Neil at Bournemouth)"),
             Line2D([], [], ls="none", marker="o", ms=11, mfc="white", mec=BLUE, mew=2.2, label="Iraola's signature at Rayo Vallecano"),
             Line2D([], [], ls="none", marker="D", ms=10, color=BLUE, label="predicted after ten matches (blend, off-ball weight 0.55)"),
             Line2D([], [], ls="none", marker="*", ms=17, color=BLACK, label="actual, first ten matches at Bournemouth")]
    order = [0, 2, 1, 3]
    leg = fig.legend(handles=[items[i] for i in order], loc="upper left", bbox_to_anchor=(0.05, 0.87), ncol=2, frameon=False,
                     fontsize=13, handletextpad=0.4, columnspacing=2.2, labelspacing=0.7)
    for i, txt, hnd in zip(order, leg.get_texts(), leg.legend_handles):
        if i > stage: txt.set_alpha(0); hnd.set_alpha(0)
    fig.text(0.06, 0.965, "The hiring expectation card", fontsize=24, fontweight="bold", va="top")
    fig.text(0.06, 0.915, "Andoni Iraola, Rayo Vallecano to AFC Bournemouth, 2023. Written before his first match, checked after ten.", fontsize=13.5, color=GREY, va="top")
    if stage >= 3:
        fig.text(0.06, 0.05, f"Four of four families called right here. Across the seven qualifying appointments, {n_hit} of 28; league-mean reversion would give {n_mr}.", fontsize=12.5, color=GREY)
    return fig_to_frame(fig)

frames = [card_frame(s) for s in (0, 1, 2, 3)]; durs = [1600, 1600, 1800, 4200]
save_gif(frames, durs, OUT / "hiring_card.gif")
