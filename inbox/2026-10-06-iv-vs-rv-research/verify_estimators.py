"""Numerical check of realised-volatility estimators (numpy only).

Simulates geometric Brownian motion with a KNOWN volatility (20% a year, 252
days a year), with and without drift, with and without an overnight gap, and
shows what each estimator returns.

Grid: each trading session is 375 minutes (the NSE session) cut into 1500
"ticks" of 15 seconds.  1-minute bars are 4 ticks, 5-minute bars are 20 ticks.
The TRUE continuous high and low inside every tick are drawn exactly from the
law of the maximum of a Brownian bridge, so "continuous" highs and lows are
not an approximation.  (The maximum and the minimum inside one tick are drawn
independently; this only matters when a bar's high and low fall in the same
15-second tick, which is rare for the bar sizes used here.)

Every result is printed as  estimated variance / true variance.  1.000 means
the estimator recovers the known volatility; 1.10 means variance is 10% too
high, i.e. volatility is about 4.9% too high (sqrt(1.10) = 1.049).

Run:  python verify_estimators.py        (about a minute)
"""

import math

import numpy as np

SIGMA_ANN = 0.20
DAYS_PER_YEAR = 252
MINUTES = 375
TICKS_PER_MIN = 4
TICKS = MINUTES * TICKS_PER_MIN  # 1500
VAR_DAY = SIGMA_ANN**2 / DAYS_PER_YEAR  # whole-day (close-to-close) variance
SD_DAY = math.sqrt(VAR_DAY)
LN2 = math.log(2.0)
MU1 = math.sqrt(2.0 / math.pi)  # E|Z| for a standard normal Z


