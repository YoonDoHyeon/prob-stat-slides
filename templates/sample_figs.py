import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

font_manager.fontManager.addfont("/System/Library/Fonts/AppleSDGothicNeo.ttc")
plt.rcParams.update({
    "font.family": "Apple SD Gothic Neo",
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "font.size": 15,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#222222",
})

NAVY = "#1F3A5F"
ORANGE = "#E07A2E"
SKY = "#8FB8DE"
LIGHT = "#EEF3F8"
GRAY = "#888888"


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)


# 1. 동전 두 번: 표본공간 -> X 값 대응
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
ax.add_patch(Ellipse((2.5, 3.3), 3.4, 5.6, fill=False, lw=2.5, ec=NAVY))
ax.add_patch(Ellipse((7.5, 3.3), 2.4, 5.0, fill=False, lw=2.5, ec=ORANGE))
ax.text(2.5, 6.6, "표본공간 $S$", ha="center", fontsize=18, color=NAVY, weight="bold")
ax.text(7.5, 6.6, "$X$의 값", ha="center", fontsize=18, color=ORANGE, weight="bold")
outs = [("(H, H)", 5.0, 2), ("(H, T)", 3.9, 1), ("(T, H)", 2.8, 1), ("(T, T)", 1.7, 0)]
ys = {2: 4.7, 1: 3.3, 0: 1.9}
for lab, y, v in outs:
    ax.text(2.5, y, lab, ha="center", va="center", fontsize=17)
    ax.add_patch(FancyArrowPatch((3.5, y), (7.1, ys[v]), arrowstyle="-|>", mutation_scale=16, lw=1.8, color=SKY))
for v, y in ys.items():
    ax.text(7.5, y, str(v), ha="center", va="center", fontsize=22, weight="bold", color=ORANGE)
save(fig, "01_mapping")