# --------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------
def simulate(
    n_days,
    drift_ratio=0.0,  # drift per day, in units of one day's standard deviation
    f=0.0,  # share of the day's variance that falls overnight
    jump_share=0.0,  # one jump a day; its variance as a share of the session variance
    noise_bp=0.0,  # microstructure noise, standard deviation in basis points
    u_shape=0.0,  # 0 = flat intraday volatility; 3 = open/close variance 4x midday
    seed=1,
    chunk=1000,
):
    rng = np.random.default_rng(seed)
    mu_day = drift_ratio * SD_DAY
    t = (np.arange(TICKS) + 0.5) / TICKS
    prof = 1.0 + u_shape * (2.0 * t - 1.0) ** 2
    prof /= prof.mean()
    v_tick = (1.0 - f) * VAR_DAY / TICKS * prof  # variance of each tick step
    m_tick = (1.0 - f) * mu_day / TICKS
    keys = {}

    def put(name, arr):
        keys.setdefault(name, []).append(arr)

    for start in range(0, n_days, chunk):
        nd = min(chunk, n_days - start)
        if f > 0:
            o = mu_day * f + math.sqrt(f * VAR_DAY) * rng.standard_normal(nd)
        else:
            o = np.zeros(nd)
        incr = m_tick + np.sqrt(v_tick) * rng.standard_normal((nd, TICKS))
        x_end = np.cumsum(incr, axis=1)  # diffusive path at the end of each tick
        x_beg = np.concatenate([np.zeros((nd, 1)), x_end[:, :-1]], axis=1)
        # exact continuous extremes inside each tick (Brownian-bridge law)
        disc = (x_end - x_beg) ** 2
        e_hi = -2.0 * v_tick * np.log(rng.random((nd, TICKS)))
        e_lo = -2.0 * v_tick * np.log(rng.random((nd, TICKS)))
        hi = 0.5 * (x_beg + x_end + np.sqrt(disc + e_hi))
        lo = 0.5 * (x_beg + x_end - np.sqrt(disc + e_lo))
        if jump_share > 0:  # the jump lands exactly at the end of a random tick
            jsd = math.sqrt(jump_share * (1.0 - f) * VAR_DAY)
            jmp = np.zeros((nd, TICKS))
            jmp[np.arange(nd), rng.integers(0, TICKS, nd)] = jsd * rng.standard_normal(nd)
            jcum = np.cumsum(jmp, axis=1)
            jprev = np.concatenate([np.zeros((nd, 1)), jcum[:, :-1]], axis=1)
            hi += jprev
            lo += jprev
            x_end = x_end + jcum
        x = np.concatenate([np.zeros((nd, 1)), x_end], axis=1)  # (nd, TICKS+1), open = 0
        hi = np.maximum(hi, x[:, 1:])
        lo = np.minimum(lo, x[:, 1:])

        put("o", o)
        put("c", x[:, -1])
        put("u_cont", np.maximum(hi.max(axis=1), 0.0))
        put("d_cont", np.minimum(lo.min(axis=1), 0.0))
        for n_obs, step in ((1500, 1), (375, 4), (75, 20), (25, 60)):
            g = x[:, ::step]
            put(f"u_{n_obs}", g.max(axis=1))
            put(f"d_{n_obs}", g.min(axis=1))

        # ---- intraday measures use the OBSERVED price y = true + noise ----
        y = x
        if noise_bp > 0:
            y = x + noise_bp * 1e-4 * rng.standard_normal(x.shape)
        for label, step in (("15s", 1), ("1m", 4), ("5m", 20), ("15m", 60), ("25m", 100)):
            r = np.diff(y[:, ::step], axis=1)
            put(f"rv_{label}", (r**2).sum(axis=1))
        K = 20  # 5 minutes, in ticks
        n = TICKS
        lagk = y[:, K:] - y[:, :-K]
        rv_avg = (lagk**2).sum(axis=1) / K  # subsampled-and-averaged RV
        nbar = (n - K + 1) / K
        tsrv = rv_avg - (nbar / n) * keys["rv_15s"][-1]
        put("rv_sub5m", rv_avg)
        put("tsrv", tsrv)
        put("tsrv_adj", tsrv / (1.0 - nbar / n))
        for label, step in (("5m", 20), ("1m", 4)):
            a = np.abs(np.diff(y[:, ::step], axis=1))
            m = a.shape[1]
            # m/(m-1) is a common end correction; Barndorff-Nielsen & Shephard (2004) print none
            put(f"bv_{label}", (a[:, 1:] * a[:, :-1]).sum(axis=1) * (m / (m - 1)) / MU1**2)
            mn = np.minimum(a[:, 1:], a[:, :-1])
            put(f"minrv_{label}", (mn**2).sum(axis=1) * (math.pi / (math.pi - 2)) * (m / (m - 1)))
            md = np.median(np.stack([a[:, 2:], a[:, 1:-1], a[:, :-2]]), axis=0)
            put(
                f"medrv_{label}",
                (md**2).sum(axis=1) * (math.pi / (6 - 4 * math.sqrt(3) + math.pi)) * (m / (m - 2)),
            )
        # realised range on 5-minute bars
        bars = MINUTES // 5
        bh = hi.reshape(nd, bars, 20).max(axis=2)
        bl = lo.reshape(nd, bars, 20).min(axis=2)
        put("rr5_cont", ((bh - bl) ** 2).sum(axis=1) / (4 * LN2))
        g1 = x[:, ::4]  # 1-minute closes: 6 points per 5-minute bar, 5 returns
        idx = np.arange(bars)[:, None] * 5 + np.arange(6)[None, :]
        seg = g1[:, idx]
        put("rr5_m5", ((seg.max(axis=2) - seg.min(axis=2)) ** 2).sum(axis=1) / (4 * LN2))
        # part-day realised variance from 1-minute returns
        r1 = np.diff(y[:, ::4], axis=1) ** 2
        put("rv1_first60", r1[:, :60].sum(axis=1))
        put("rv1_first187", r1[:, :187].sum(axis=1))
    out = {k: np.concatenate(v) for k, v in keys.items()}
    out["profile_cum"] = np.cumsum(prof.reshape(MINUTES, TICKS_PER_MIN).mean(axis=1)) / MINUTES
    return out


# --------------------------------------------------------------------------
# Daily-bar estimators.  All take per-day arrays shaped (windows, n) and
# return one variance per window, in per-day units.
#   o = ln(O_i / C_{i-1})   overnight
#   u = ln(H_i / O_i), d = ln(L_i / O_i), c = ln(C_i / O_i)
# --------------------------------------------------------------------------
def cc_demeaned(o, u, d, c):
    return (o + c).var(axis=1, ddof=1)


def cc_zero_mean(o, u, d, c):
    return ((o + c) ** 2).mean(axis=1)


def parkinson(o, u, d, c):
    return ((u - d) ** 2).mean(axis=1) / (4 * LN2)


def gk_practical(o, u, d, c):  # Garman-Klass eq. (19a)
    return (0.5 * (u - d) ** 2 - (2 * LN2 - 1) * c**2).mean(axis=1)


def gk_exact(o, u, d, c):  # Garman-Klass eq. (19)
    return (0.511 * (u - d) ** 2 - 0.019 * (c * (u + d) - 2 * u * d) - 0.383 * c**2).mean(axis=1)


def rogers_satchell(o, u, d, c):
    return (u * (u - c) + d * (d - c)).mean(axis=1)


def gkyz_practical(o, u, d, c):  # the form Sinclair, Bennett and TTR print
    return (o**2 + 0.5 * (u - d) ** 2 - (2 * LN2 - 1) * c**2).mean(axis=1)


def gk_yz_eq4(o, u, d, c):  # Yang-Zhang (2000) eq. (4)
    return (
        (o**2).mean(axis=1)
        - 0.383 * (c**2).mean(axis=1)
        + 1.364 * parkinson(o, u, d, c)
        + 0.019 * rogers_satchell(o, u, d, c)
    )


def yz_k(n, alpha=1.34):  # Yang-Zhang eq. (10) and (18)
    return (alpha - 1.0) / (alpha + (n + 1.0) / (n - 1.0))


def yang_zhang(o, u, d, c):  # Yang-Zhang eq. (7)-(9)
    n = o.shape[1]
    k = yz_k(n)
    return o.var(axis=1, ddof=1) + k * c.var(axis=1, ddof=1) + (1 - k) * rogers_satchell(o, u, d, c)


def yang_zhang_library_variant(o, u, d, c):
    """What jasonstrimpel/volatility-trading computes (and code copied from it):
    close-to-CLOSE squared returns in place of open-to-close, no mean taken off,
    and Rogers-Satchell divided by n-1 instead of n."""
    n = o.shape[1]
    k = yz_k(n)
    v_o = (o**2).sum(axis=1) / (n - 1)
    v_c = ((o + c) ** 2).sum(axis=1) / (n - 1)
    v_rs = (u * (u - c) + d * (d - c)).sum(axis=1) / (n - 1)
    return v_o + k * v_c + (1 - k) * v_rs


def yang_zhang_wrong_k(o, u, d, c):
    """k = 0.34 / (1 + (n+1)/(n-1)): the misprint that was in volatility-trading
    until its issue #16; otherwise as the paper."""
    n = o.shape[1]
    k = 0.34 / (1.0 + (n + 1.0) / (n - 1.0))
    return o.var(axis=1, ddof=1) + k * c.var(axis=1, ddof=1) + (1 - k) * rogers_satchell(o, u, d, c)


def rs_corrected(u, d, c, n_obs):
    """Rogers-Satchell (1991) eq. (5): correction for highs and lows seen at
    only n_obs equally spaced points.  Returns one variance per day."""
    h = 1.0 / n_obs
    a = math.sqrt(2 * math.pi) * (0.25 - (math.sqrt(2) - 1) / 6)
    b = (1 + 3 * math.pi / 4) / 12
    rs = u * (u - c) + d * (d - c)
    A = 1 - 2 * b * h
    B = 2 * (u - d) * a * math.sqrt(h)
    sig = (B + np.sqrt(B**2 + 4 * A * rs)) / (2 * A)
    return sig**2