# 2. 공학 속 확률변수 3가지
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
rng = np.random.default_rng(3)
# 불량품 개수
ax = axes[0]
for i in range(10):
    bad = i in (2, 7)
    ax.add_patch(FancyBboxPatch((i % 5 * 1.1, (i // 5) * 1.3), 0.8, 0.9, boxstyle="round,pad=0.05",
                                fc=ORANGE if bad else SKY, ec="white"))
    if bad:
        ax.text(i % 5 * 1.1 + 0.4, (i // 5) * 1.3 + 0.45, "×", ha="center", va="center", color="white", fontsize=18, weight="bold")
ax.set_xlim(-0.3, 5.6); ax.set_ylim(-0.4, 2.6); ax.axis("off")
ax.set_title("부품 10개 중 불량품 개수\n$X$ = 0, 1, 2, …, 10", fontsize=15, color=NAVY)
# 부품 수명
ax = axes[1]
t = np.linspace(0, 3000, 300)
ax.plot(t, np.exp(-t / 1000), color=NAVY, lw=2.5)
ax.set_xlabel("사용 시간 (h)"); ax.set_ylabel("작동 중인 비율")
ax.set_title("부품 수명\n$X \\geq 0$ 인 모든 실수", fontsize=15, color=NAVY)
# 측정 오차
ax = axes[2]
e = rng.normal(0, 0.02, 400)
ax.hist(e, bins=25, color=SKY, ec="white")
ax.axvline(0, color=ORANGE, lw=2, ls="--")
ax.set_xlabel("측정 오차 (mm)"); ax.set_ylabel("측정 횟수")
ax.set_title("길이 측정 오차\n구간 안의 모든 실수", fontsize=15, color=NAVY)
fig.tight_layout(w_pad=3)
save(fig, "02_engineering")

# 3. 이산 vs 연속
fig, axes = plt.subplots(2, 1, figsize=(7.5, 3.6))
for ax in axes:
    ax.set_ylim(-1, 1); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.axhline(0, color="#444444", lw=1.2)
ax = axes[0]
ax.set_xlim(-0.5, 6.5)
ax.scatter(range(7), [0] * 7, s=180, color=ORANGE, zorder=3)
ax.set_xticks(range(7))
ax.text(-0.45, 0.55, "이산: 하나씩 셀 수 있는 값", fontsize=19, color=ORANGE, weight="bold")
ax = axes[1]
ax.set_xlim(-0.5, 10.5)
ax.plot([0, 10], [0, 0], color=NAVY, lw=9, solid_capstyle="butt")
ax.scatter([0, 10], [0, 0], s=140, color=NAVY, zorder=3)
ax.set_xticks([0, 10])
ax.text(-0.45, 0.55, "연속: 구간 안의 모든 실수", fontsize=19, color=NAVY, weight="bold")
fig.tight_layout(h_pad=1.5)
save(fig, "03_disc_vs_cont")

# 4. 동전 두 번 확률분포 막대그래프
fig, ax = plt.subplots(figsize=(6, 4.2))
xs = [0, 1, 2]; ps = [1 / 4, 1 / 2, 1 / 4]
ax.vlines(xs, 0, ps, color=NAVY, lw=6)
ax.scatter(xs, ps, color=ORANGE, s=110, zorder=3)
for x, p, lab in zip(xs, ps, ["1/4", "1/2", "1/4"]):
    ax.text(x + 0.12, p, lab, va="center", fontsize=17, color=ORANGE)
ax.set_xticks(xs); ax.set_xlim(-0.5, 2.7); ax.set_ylim(0, 0.62)
ax.set_xlabel("$x$ (앞면의 개수)"); ax.set_ylabel("$P(X=x)$")
save(fig, "04_coin_pmf")

# 5. 확률의 합 = 1 (쌓은 막대)
fig, ax = plt.subplots(figsize=(11, 1.8))
left = 0
for p, lab, c in zip(ps, ["$P(X=0)$\n1/4", "$P(X=1)$\n1/2", "$P(X=2)$\n1/4"], [SKY, NAVY, ORANGE]):
    ax.barh(0, p, left=left, color=c, ec="white", lw=3, height=0.8)
    ax.text(left + p / 2, 0, lab, ha="center", va="center", color="white", fontsize=15, weight="bold")
    left += p
ax.set_xlim(0, 1); ax.set_yticks([]); ax.set_xticks([0, 0.5, 1])
ax.spines["left"].set_visible(False)
ax.set_xlabel("모든 확률을 이어 붙인 길이 = 1")
save(fig, "05_sum_one")

# 6. 불량품 개수 분포 (3개 검사, 불량률 0.1)
fig, ax = plt.subplots(figsize=(6.4, 4.3))
pp = [0.729, 0.243, 0.027, 0.001]
ax.bar(range(4), pp, color=[NAVY, SKY, ORANGE, ORANGE], width=0.6)
for i, p in enumerate(pp):
    ax.text(i, p + 0.02, f"{p:.3f}", ha="center", fontsize=15)
ax.set_xticks(range(4)); ax.set_ylim(0, 0.85)
ax.set_xlabel("$x$ (불량품 개수)"); ax.set_ylabel("$P(X=x)$")
save(fig, "06_defect_pmf")

# 7. 지하철 대기 시간 균등분포
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([0, 10], [0.1, 0.1], color=NAVY, lw=3)
ax.plot([0, 0], [0, 0.1], color=NAVY, lw=1.2, ls=":"); ax.plot([10, 10], [0, 0.1], color=NAVY, lw=1.2, ls=":")
ax.fill_between([3, 7], 0, 0.1, color=ORANGE, alpha=0.75)
ax.text(5, 0.05, "$P(3 \\leq X \\leq 7)$\n$= 4 \\times \\frac{1}{10} = 0.4$", ha="center", va="center", fontsize=15, color="white", weight="bold")
ax.text(10.2, 0.1, "$f(x)=\\frac{1}{10}$", va="center", fontsize=16, color=NAVY)
ax.set_xlim(-0.5, 12); ax.set_ylim(0, 0.15)
ax.set_xticks([0, 3, 7, 10]); ax.set_yticks([0, 0.1]); ax.set_yticklabels(["0", "1/10"])
ax.set_xlabel("$x$ (대기 시간, 분)"); ax.set_ylabel("$f(x)$")
save(fig, "07_subway_uniform")

# 8. 확률밀도함수 넓이
fig, ax = plt.subplots(figsize=(7, 4))
x = np.linspace(0, 10, 400)
f = np.exp(-(x - 5) ** 2 / 3); f /= np.trapezoid(f, x)
ax.plot(x, f, color=NAVY, lw=3)
m = (x >= 4) & (x <= 6)
ax.fill_between(x[m], 0, f[m], color=ORANGE, alpha=0.8)
ax.fill_between(x, 0, f, color=SKY, alpha=0.25)
ax.annotate("$P(a \\leq X \\leq b)$\n= 색칠한 넓이", xy=(5.3, 0.15), xytext=(7.2, 0.27), fontsize=15,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8), color=ORANGE)
ax.text(1.0, 0.12, "전체 넓이 = 1", fontsize=15, color=NAVY)
ax.set_xticks([4, 6]); ax.set_xticklabels(["$a$", "$b$"]); ax.set_yticks([])
ax.set_xlabel("$x$"); ax.set_ylabel("$f(x)$"); ax.set_ylim(0, 0.38)
save(fig, "08_pdf_area")

# 9. 한 점의 확률 = 0
fig, axes = plt.subplots(1, 3, figsize=(13, 3.2))
titles = ["$P(a \\leq X \\leq b)$", "$P(a \\leq X < b)$", "$P(X = b)$"]
for k, ax in enumerate(axes):
    ax.plot(x, f, color=NAVY, lw=2.5)
    if k < 2:
        ax.fill_between(x[m], 0, f[m], color=SKY, alpha=0.9)
    if k == 1:
        ax.plot([6, 6], [0, f[np.argmin(abs(x - 6))]], color=NAVY, ls="--", lw=1.5)
    if k == 2:
        ax.plot([6, 6], [0, f[np.argmin(abs(x - 6))]], color=ORANGE, lw=3)
        ax.text(6.4, 0.2, "넓이 0", color=ORANGE, fontsize=16, weight="bold")
    ax.set_title(titles[k], fontsize=17)
    ax.set_xticks([4, 6] if k < 2 else [6]); ax.set_xticklabels(["$a$", "$b$"] if k < 2 else ["$b$"])
    ax.set_yticks([]); ax.set_ylim(0, 0.33)
fig.text(0.355, 0.45, "=", fontsize=30, ha="center")
fig.text(0.675, 0.45, "+", fontsize=30, ha="center")
fig.tight_layout(w_pad=5)
save(fig, "09_point_zero")

# 10. 부품 수명 (지수분포, 평균 1000시간)
fig, ax = plt.subplots(figsize=(7.5, 4.2))
t = np.linspace(0, 4000, 400)
ft = np.exp(-t / 1000) / 1000
ax.plot(t, ft * 1000, color=NAVY, lw=3)
mm = t <= 500
ax.fill_between(t[mm], 0, ft[mm] * 1000, color=ORANGE, alpha=0.8)
ax.annotate("$P(X \\leq 500) \\approx 0.39$\n500시간 안에 고장날 확률", xy=(250, 0.4), xytext=(1300, 0.65), fontsize=15,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8), color=ORANGE)
ax.set_xlabel("$x$ (수명, 시간)"); ax.set_ylabel("$f(x)$ (×$10^{-3}$)")
ax.set_ylim(0, 1.1)
save(fig, "10_lifetime")

# 11. 퀴즈 3번 그래프 f(x)=kx
fig, ax = plt.subplots(figsize=(4.5, 3.6))
ax.plot([0, 4], [0, 4], color=NAVY, lw=3)
ax.plot([4, 4], [0, 4], color=NAVY, lw=1.2, ls=":")
ax.fill_between([0, 2], 0, [0, 2], color=ORANGE, alpha=0.8)
ax.text(2.3, 3.4, "$y = f(x)$", fontsize=15, color=NAVY)
ax.set_xticks([0, 2, 4]); ax.set_yticks([4]); ax.set_yticklabels(["$4k$"])
ax.set_xlabel("$x$"); ax.set_xlim(0, 4.6); ax.set_ylim(0, 4.6)
save(fig, "11_quiz_kx")
print("done")