def ewma(r, lam=0.94, burn=250):
    """RiskMetrics: var_t = lam * var_{t-1} + (1 - lam) * r_t^2 (zero mean)."""
    v = np.empty_like(r)
    cur = (r[:20] ** 2).mean()
    for i, ri in enumerate(r):
        cur = lam * cur + (1 - lam) * ri * ri
        v[i] = cur
    return v[burn:]


DAILY = [
    ("Close-to-close, mean removed, n-1", cc_demeaned),
    ("Close-to-close, zero mean, n", cc_zero_mean),
    ("Parkinson", parkinson),
    ("Garman-Klass practical (19a)", gk_practical),
    ("Garman-Klass exact (19)", gk_exact),
    ("Rogers-Satchell", rogers_satchell),
    ("GKYZ practical (o^2 + 19a)", gkyz_practical),
    ("GK per Yang-Zhang eq. (4)", gk_yz_eq4),
    ("Yang-Zhang, k from eq. (18)", yang_zhang),
    ("Yang-Zhang, wrong k (0.34/(1+..))", yang_zhang_wrong_k),
    ("Yang-Zhang, library variant", yang_zhang_library_variant),
]


def windows(sim, n, hl="cont"):
    w = len(sim["o"]) // n
    cut = lambda a: a[: w * n].reshape(w, n)  # noqa: E731
    return cut(sim["o"]), cut(sim[f"u_{hl}"]), cut(sim[f"d_{hl}"]), cut(sim["c"])


def fmt(x):
    return f"{x:7.3f}"


def table(title, header, rows, width=36):
    print()
    print(title)
    print("-" * len(title))
    print(f"{'':{width}}" + "".join(f"{h:>15}" for h in header))
    for name, vals in rows:
        print(f"{name:{width}}" + "".join(f"{v:>15}" for v in vals))


def main():
    N_DAYS = 60000
    WIN = 20
    print(f"True volatility {SIGMA_ANN:.0%} a year; {DAYS_PER_YEAR} days a year; ")
    print(f"{N_DAYS} simulated days per scenario; session {MINUTES} minutes; {TICKS} ticks a day.")
    print("Every figure is  mean estimated variance / true variance  unless it says otherwise.")

    scen = {
        "A": dict(drift_ratio=0.0, f=0.0),
        "B": dict(drift_ratio=0.5, f=0.0),
        "C": dict(drift_ratio=0.0, f=0.25),
        "D": dict(drift_ratio=0.5, f=0.25),
    }
    sims = {k: simulate(N_DAYS, seed=10 + i, **v) for i, (k, v) in enumerate(scen.items())}

    # ---- Table 1: bias of the daily-bar estimators ------------------------
    rows = []
    for name, fn in DAILY:
        rows.append((name, [fmt(fn(*windows(sims[s], WIN)).mean() / VAR_DAY) for s in "ABCD"]))
    rows.append(
        ("EWMA lambda 0.94 (zero mean)", [fmt(ewma(sims[s]["o"] + sims[s]["c"]).mean() / VAR_DAY) for s in "ABCD"])
    )
    table(
        "Table 1. Daily-bar estimators, 20-day windows, true continuous highs and lows",
        ["A none", "B drift", "C gap", "D both"],
        rows,
    )
    print("A: no drift, no overnight gap.  B: drift of 0.5 daily standard deviations a day (about 159% a year).")
    print("C: 25% of each day's variance falls overnight.  D: both.")

    # ---- Table 2: efficiency ---------------------------------------------
    rows = []
    theory = {
        "Close-to-close, mean removed, n-1": "",
        "Close-to-close, zero mean, n": "1.0",
        "Parkinson": "4.91 / 5.2",
        "Garman-Klass practical (19a)": "7.4",
        "Garman-Klass exact (19)": "7.4",
        "Rogers-Satchell": "6.0",
    }
    one = lambda a: a.reshape(-1, 1)  # noqa: E731  (every day is its own window)
    a = sims["A"]
    day_args = (one(a["o"]), one(a["u_cont"]), one(a["d_cont"]), one(a["c"]))
    base_day = cc_zero_mean(*day_args).var()
    for name, fn in DAILY[:10]:
        vals = []
        single = name in theory and theory[name] != ""
        vals.append(fmt(base_day / fn(*day_args).var()) if single else "")
        vals.append(theory.get(name, ""))
        for s in "AC":
            est = fn(*windows(sims[s], WIN))
            if abs(est.mean() / VAR_DAY - 1) > 0.05:
                vals.append("(biased)")
            else:
                vals.append(fmt(cc_demeaned(*windows(sims[s], WIN)).var() / est.var()))
        rows.append((name, vals))
    ew = [fmt(cc_demeaned(*windows(sims[s], WIN)).var() / ewma(sims[s]["o"] + sims[s]["c"]).var()) for s in "AC"]
    rows.append(("EWMA lambda 0.94 (zero mean)", ["", ""] + ew))
    table(
        "Table 2. Efficiency: variance of the close-to-close estimate / variance of this estimate",
        ["1 day, A", "paper", "20 days, A", "20 days, C"],
        rows,
    )
    print("'1 day' is the papers' own definition: one day's squared close-to-close return against one day's estimate.")
    print("'20 days' compares 20-day windows with the mean-removed close-to-close estimate (n-1 = 19), so the")
    print("single-day figures are multiplied by about 20/19 there.")
    k20 = yz_k(20)
    print(f"Yang-Zhang k for n=20: {k20:.4f}.  Paper's eq. (11) efficiency 1/(f^2+(1-f)^2 k) "
          f"with f=0.25: {1 / (0.25**2 + 0.75**2 * k20):.2f}; with f=0: {1 / k20:.2f}.")
    print("EWMA theory: (1+lambda)/(1-lambda) = 32.3 effective days against 19, ratio 1.70.")

    # ---- Table 3: highs and lows seen only at discrete points -------------
    rows = []
    a = sims["A"]
    for name, fn in (("Parkinson", parkinson), ("Garman-Klass practical (19a)", gk_practical),
                     ("Rogers-Satchell", rogers_satchell)):
        vals = [fmt(fn(*windows(a, WIN, hl)).mean() / VAR_DAY) for hl in ("25", "75", "375", "1500", "cont")]
        rows.append((name, vals))
    vals = [fmt(rs_corrected(a[f"u_{n}"], a[f"d_{n}"], a["c"], n).mean() / VAR_DAY) for n in (25, 75, 375, 1500)]
    rows.append(("Rogers-Satchell corrected, eq. (5)", vals + ["n/a"]))
    table(
        "Table 3. Scenario A, highs and lows taken from N equally spaced prices a day",
        ["N=25", "N=75", "N=375", "N=1500", "continuous"],
        rows,
    )
    print("N=75 is one price every 5 minutes, N=375 every minute, N=1500 every 15 seconds.")

    # ---- Table 4: drift sweep --------------------------------------------
    rows = {name: [] for name in ("Close-to-close, zero mean, n", "Close-to-close, mean removed, n-1", "Parkinson",
                                  "Garman-Klass practical (19a)", "Rogers-Satchell",
                                  "Yang-Zhang, k from eq. (18)")}
    fns = dict(DAILY)
    ratios = (0.0, 0.1, 0.25, 0.5, 1.0, 2.0)
    for i, dr in enumerate(ratios):
        s = simulate(6000, drift_ratio=dr, seed=100 + i)
        for name in rows:
            rows[name].append(fmt(fns[name](*windows(s, WIN)).mean() / VAR_DAY))
    table(
        "Table 4. Bias against drift (drift per day / one day's standard deviation), no gap, continuous highs and lows",
        [f"{r:g}" for r in ratios],
        list(rows.items()),
    )
    print("0.1 is about 32% a year at 20% volatility; 0.5 is about 159% a year; 1.0 and 2.0 are short violent trends.")

    # ---- Table 5: small-sample bias of the standard deviation ------------
    r = sims["A"]["o"] + sims["A"]["c"]
    rows = []
    for n in (5, 10, 20, 60):
        w = len(r) // n
        s = r[: w * n].reshape(w, n).std(axis=1, ddof=1)
        c4 = math.sqrt(2.0 / (n - 1)) * math.exp(math.lgamma(n / 2) - math.lgamma((n - 1) / 2))
        rows.append((f"n = {n} returns", [fmt(s.mean() / SD_DAY), fmt((s**2).mean() / VAR_DAY),
                                          fmt(s.mean() / math.sqrt((s**2).mean())), fmt(c4)]))
    table(
        "Table 5. Close-to-close: the standard deviation is biased low even when the variance is not",
        ["mean s/sigma", "mean s2/var", "E[s]/rtE[s2]", "c4(n)"],
        rows,
    )

    print("s = sample standard deviation with n-1.  The third column removes this sample's own luck in the variance")
    print("and should equal c4(n) = sqrt(2/(n-1)) * Gamma(n/2) / Gamma((n-1)/2).")
    print(f"Sampling error of a mean variance over {N_DAYS} days is about {math.sqrt(2 / N_DAYS):.3f}.")

    # ---- Table 6: intraday realised variance and the overnight gap --------
    rows = []
    for s in "AC":
        d = sims[s]
        f = scen[s]["f"]
        sess = (1 - f) * VAR_DAY
        r_cc = d["o"] + d["c"]
        delta = ((r_cc - r_cc.mean()) ** 2).sum() / d["rv_5m"].sum()
        rows.append((f"{s}: RV 1-min / session variance", [fmt(d["rv_1m"].mean() / sess)]))
        rows.append((f"{s}: RV 5-min / session variance", [fmt(d["rv_5m"].mean() / sess)]))
        rows.append((f"{s}: RV 5-min / whole-day variance", [fmt(d["rv_5m"].mean() / VAR_DAY)]))
        rows.append((f"{s}: (RV 5-min + overnight^2) / whole day", [fmt((d["rv_5m"] + d["o"] ** 2).mean() / VAR_DAY)]))
        rows.append((f"{s}: scaled RV 5-min / whole day", [fmt((delta * d["rv_5m"]).mean() / VAR_DAY)]))
        rows.append((f"{s}:   scale factor used", [fmt(delta)]))
        rows.append((f"{s}: sd of daily (RV5 + overnight^2)", [fmt((d["rv_5m"] + d["o"] ** 2).std() / VAR_DAY)]))
        rows.append((f"{s}: sd of daily scaled RV5", [fmt((delta * d["rv_5m"]).std() / VAR_DAY)]))
        rows.append((f"{s}: sd of daily squared c-c return", [fmt((r_cc**2).std() / VAR_DAY)]))
    table("Table 6. Intraday realised variance (RV), no noise", ["ratio"], rows, width=44)
    print("'sd' rows: day-to-day standard deviation of the one-day estimate, in units of the true daily variance.")

    # ---- Table 7: microstructure noise -----------------------------------
    nz = simulate(6000, noise_bp=2.0, seed=200)
    rows = [(f"RV sampled every {lab}", [fmt(nz[f"rv_{lab}"].mean() / VAR_DAY)])
            for lab in ("15s", "1m", "5m", "15m", "25m")]
    rows.append(("Subsampled 5-min RV (20 offsets)", [fmt(nz["rv_sub5m"].mean() / VAR_DAY)]))
    rows.append(("Two-scales RV, K=20", [fmt(nz["tsrv"].mean() / VAR_DAY)]))
    rows.append(("Two-scales RV, small-sample adjusted", [fmt(nz["tsrv_adj"].mean() / VAR_DAY)]))
    rows.append(("sd of daily: RV 5-min", [fmt(nz["rv_5m"].std() / VAR_DAY)]))
    rows.append(("sd of daily: subsampled 5-min RV", [fmt(nz["rv_sub5m"].std() / VAR_DAY)]))
    rows.append(("sd of daily: two-scales adjusted", [fmt(nz["tsrv_adj"].std() / VAR_DAY)]))
    table("Table 7. Noise of 2 basis points added to every 15-second price (scenario A otherwise)",
          ["ratio"], rows, width=44)
    print("Expected RV bias = 2 * (number of returns) * noise variance: "
          + ", ".join(f"{lab} {1 + 2 * n * (2e-4) ** 2 / VAR_DAY:.3f}" for lab, n in
                      (("15s", 1500), ("1m", 375), ("5m", 75), ("15m", 25), ("25m", 15))))
    print("(A 375-minute session does not divide into 30- or 60-minute bars; 25 minutes is used instead.)")

    # ---- Table 8: jumps --------------------------------------------------
    js = simulate(6000, jump_share=0.25, seed=300)
    rows = []
    for lab in ("5m", "1m"):
        for nm, key in (("RV", "rv"), ("Bipower variation", "bv"), ("MedRV", "medrv"), ("MinRV", "minrv")):
            rows.append((f"{nm}, {lab} returns", [fmt(js[f"{key}_{lab}"].mean() / VAR_DAY),
                                                  fmt(sims["A"][f"{key}_{lab}"].mean() / VAR_DAY)]))
    table("Table 8. One jump a day carrying 25% extra variance (quadratic variation = 1.25, integrated variance = 1.00)",
          ["with jumps", "no jumps"], rows, width=44)

    # ---- Table 9: realised range -----------------------------------------
    a = sims["A"]
    rows = [
        ("Realised range, 5-min bars, true highs/lows", [fmt(a["rr5_cont"].mean() / VAR_DAY), fmt(a["rr5_cont"].std() / VAR_DAY)]),
        ("Realised range, bars built from 5 1-min closes", [fmt(a["rr5_m5"].mean() / VAR_DAY), fmt(a["rr5_m5"].std() / VAR_DAY)]),
        ("RV 5-min", [fmt(a["rv_5m"].mean() / VAR_DAY), fmt(a["rv_5m"].std() / VAR_DAY)]),
        ("RV 1-min", [fmt(a["rv_1m"].mean() / VAR_DAY), fmt(a["rv_1m"].std() / VAR_DAY)]),
    ]
    table("Table 9. Realised range against realised variance, scenario A, divisor 4 ln 2", ["mean", "sd of daily"], rows, width=48)
    print(f"Theory for the sd of one day: RV with M returns sqrt(2/M): 5-min {math.sqrt(2 / 75):.3f}, "
          f"1-min {math.sqrt(2 / 375):.3f}; range with 75 bars sqrt(0.4073/75) = {math.sqrt(0.4073 / 75):.3f}.")

    # ---- Table 10: intraday seasonality ----------------------------------
    us = simulate(6000, u_shape=3.0, seed=400)
    rows = []
    for mins, key in ((60, "rv1_first60"), (187, "rv1_first187")):
        naive = us[key].mean() * (MINUTES / mins) / VAR_DAY
        share = us["profile_cum"][mins - 1]
        adj = us[key].mean() / share / VAR_DAY
        rows.append((f"after {mins} of 375 minutes", [fmt(naive), fmt(adj), fmt(share)]))
    table("Table 10. U-shaped session (variance at the open and close 4x midday): part-day RV scaled to a full session",
          ["by clock", "by profile", "share so far"], rows)

    print()
    print("Annualising check: sqrt(252 * mean daily variance) for scenario A close-to-close = "
          f"{math.sqrt(DAYS_PER_YEAR * cc_demeaned(*windows(sims['A'], WIN)).mean()):.4f} (true 0.2000)")


if __name__ == "__main__":
    main()
