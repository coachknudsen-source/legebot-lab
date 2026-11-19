#!/usr/bin/env python3
"""
LEGEBOT-LABORATORIET
====================
Tester hver nat legebottens tre setups på 4 års 15-minutters kurshistorik og kårer
én vinder og to udfordrere pr. regime (bullish, flat, bearish). Kun strategier, der
består alle 4 tests og slår købt og holdt efter gebyrer, kommer med.

Kører på GitHub Actions (se .github/workflows/laboratoriet.yml). Handler aldrig selv.
Skriver strategier.json (læses af legebotten) og rapport.md (strategikort til mennesker).

Brug:
    python lab.py            # nat: hurtig permutationstest (faste indstillinger), 1000 permutationer
    python lab.py --soendag  # grundig: optimerer forfra på hvert blandet forløb (200 permutationer)
    python lab.py --syntetisk --hurtig   # test uden internet (kunstige kurser, få permutationer)

Regler, der beskytter mod snyd med fremtiden ("lookahead"):
  * Handler besluttes på et AFSLUTTET 15-minutters lys og udføres på NÆSTE lys' åbning.
  * Regimet bruger kun afsluttede timelys. 4H-sving tæller først, når de 2 lys efter er lukket.
  * Walk-forward vælger indstillinger kun på fortiden og tester på perioden lige efter.
  * Den endelige vinder vælges på det seneste træningsvindue, aldrig på testdata.
"""
import os, sys, io, json, math, time, zipfile, datetime as dt
UTC = dt.timezone.utc
def _fra_ts(x): return dt.datetime.fromtimestamp(int(x), UTC)
def _nu(): return dt.datetime.now(UTC).replace(tzinfo=None)
import numpy as np
import pandas as pd

try:
    from numba import njit
    NUMBA = True
except Exception:  # lokalt uden numba: samme kode, bare langsommere
    NUMBA = False
    def njit(*a, **k):
        if a and callable(a[0]):
            return a[0]
        return lambda f: f

# ----------------------------------------------------------------------------- indstillinger
MOENTER = ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'DOGE', 'LINK', 'DOT', 'AVAX', 'LTC', 'BCH', 'ATOM', 'UNI', 'AAVE', 'TRX']
AAR = 4
GEBYR_M = 0.0002        # WEEX futures maker-gebyr (limit-ordre, der hviler i ordrebogen)
GEBYR_T = 0.0008        # WEEX futures taker-gebyr (markedsordre, fx stop-loss)
SLIP = 0.0005           # prisforskel på markedsordrer (samme som botten)
FUNDING = 0.0001        # funding pr. 8 timer (lange betaler, shorts modtager – typisk niveau)
KOST = GEBYR_M + GEBYR_T + SLIP   # ind med limit (maker), ud i værste fald med stop (taker + prisforskel)
VENT = 2                # en limit-ordre, der ikke er fyldt efter 2 lys (30 min), annulleres
RISIKO = 0.01           # 1 % af formuen pr. handel
MAKS_POS = 0.20         # højst 20 % af formuen i én position (profilen Normal)
MIN_RR = 2.5            # R:R efter gebyr
SETUPS = {
    0: dict(navn='Pullback-køb i bullish regime', regime='bull', kode='trend_lang', bottype='momentum',
            ide='Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.',
            hvorfor='Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter.',
            betaler='De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.'),
    1: dict(navn='Breakdown-short i bearish regime', regime='bear', kode='trend_short', bottype='momentum',
            ide='Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.',
            hvorfor='Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter.',
            betaler='Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.'),
    2: dict(navn='Range-handel i flat regime', regime='flat', kode='range', bottype='modtrend',
            ide='Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.',
            hvorfor='I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet.',
            betaler='Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.'),
    3: dict(navn='Dagstrend (udbrud på dagslys)', regime='trend', kode='dagtrend', bottype='dagtrend',
            ide='Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.',
            hvorfor='Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede.',
            betaler='Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.'),
}
GITTER = dict(lb=[10, 20, 40], stopATR=[0.5, 1.0], tp1R=[1.5, 2.0, 2.5], volF=[1.2, 1.5], limitATR=[0.0, 0.25], btcF=[0, 1])
GITTER_DAG = dict(N=[20, 55], M=[10, 20], stopATR=[2.0, 3.0], btcF=[0, 1])
DATAMAPPE = 'data'


# ----------------------------------------------------------------------------- data (Binance Vision, gratis)
def _hent(url):
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return r.read()
    except Exception:
        return None


def _laes_zip(b):
    z = zipfile.ZipFile(io.BytesIO(b))
    df = pd.read_csv(z.open(z.namelist()[0]), header=None)
    if not str(df.iloc[0, 0]).replace('.', '').isdigit():   # nogle filer har overskrift
        df = df.iloc[1:].astype(float)
    df = df.iloc[:, :6].astype(float)
    df.columns = ['t', 'o', 'h', 'l', 'c', 'v']
    t = df['t'].values
    t = np.where(t > 1e14, t / 1e6, np.where(t > 1e11, t / 1e3, t))   # mikro- eller millisekunder → sekunder
    df['t'] = t.astype(np.int64)
    return df


def hent_data(moent, aar=AAR):
    """4 års 15-minutters lys for moent/USDT fra Binance Vision. Gemmer i data/ og henter kun det, der mangler."""
    os.makedirs(DATAMAPPE, exist_ok=True)
    sym = moent + 'USDT'
    fil = os.path.join(DATAMAPPE, sym + '_15m_fut.csv.gz')
    gl = pd.read_csv(fil) if os.path.exists(fil) else pd.DataFrame(columns=['t', 'o', 'h', 'l', 'c', 'v'])
    nu = _nu()
    fra = dt.datetime(nu.year - aar, nu.month, 1)
    have = set(pd.to_datetime(gl['t'], unit='s').dt.strftime('%Y-%m-%d').unique()) if len(gl) else set()
    dele = [gl]
    m = fra
    while (m.year, m.month) < (nu.year, nu.month):
        mn = m.strftime('%Y-%m')
        if not any(d.startswith(mn) for d in have) or sum(d.startswith(mn) for d in have) < 27:
            b = (_hent(f'https://data.binance.vision/data/futures/um/monthly/klines/{sym}/15m/{sym}-15m-{mn}.zip')
                 or _hent(f'https://data.binance.vision/data/spot/monthly/klines/{sym}/15m/{sym}-15m-{mn}.zip'))
            if b:
                dele.append(_laes_zip(b))
        m = dt.datetime(m.year + (m.month == 12), m.month % 12 + 1, 1)
    d = dt.datetime(nu.year, nu.month, 1)
    while d.date() < nu.date():
        ds = d.strftime('%Y-%m-%d')
        if ds not in have:
            b = (_hent(f'https://data.binance.vision/data/futures/um/daily/klines/{sym}/15m/{sym}-15m-{ds}.zip')
                 or _hent(f'https://data.binance.vision/data/spot/daily/klines/{sym}/15m/{sym}-15m-{ds}.zip'))
            if b:
                dele.append(_laes_zip(b))
        d += dt.timedelta(days=1)
    df = pd.concat([x for x in dele if len(x)], ignore_index=True)
    if not len(df):
        return None
    df = df.drop_duplicates('t').sort_values('t')
    df = df[df['t'] >= int(fra.replace(tzinfo=dt.timezone.utc).timestamp())]
    df.to_csv(fil, index=False, compression='gzip')
    return df.reset_index(drop=True)


def hent_funding(moent, aar=AAR):
    """Historisk funding for USDT-M futures (Binance Vision, månedlige filer). Returnerer DataFrame(t, rate) eller None."""
    os.makedirs(DATAMAPPE, exist_ok=True)
    sym = moent + 'USDT'
    fil = os.path.join(DATAMAPPE, sym + '_funding.csv.gz')
    gl = pd.read_csv(fil) if os.path.exists(fil) else pd.DataFrame(columns=['t', 'rate'])
    have = set(pd.to_datetime(gl['t'], unit='s').dt.strftime('%Y-%m').unique()) if len(gl) else set()
    nu = _nu()
    m = dt.datetime(nu.year - aar, nu.month, 1)
    dele = [gl]
    while (m.year, m.month) < (nu.year, nu.month):
        mn = m.strftime('%Y-%m')
        if mn not in have:
            b = _hent(f'https://data.binance.vision/data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{mn}.zip')
            if b:
                try:
                    z = zipfile.ZipFile(io.BytesIO(b))
                    f = pd.read_csv(z.open(z.namelist()[0]))
                    tc = [c for c in f.columns if 'time' in c.lower()][0]
                    rc = [c for c in f.columns if 'rate' in c.lower()][0]
                    t = f[tc].astype(float).values
                    dele.append(pd.DataFrame(dict(t=(np.where(t > 1e11, t / 1e3, t)).astype(np.int64), rate=f[rc].astype(float).values)))
                except Exception:
                    pass
        m = dt.datetime(m.year + (m.month == 12), m.month % 12 + 1, 1)
    df = pd.concat([x for x in dele if len(x)], ignore_index=True) if any(len(x) for x in dele) else None
    if df is None or not len(df):
        return None
    df = df.drop_duplicates('t').sort_values('t')
    df.to_csv(fil, index=False, compression='gzip')
    return df.reset_index(drop=True)


def saet_funding(df, fdf):
    """Kolonnen f = funding, der betales i hvert 15-minutters lys (positiv: lange betaler). Uden data: 0,01 % hver 8. time."""
    t = df['t'].values
    f = np.where(t % 28800 == 0, FUNDING, 0.0)
    if fdf is not None and len(fdf):
        idx = np.searchsorted(t, fdf['t'].values, side='right') - 1
        ok = (idx >= 0) & (fdf['t'].values - t[np.clip(idx, 0, None)] < 900)
        sidst = int(fdf['t'].max())
        f = np.where(t <= sidst, 0.0, f)                     # rigtig historik, hvor den findes
        np.add.at(f, idx[ok], fdf['rate'].values[ok])
    df = df.copy(); df['f'] = f
    return df


def syntetisk(moent, n=int(os.environ.get('LAB_N', 35040)), seed=0):
    """Kunstige kurser til test uden internet (trend-regimer + støj + volumen)."""
    import zlib
    rng = np.random.default_rng(zlib.crc32(moent.encode()) + seed)
    drift = np.repeat(rng.normal(0, 0.00025, n // 600 + 1), 600)[:n]
    r = drift + rng.normal(0, 0.003, n)
    c = 100 * np.exp(np.cumsum(r))
    o = np.r_[c[0], c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.002, n)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.002, n)))
    v = rng.gamma(2, 500, n) * (1 + 2 * (rng.random(n) < 0.06))
    t = (1640995200 + 900 * np.arange(n)).astype(np.int64)
    return pd.DataFrame(dict(t=t, o=o, h=h, l=l, c=c, v=v))


# ----------------------------------------------------------------------------- indikatorer (som i botten)
def ema(x, n):
    return pd.Series(x).ewm(span=n, adjust=False).mean().values


def rsi(c, n=14):
    d = np.diff(c, prepend=c[0])
    up = pd.Series(np.maximum(d, 0)).ewm(alpha=1 / n, adjust=False).mean()
    dn = pd.Series(np.maximum(-d, 0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(100).values


def true_range(h, l, c):
    pc = np.r_[c[0], c[:-1]]
    return np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))


def adx(h, l, c, n=14):
    up = np.diff(h, prepend=h[0]); dn = -np.diff(l, prepend=l[0])
    pdm = np.where((up > dn) & (up > 0), up, 0.0); ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = true_range(h, l, c)
    a = lambda x: pd.Series(x).ewm(alpha=1 / n, adjust=False).mean().values
    atr_ = a(tr)
    pdi = 100 * a(pdm) / np.where(atr_ > 0, atr_, np.nan); ndi = 100 * a(ndm) / np.where(atr_ > 0, atr_, np.nan)
    dx = 100 * np.abs(pdi - ndi) / np.where(pdi + ndi > 0, pdi + ndi, np.nan)
    return pd.Series(np.nan_to_num(dx)).ewm(alpha=1 / n, adjust=False).mean().values


def aggreger(df, n):
    """15-minutters lys → større lys (n=4: 1 time, n=16: 4 timer). Kun hele, afsluttede lys."""
    g = (df['t'] // (900 * n)).values
    a = df.groupby(g).agg(t=('t', 'first'), o=('o', 'first'), h=('h', 'max'), l=('l', 'min'), c=('c', 'last'), v=('v', 'sum'), n=('t', 'size'))
    a = a[a['n'] == n].reset_index(drop=True)
    a['slut'] = (a['t'] // (900 * n) + 1) * 900 * n
    return a


def regime_serie(h1):
    """1 = bullish (over stigende 200-EMA), 2 = bearish (under faldende), 0 = flat (ADX < 20). Gælder først efter 3 lys."""
    c = h1['c'].values
    e = ema(c, 200); a = adx(h1['h'].values, h1['l'].values, c, 14)
    stig = np.r_[np.zeros(5, bool), e[5:] > e[:-5]]; fald = np.r_[np.zeros(5, bool), e[5:] < e[:-5]]
    raa = np.where(a < 20, 0, np.where((c > e) & stig, 1, np.where((c < e) & fald, 2, 0))).astype(np.int64)
    return _bekraeft(raa)


@njit(cache=True)
def _bekraeft(raa):
    ud = np.full(len(raa), -1, np.int8)
    cur = -1; run = 0; last = -9
    for i in range(len(raa)):
        run = run + 1 if raa[i] == last else 1
        last = raa[i]
        if run >= 3 and i >= 230:
            cur = raa[i]
        ud[i] = cur if i >= 230 else -1
    return ud


def forbered(df, btc=None):
    """Alt, der ikke afhænger af strategiens indstillinger, regnes én gang pr. kursforløb.
    btc = (tider, regime) for BTC – bruges som filter for de andre mønter. None = ingen filter (BTC selv)."""
    df = df.reset_index(drop=True)
    o, h, l, c, v, t = (df[k].values.astype(np.float64) for k in 'ohlcvt')
    t = df['t'].values.astype(np.int64)
    h1 = aggreger(df, 4)
    reg1 = regime_serie(h1)
    # regime for hvert 15-min-lys = regimet for det seneste AFSLUTTEDE timelys
    idx = np.searchsorted(h1['slut'].values, t + 900, side='right') - 1
    reg = np.where(idx >= 0, reg1[np.clip(idx, 0, None)], -1).astype(np.int8)
    h4 = aggreger(df, 16)
    tr4 = true_range(h4['h'].values, h4['l'].values, h4['c'].values)
    atr4_4 = pd.Series(tr4).rolling(14).mean().values
    i4 = np.searchsorted(h4['slut'].values, t + 900, side='right') - 1
    atr4 = np.where(i4 >= 0, atr4_4[np.clip(i4, 0, None)], np.nan)
    # 4H-sving: kendes først, når de 2 lys efter er lukket
    H, L = h4['h'].values.astype(np.float64), h4['l'].values.astype(np.float64)
    S4, T4 = h4['slut'].values.astype(np.int64), h4['t'].values.astype(np.int64)
    n4 = len(H)
    i = np.arange(2, max(n4 - 2, 2))
    if len(i):
        top = (H[i] > H[i-1]) & (H[i] > H[i-2]) & (H[i] >= H[i+1]) & (H[i] >= H[i+2])
        bund = (L[i] < L[i-1]) & (L[i] < L[i-2]) & (L[i] <= L[i+1]) & (L[i] <= L[i+2])
        it, ib = i[top], i[bund]
    else:
        it = ib = np.array([], np.int64)
    tom = lambda x: x if len(x) else None
    shL, shK, shT = (H[it], S4[it + 2], T4[it]) if len(it) else (np.zeros(1), np.zeros(1, np.int64), np.zeros(1, np.int64))
    slL, slK, slT = (L[ib], S4[ib + 2], T4[ib]) if len(ib) else (np.zeros(1), np.zeros(1, np.int64), np.zeros(1, np.int64))
    tp = (h + l + c) / 3
    vwap = (pd.Series(tp * v).rolling(96).sum() / pd.Series(v).rolling(96).sum()).values
    vavg = pd.Series(np.where(v > 0, v, np.nan)).rolling(34, min_periods=10).mean().shift(6).values
    mins = {lb: pd.Series(l).rolling(lb).min().shift(1).values for lb in GITTER['lb']}
    maks = {lb: pd.Series(h).rolling(lb).max().shift(1).values for lb in GITTER['lb']}
    if btc is not None:
        bi = np.searchsorted(btc[0], t, side='right') - 1
        btcreg = np.where(bi >= 0, btc[1][np.clip(bi, 0, None)], -1).astype(np.int8)
    else:
        btcreg = np.full(len(t), -1, np.int8)
    fper = df['f'].values if 'f' in df else np.where(t % 28800 == 0, FUNDING, 0.0)
    fcum = np.cumsum(fper).astype(np.float64)
    dg = aggreger(df, 96)
    trd = true_range(dg['h'].values, dg['l'].values, dg['c'].values)
    dag = dict(o=dg['o'].values.astype(np.float64), h=dg['h'].values.astype(np.float64), l=dg['l'].values.astype(np.float64),
               c=dg['c'].values.astype(np.float64), t=dg['t'].values.astype(np.int64), slut=dg['slut'].values.astype(np.int64),
               atr=pd.Series(trd).rolling(20).mean().fillna(0).values.astype(np.float64))
    di = np.clip(np.searchsorted(t, dag['slut'] - 900, side='left'), 0, len(t) - 1)   # dagens sidste 15-min-lys
    dag['btc'] = btcreg[di]; dag['fcum'] = fcum[di]
    return dict(dag=dag, btcreg=btcreg, fcum=fcum, o=o, h=h, l=l, c=c, v=v, t=t, reg=reg, atr15=pd.Series(true_range(h, l, c)).rolling(14).mean().values,
                ema21=ema(c, 21), rsi=rsi(c), vwap=vwap, vavg=vavg, atr4=atr4, shL=shL, shK=shK, shT=shT,
                slL=slL, slK=slK, slT=slT, mins=mins, maks=maks)


# ----------------------------------------------------------------------------- simulering (samme regler som botten)
@njit(cache=True)
def _simuler(o, h, l, c, v, t, reg, atr15, ema21, rsi_, vwap, vavg, atr4, rmin, rmax,
             shL, shK, shT, slL, slK, slT, btcreg, fcum, setup, lb, stopATR, tp1R, volF, limitATR, btcF, start, slut,
             kost, gm, gt, slip, vent, risiko, makspos, minrr):
    n = len(c)
    ud_ind = np.empty(n, np.int64); ud_ud = np.empty(n, np.int64); ud_pnl = np.empty(n); ud_dir = np.empty(n, np.int8)
    m = 0
    i = max(start, 60)
    ph0 = 0; ph1 = 0; pl0 = 0; pl1 = 0
    while i < min(slut, n - 1):
        r = reg[i]
        ok = (setup == 0 and r == 1) or (setup == 1 and r == 2) or (setup == 2 and r == 0)
        if not ok:
            i += 1
            continue
        # tid: ingen nye handler 14:15–15:15 UTC (US-åbning); halv risiko i weekenden
        luk = t[i] + 900
        mod = (luk // 60) % 1440
        if mod >= 855 and mod <= 915:
            i += 1
            continue
        wd = ((luk // 86400) + 4) % 7          # 0 = mandag
        weekend = wd >= 5
        # 4H-sving i vinduet (bekræftet og højst 40 4H-lys gamle)
        while ph1 < len(shK) and shK[ph1] <= luk: ph1 += 1
        while ph0 < ph1 and shT[ph0] < luk - 40 * 14400: ph0 += 1
        while pl1 < len(slK) and slK[pl1] <= luk: pl1 += 1
        while pl0 < pl1 and slT[pl0] < luk - 40 * 14400: pl0 += 1
        bedst_rr = -1.0; b_dir = 0; b_stop = 0.0; b_tp1 = 0.0; b_tp2 = 0.0; b_ent = 0.0
        for dirn in (1, -1):
            if setup == 0 and dirn == -1: continue
            if setup == 1 and dirn == 1: continue
            if btcF == 1 and ((dirn == 1 and btcreg[i] == 2) or (dirn == -1 and btcreg[i] == 1)): continue   # BTC-filter
            lang = dirn == 1
            fundet = False; lunte = 0.0; vmax = 0.0; struktur = 0.0
            for k in range(i - 1, i - 8, -1):
                if k - lb < 0 or k < 4: break
                niv = rmin[k] if lang else rmax[k]
                if niv != niv: continue
                fej = (l[k] < niv and c[k] > niv) if lang else (h[k] > niv and c[k] < niv)
                if not fej: continue
                s = h[k]
                for q in range(k - 3, k + 1):
                    if lang:
                        if h[q] > s: s = h[q]
                    else:
                        if q == k - 3 or l[q] < s: s = l[q]
                if not lang:
                    s = l[k]
                    for q in range(k - 3, k + 1):
                        if l[q] < s: s = l[q]
                mss = -1
                for j in range(k + 1, i + 1):
                    if (c[j] > s) if lang else (c[j] < s):
                        mss = j; break
                if mss < 0: continue
                if (c[i] <= s) if lang else (c[i] >= s): continue
                fundet = True; lunte = l[k] if lang else h[k]; struktur = s
                vmax = v[k] if v[k] > v[mss] else v[mss]
                break
            if not fundet: continue
            if setup == 2:   # range: kun ved 4H-støtte / -modstand
                a4 = atr4[i]
                if a4 != a4: continue
                ved = False
                if lang:
                    for z in range(pl0, pl1):
                        if abs(lunte - slL[z]) <= a4: ved = True
                else:
                    for z in range(ph0, ph1):
                        if abs(lunte - shL[z]) <= a4: ved = True
                if not ved: continue
            va = vavg[i]
            if not (va > 0) or vmax < volF * va: continue
            if lang:
                if not (c[i] > ema21[i] or c[i] > vwap[i]): continue
                if rsi_[i] >= 70: continue
            else:
                if not (c[i] < ema21[i] or c[i] < vwap[i]): continue
                if rsi_[i] <= 30: continue
            a15 = atr15[i]
            if a15 != a15: continue
            entry = c[i] - dirn * limitATR * a15     # limit-pris: lidt bedre end lukkekursen
            stop = lunte - dirn * stopATR * a15
            R = abs(entry - stop)
            if R <= 0: continue
            tp1 = entry + dirn * tp1R * R
            naer = -1.0
            if lang:
                for z in range(ph0, ph1):
                    if shL[z] > entry and (naer < 0 or shL[z] < naer): naer = shL[z]
                if naer > 0 and naer <= tp1: continue
            else:
                for z in range(pl0, pl1):
                    if slL[z] < entry and (naer < 0 or slL[z] > naer): naer = slL[z]
                if naer > 0 and naer >= tp1: continue
            tp2 = naer if naer > 0 else entry + dirn * 2 * tp1R * R
            forv = 0.5 * abs(tp1 - entry) + 0.5 * abs(tp2 - entry)
            fee = kost * entry
            if fee > 0.15 * forv: continue
            rr = (forv - fee) / (R + fee)
            if rr < minrr: continue
            if rr > bedst_rr:
                bedst_rr = rr; b_dir = dirn; b_stop = stop; b_tp1 = tp1; b_tp2 = tp2; b_ent = entry
        if b_dir == 0:
            i += 1
            continue
        # limit-ordre lagt efter lyset er lukket: fyldes kun, hvis kursen når limit-prisen inden for 'vent' lys
        e = -1
        for q in range(i + 1, min(i + 1 + vent, n)):
            if (l[q] <= b_ent) if b_dir == 1 else (h[q] >= b_ent):
                e = q; break
        if e < 0:
            i += 1
            continue
        fill = min(b_ent, o[e]) if b_dir == 1 else max(b_ent, o[e])   # åbner kursen på den gode side, fyldes til åbningen
        if (b_dir == 1 and fill <= b_stop) or (b_dir == -1 and fill >= b_stop):
            i += 1
            continue
        risk = risiko * (0.5 if weekend else 1.0)
        frac = risk / (abs(fill - b_stop) / fill)
        if frac > makspos: frac = makspos
        pnl = -frac * gm                         # maker-gebyr ved indgang
        rest = 1.0; stop = b_stop; tp1naa = False; j = e; slutj = -1
        while j < n:
            lo_ = l[j]; hi_ = h[j]
            ramt_stop = (lo_ <= stop) if b_dir == 1 else (hi_ >= stop)
            if ramt_stop:                         # stop først (forsigtigt, hvis både stop og mål er i samme lys) – markedsordre
                px = stop * (1 - b_dir * slip)
                if j > e:
                    px = (min(px, o[j]) if b_dir == 1 else max(px, o[j]))   # hul forbi stoppet: fyldes til åbningen
                pnl += frac * rest * (b_dir * (px / fill - 1) - gt)
                slutj = j; break
            if (hi_ >= b_tp2) if b_dir == 1 else (lo_ <= b_tp2):   # mål: limit-ordre (maker)
                pnl += frac * rest * (b_dir * (b_tp2 / fill - 1) - gm)
                slutj = j; break
            if (not tp1naa) and ((hi_ >= b_tp1) if b_dir == 1 else (lo_ <= b_tp1)):
                pnl += frac * 0.5 * (b_dir * (b_tp1 / fill - 1) - gm)
                rest = 0.5; tp1naa = True
                stop = fill * (1 + b_dir * kost)  # break-even inkl. gebyrer
            j += 1
        if slutj < 0:
            px = c[n - 1]
            pnl += frac * rest * (b_dir * (px / fill - 1) - gt)
            slutj = n - 1
        pnl -= frac * b_dir * (fcum[slutj] - fcum[e - 1])     # rigtig funding i holdeperioden (lange betaler ved positiv sats)
        ud_ind[m] = e; ud_ud[m] = slutj; ud_pnl[m] = pnl; ud_dir[m] = b_dir
        m += 1
        i = slutj + 1                             # én position ad gangen pr. marked
    return ud_ind[:m], ud_ud[:m], ud_pnl[:m], ud_dir[:m]


@njit(cache=True)
def _simuler_dag(o, h, l, c, atrd, btc, fcum, N, M, stopATR, btcF, start, slut, gt, slip, risiko, makspos):
    """Dagstrend: signal på et AFSLUTTET dagslys, indgang på næste dags åbning (markedsordre), glidende stop og
    udgang, når lukkekursen bryder M dages kanal den anden vej."""
    n = len(c)
    ud_ind = np.empty(n, np.int64); ud_ud = np.empty(n, np.int64); ud_pnl = np.empty(n); ud_dir = np.empty(n, np.int8)
    m = 0
    i = max(start, N + 2, M + 2, 21)
    while i < min(slut, n - 1):
        hoej = h[i - N]; lav = l[i - N]
        for q in range(i - N, i):
            if h[q] > hoej: hoej = h[q]
            if l[q] < lav: lav = l[q]
        hoej1 = h[i - 1 - N]; lav1 = l[i - 1 - N]
        for q in range(i - 1 - N, i - 1):
            if h[q] > hoej1: hoej1 = h[q]
            if l[q] < lav1: lav1 = l[q]
        d = 0
        if c[i] > hoej and c[i - 1] <= hoej1: d = 1
        elif c[i] < lav and c[i - 1] >= lav1: d = -1
        a = atrd[i]
        if btcF == 1 and ((d == 1 and btc[i] == 2) or (d == -1 and btc[i] == 1)): d = 0   # BTC-filter
        if d == 0 or not (a > 0):
            i += 1
            continue
        e = i + 1
        fill = o[e] * (1 + d * slip)
        stop = fill - d * stopATR * a
        frac = risiko / (abs(fill - stop) / fill)
        if frac > makspos: frac = makspos
        pnl = -frac * gt
        j = e; slutj = -1
        while j < n:
            if (l[j] <= stop) if d == 1 else (h[j] >= stop):
                px = stop * (1 - d * slip)
                px = min(px, o[j]) if d == 1 else max(px, o[j])
                pnl += frac * (d * (px / fill - 1) - gt)
                slutj = j; break
            # efter lukning: flyt stoppet med trenden og tjek udgangskanalen
            ny = c[j] - d * stopATR * atrd[j]
            if (d == 1 and ny > stop) or (d == -1 and ny < stop): stop = ny
            if j - M >= 0 and j + 1 < n:
                ud = False
                if d == 1:
                    lv = l[j - M]
                    for q in range(j - M, j):
                        if l[q] < lv: lv = l[q]
                    ud = c[j] < lv
                else:
                    hv = h[j - M]
                    for q in range(j - M, j):
                        if h[q] > hv: hv = h[q]
                    ud = c[j] > hv
                if ud:
                    px = o[j + 1] * (1 - d * slip)
                    pnl += frac * (d * (px / fill - 1) - gt)
                    slutj = j + 1; break
            j += 1
        if slutj < 0:
            pnl += frac * (d * (c[n - 1] / fill - 1) - gt)
            slutj = n - 1
        pnl -= frac * d * (fcum[slutj] - fcum[e - 1])   # rigtig funding i holdeperioden
        ud_ind[m] = e; ud_ud[m] = slutj; ud_pnl[m] = pnl; ud_dir[m] = d
        m += 1
        i = slutj + 1
    return ud_ind[:m], ud_ud[:m], ud_pnl[:m], ud_dir[:m]


G = globals()


def simuler(F, setup, p, start=0, slut=None):
    """start/slut er indeks i 15-minutters lysene. Returnerer indeks i 15-minutters lysene (dagstrend omregnes)."""
    slut = len(F['c']) if slut is None else slut
    if setup == 3:
        D = F['dag']
        if len(D['c']) < 30:
            z = np.zeros(0, np.int64); return z, z, np.zeros(0), np.zeros(0, np.int8)
        t0 = F['t'][start] if start < len(F['t']) else F['t'][-1] + 900
        t1 = F['t'][slut - 1] + 900 if slut > 0 else 0
        ds = int(np.searchsorted(D['slut'], t0 + 1, side='left'))       # første dag, der lukker efter start
        de = int(np.searchsorted(D['slut'], t1, side='right'))          # dage lukket inden slut
        ind, ud, pnl, d = _simuler_dag(D['o'], D['h'], D['l'], D['c'], D['atr'], D['btc'], D['fcum'], int(p['N']), int(p['M']), float(p['stopATR']),
                                       int(p.get('btcF', 0)), ds, de, G['GEBYR_T'], G['SLIP'], RISIKO, MAKS_POS)
        # dagsindeks → indeks i 15-minutters lysene (dagens sidste lys)
        til15 = np.clip(np.searchsorted(F['t'], D['slut'][ud] - 900, side='left'), 0, len(F['t']) - 1)
        fra15 = np.clip(np.searchsorted(F['t'], D['t'][ind], side='left'), 0, len(F['t']) - 1)
        return fra15, til15, pnl, d
    return _simuler(F['o'], F['h'], F['l'], F['c'], F['v'], F['t'], F['reg'], F['atr15'], F['ema21'], F['rsi'], F['vwap'],
                    F['vavg'], F['atr4'], F['mins'][p['lb']], F['maks'][p['lb']], F['shL'], F['shK'], F['shT'],
                    F['slL'], F['slK'], F['slT'], F['btcreg'], F['fcum'], setup, p['lb'], float(p['stopATR']), float(p['tp1R']), float(p['volF']), float(p['limitATR']),
                    int(p.get('btcF', 0)), start, slut,
                    G['KOST'], G['GEBYR_M'], G['GEBYR_T'], G['SLIP'], G['VENT'], RISIKO, MAKS_POS, MIN_RR)


# ----------------------------------------------------------------------------- nøgletal
def noegletal(handler):
    """handler: liste af (udgangstid, pnl). Giver netto, fald, antal, vinderrate, profitfaktor, længste tabsrække, værste måned."""
    if not handler:
        return dict(netto=0.0, fald=0.0, antal=0, vind=0.0, pf=0.0, raekke=0, vaerste_maaned=0.0, maaneder={})
    h = sorted(handler)
    p = np.array([x[1] for x in h])
    kurve = np.cumsum(p); top = np.maximum.accumulate(np.r_[0, kurve])[1:]
    fald = float(np.max(top - kurve)) if len(p) else 0.0
    gev, tab = p[p > 0].sum(), -p[p < 0].sum()
    raekke = m = 0
    for x in p:
        m = m + 1 if x <= 0 else 0; raekke = max(raekke, m)
    mdr = {}
    for tt, x in h:
        k = _fra_ts(int(tt)).strftime('%Y-%m'); mdr[k] = mdr.get(k, 0) + x
    return dict(netto=float(p.sum()), fald=fald, antal=len(p), vind=float((p > 0).mean()), pf=float(gev / tab) if tab > 0 else 99.0,
                raekke=raekke, vaerste_maaned=float(min(mdr.values())) if mdr else 0.0, maaneder=mdr)


def maal(nt):
    """Optimeringsmål: afkast i forhold til største fald – kræver mindst 30 handler."""
    if nt['antal'] < 30:
        return -1e9
    return nt['netto'] / max(nt['fald'], 0.01)


def koebt_og_holdt(FS, regime, start_t=None, slut_t=None):
    """Lige vægtet købt og holdt, kun i de lys hvor markedet var i regimet. Afkast og største fald."""
    serier = []
    for F in FS:
        lr = np.diff(np.log(F['c']), prepend=np.log(F['c'][0]))
        if regime is None:
            m = F['reg'] >= 0                     # dagstrend: alle perioder med kendt regime
        else:
            m = (F['reg'] == regime)
            m = np.r_[False, m[:-1]]              # regimet kendt FØR lyset
        if start_t is not None: m &= F['t'] >= start_t
        if slut_t is not None: m &= F['t'] < slut_t
        serier.append(pd.Series(np.where(m, lr, 0.0), index=F['t']))
    s = pd.concat(serier, axis=1).fillna(0).mean(axis=1).sort_index()
    k = s.cumsum().values
    top = np.maximum.accumulate(np.r_[0, k])[1:]
    return dict(afkast=float(np.expm1(k[-1])) if len(k) else 0.0, fald=float(np.max(top - k)) if len(k) else 0.0)


def slaar_bh(nt, bh):
    """Slår købt og holdt efter gebyrer, målt som afkast pr. største fald (og skal tjene penge)."""
    if nt['netto'] <= 0:
        return False
    st = nt['netto'] / max(nt['fald'], 0.005)
    b = bh['afkast'] / max(bh['fald'], 0.005)
    return st > max(b, 0)


# ----------------------------------------------------------------------------- permutation (Masters' metode)
def permuter(df, rng, fra=0, til=None):
    """Blander lysene i [fra, til): mellemrum mellem lys og lysenes form blandes hver for sig.
    Kursens samlede udvikling og fordeling bevares – mønstrene i tid ødelægges."""
    til = len(df) if til is None else til
    lo, lh, ll, lc = (np.log(df[k].values) for k in 'ohlc')
    gap = np.r_[0, lo[1:] - lc[:-1]]
    rh, rl, rc = lh - lo, ll - lo, lc - lo
    v = df['v'].values.copy()
    idx = np.arange(len(df))
    a = idx[fra + 1:til]
    p1 = rng.permutation(a); p2 = rng.permutation(a)
    rh2, rl2, rc2, v2, gap2 = rh.copy(), rl.copy(), rc.copy(), v.copy(), gap.copy()
    rh2[a], rl2[a], rc2[a], v2[a] = rh[p1], rl[p1], rc[p1], v[p1]
    gap2[a] = gap[p2]
    # luk[i] = luk[i-1] + gap[i] + krop[i]; før vinduet: originalen, efter: originale bevægelser
    trin = gap + rc
    trin2 = trin.copy(); trin2[a] = gap2[a] + rc2[a]
    nc = lc.copy()
    if len(df) > fra + 1:
        nc[fra + 1:] = lc[fra] + np.cumsum(trin2[fra + 1:])
    no = nc - np.where(np.arange(len(df)) > fra, rc2, rc)
    no[:fra + 1] = lo[:fra + 1]
    ud = pd.DataFrame(dict(t=df['t'].values, o=np.exp(no), h=np.exp(no + rh2), l=np.exp(no + rl2), c=np.exp(nc), v=v2))
    if 'f' in df:
        ud['f'] = df['f'].values
    return ud


# ----------------------------------------------------------------------------- tests
def varianter(setup=0):
    import itertools
    g = GITTER_DAG if setup == 3 else GITTER
    for v in itertools.product(*g.values()):
        yield dict(zip(g.keys(), v))


def koer_alle(FS, setup, p, fra_t=None, til_t=None):
    hs = []
    for F in FS:
        a = 0 if fra_t is None else int(np.searchsorted(F['t'], fra_t))
        b = len(F['t']) if til_t is None else int(np.searchsorted(F['t'], til_t))
        ind, ud, pnl, d = simuler(F, setup, p, a, b)
        hs += [(int(F['t'][x]), float(y)) for x, y in zip(ud, pnl)]
    return hs


def optimer(FS, setup, fra_t=None, til_t=None, VAR=None):
    res = []
    for p in (VAR or list(varianter())):
        nt = noegletal(koer_alle(FS, setup, p, fra_t, til_t))
        res.append((maal(nt), p, nt))
    res.sort(key=lambda x: -x[0])
    return res


def naboer(p, alle):
    """Varianter, der kun afviger ét trin på én indstilling – holder strategien på tværs af indstillinger?"""
    ud = []
    for q in alle:
        diff = [k for k in p if q[k] != p[k]]
        if len(diff) == 1:
            k = diff[0]; g = (GITTER_DAG if 'N' in p else GITTER)[k]
            if abs(g.index(q[k]) - g.index(p[k])) == 1:
                ud.append(q)
    return ud


def laboratorium(DFS, grundig=False, perms=1000, perms_grundig=200, hurtig=False, log=print, navne=None):
    t0 = time.time()
    navne = navne or [str(i) for i in range(len(DFS))]
    btc = None
    if 'BTC' in navne:
        Fb = forbered(DFS[navne.index('BTC')])
        btc = (Fb['t'], Fb['reg'])
    BTCS = [None if n == 'BTC' else btc for n in navne]   # BTC-filteret gælder de andre mønter
    FS = [forbered(df, BTCS[i]) for i, df in enumerate(DFS)]
    alle_t = np.concatenate([F['t'] for F in FS])
    t_start, t_slut = int(alle_t.min()), int(alle_t.max())
    is_slut = t_start + int((t_slut - t_start) * 0.75)          # in-sample: de første 3 af 4 år
    VARS = {s_: list(varianter(s_)) for s_ in SETUPS}
    if hurtig:
        h_ = [dict(lb=20, stopATR=0.5, tp1R=2.0, volF=1.5, limitATR=0.0, btcF=1), dict(lb=20, stopATR=0.5, tp1R=2.0, volF=1.2, limitATR=0.0, btcF=0), dict(lb=10, stopATR=0.5, tp1R=2.0, volF=1.5, limitATR=0.25, btcF=1)]
        VARS = {0: h_, 1: h_, 2: h_, 3: [dict(N=20, M=10, stopATR=2.0, btcF=1), dict(N=55, M=20, stopATR=3.0, btcF=0)]}
    rng = np.random.default_rng(42)
    aar, kvartal = 365 * 86400, 91 * 86400
    folder, t = [], t_start + aar
    while t < t_slut:
        folder.append((t - aar, t, min(t + kvartal, t_slut + 1)))
        t += kvartal
    oos_start = folder[0][1] if folder else is_slut

    # ---- GATE 1 + 3 for alle setups (ægte data)
    info = {}
    for setup, S in SETUPS.items():
        VAR = VARS[setup]
        reg_kode = {'bull': 1, 'bear': 2, 'flat': 0, 'trend': None}[S['regime']]
        log(f"\n=== {S['navn']} ({len(VAR)} varianter) ===")
        is_res = optimer(FS, setup, None, is_slut, VAR)
        bh_is = koebt_og_holdt(FS, reg_kode, None, is_slut)
        kandidater = []
        for score, p, nt in is_res[:3]:
            g1 = nt['netto'] > 0 and nt['pf'] >= 1.2 and nt['antal'] >= 30 and slaar_bh(nt, bh_is)
            kandidater.append(dict(p=p, is_nt=nt, g1=g1, perm=[]))
        log(f"  in-sample bedst: {is_res[0][1]} netto {is_res[0][2]['netto']:+.3f} handler {is_res[0][2]['antal']}")
        valg, wf_handler = [], []
        for (a, b, c_) in folder:
            best = optimer(FS, setup, a, b, VAR)[0][1]
            valg.append((a, b, c_, best))
            wf_handler += koer_alle(FS, setup, best, b, c_)
        wf_nt = noegletal(wf_handler)
        bh_wf = koebt_og_holdt(FS, reg_kode, oos_start, None)
        g3 = wf_nt['netto'] > 0 and wf_nt['antal'] >= 20 and slaar_bh(wf_nt, bh_wf)
        log(f"  walk-forward: netto {wf_nt['netto']:+.3f} handler {wf_nt['antal']} · bestået={g3}")
        info[setup] = dict(S=S, reg_kode=reg_kode, kandidater=kandidater, bh_is=bh_is, valg=valg, wf_nt=wf_nt, bh_wf=bh_wf, g3=g3, perm2=[], perm4=[])

    # ---- GATE 2 + 4: hvert blandet forløb genbruges til alle tre setups (sparer tid)
    n2 = 8 if hurtig else (perms_grundig if grundig else perms)
    n4 = 8 if hurtig else perms
    log(f"\nPermutationstest: {n2} in-sample ({'optimeret forfra' if grundig else 'faste indstillinger'}) + {n4} walk-forward ...")
    for k in range(max(n2, n4)):
        if k < n2:
            PF = [forbered(permuter(df, rng, 0, int(np.searchsorted(df['t'].values, is_slut))), BTCS[i]) for i, df in enumerate(DFS)]
            for setup, I in info.items():
                if grundig:
                    I['perm2'].append(optimer(PF, setup, None, is_slut, VARS[setup])[0][0])
                else:
                    for c in I['kandidater']:
                        c['perm'].append(maal(noegletal(koer_alle(PF, setup, c['p'], None, is_slut))))
        if k < n4:
            PF = [forbered(permuter(df, rng, int(np.searchsorted(df['t'].values, oos_start))), BTCS[i]) for i, df in enumerate(DFS)]
            for setup, I in info.items():
                hs = []
                for (a, b, c_, best) in I['valg']:
                    hs += koer_alle(PF, setup, best, b, c_)
                nt = noegletal(hs)
                I['perm4'].append(maal(nt) if I['wf_nt']['antal'] >= 30 else nt['netto'])
        if (k + 1) % 100 == 0:
            log(f"  {k + 1} permutationer · {round(time.time() - t0)} sek.")

    resultat = {}
    for setup, I in info.items():
        S, wf_nt, bh_wf, bh_is = I['S'], I['wf_nt'], I['bh_wf'], I['bh_is']
        VAR = VARS[setup]
        for c in I['kandidater']:
            fl = I['perm2'] if grundig else c['perm']
            c['p_is'] = (sum(1 for x in fl if x >= maal(c['is_nt'])) + 1) / (len(fl) + 1)
            c['g2'] = c['p_is'] < 0.01
        aegte4 = maal(wf_nt) if wf_nt['antal'] >= 30 else wf_nt['netto']
        p_wf = (sum(1 for x in I['perm4'] if x >= aegte4) + 1) / (len(I['perm4']) + 1)
        g3, g4 = I['g3'], p_wf < 0.05
        # vinderen: indstillinger fra det SENESTE træningsvindue (aldrig valgt på testdata)
        seneste = optimer(FS, setup, t_slut - aar, t_slut + 1, VAR)
        kort = []
        for rang, (score, p, nt) in enumerate(seneste[:3]):
            c = next((x for x in I['kandidater'] if x['p'] == p), None)
            nab = naboer(p, VAR)
            nab_ok = [noegletal(koer_alle(FS, setup, q, None, is_slut))['netto'] > 0 for q in nab] if not hurtig else []
            robust = (sum(nab_ok) / len(nab_ok)) if nab_ok else None
            if c:
                g1, p_is, g2, is_nt = c['g1'], c['p_is'], c['g2'], c['is_nt']
            else:   # ikke blandt de 3 bedste in-sample → tjek in-sample uden permutation
                is_nt = noegletal(koer_alle(FS, setup, p, None, is_slut))
                g1 = is_nt['netto'] > 0 and is_nt['pf'] >= 1.2 and is_nt['antal'] >= 30 and slaar_bh(is_nt, bh_is)
                p_is, g2 = None, False
            bestaaet = bool(g1 and g2 and g3 and g4 and (robust is None or robust >= 0.5))
            kar = 1 + (wf_nt['netto'] > 0) + (wf_nt['fald'] < 0.10) + (wf_nt['antal'] >= 50) + (wf_nt['raekke'] <= 6)
            kar = int(max(1, min(5, kar - (0 if slaar_bh(wf_nt, bh_wf) else 1))))
            kort.append(dict(
                rang=rang, bestaaet=bestaaet, setup=S['kode'], bottype=S['bottype'], regime=S['regime'], navn=S['navn'],
                indstillinger=p, karakter=kar, ide=S['ide'], hvorfor=S['hvorfor'], betaler=S['betaler'],
                regler=regler_tekst(setup, p),
                in_sample=dict(netto=is_nt['netto'], handler=is_nt['antal'], koebt_og_holdt=bh_is['afkast']),
                walk_forward=dict(netto=wf_nt['netto'], handler=wf_nt['antal'], vinderrate=wf_nt['vind'], profitfaktor=wf_nt['pf'],
                                  stoerste_fald=wf_nt['fald'], laengste_tabsraekke=wf_nt['raekke'], vaerste_maaned=wf_nt['vaerste_maaned'],
                                  koebt_og_holdt=bh_wf['afkast'], koebt_og_holdt_fald=bh_wf['fald']),
                tests=dict(in_sample=bool(g1), permutation_p=p_is, permutation=bool(g2), walk_forward=bool(g3), wf_permutation_p=p_wf, wf_permutation=bool(g4),
                           permutationer=n2, metode='optimeret forfra på hvert blandet forløb' if grundig else 'faste indstillinger'),
                robusthed=robust,
                advarsel='Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger ' + str(max(wf_nt['raekke'], 4) + 2) + '.',
                kan_fejle=hvorfor_fejl(wf_nt, p_is, p_wf, robust)))
        # bestået vinder først – ellers den bedste udfordrer, der bestod
        kort.sort(key=lambda k: (not k['bestaaet'], k['rang']))
        for i, k in enumerate(kort): k['rang'] = i
        resultat[S['regime']] = kort
        log(f"{S['navn']}: vinder {kort[0]['indstillinger']} bestået={kort[0]['bestaaet']} karakter={kort[0]['karakter']} p={kort[0]['tests']['permutation_p']} p_wf={p_wf:.3f}")
    return dict(genereret=_nu().strftime('%Y-%m-%dT%H:%MZ'), tid_sek=round(time.time() - t0),
                periode=dict(fra=_fra_ts(t_start).strftime('%Y-%m-%d'), til=_fra_ts(t_slut).strftime('%Y-%m-%d'),
                             in_sample_til=_fra_ts(is_slut).strftime('%Y-%m-%d')),
                grundig=grundig, regimer=resultat)


def regler_tekst(setup, p):
    st = 'Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position.'
    if setup == 3:
        return dict(indgang=f"Dagens lukkekurs bryder over de seneste {p['N']} dages top (køb) eller under bunden (short). Markedsordre næste dag.",
                    stop=f"{p['stopATR']} × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.",
                    exit=f"Når lukkekursen bryder de seneste {p['M']} dages kanal den anden vej, eller stoppet rammes.",
                    stoerrelse=st + (' BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.' if p.get('btcF') else ''))
    return dict(indgang=f"Sweep af det laveste/højeste niveau de seneste {p['lb']} lys (15 min) + strukturskift, volumen ≥ {p['volF']}× normalt, bekræftet af EMA21 eller VWAP. "
                        + (f"Limit-ordre {p['limitATR']} × ATR under/over lukkekursen" if p['limitATR'] else "Limit-ordre til lukkekursen") + f" (maker-gebyr); annulleres efter {VENT} lys uden fyld.",
                stop=f"Bag sweep-lunten + {p['stopATR']} × ATR(15 min). Markedsordre (taker-gebyr).",
                exit=f"TP1 ved {p['tp1R']}R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau ({2*p['tp1R']}R uden niveau).",
                stoerrelse=st + ' R:R efter gebyr ≥ 2,5.' + (' BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.' if p.get('btcF') else ''))


def hvorfor_fejl(nt, p_is, p_wf, robust):
    g = []
    if nt['antal'] < 100: g.append(f"kun {nt['antal']} handler uden for træningsdata – tilfældigheder fylder meget")
    if p_is is None: g.append('permutationstesten blev ikke kørt for netop disse indstillinger')
    elif p_is >= 0.01: g.append(f"et blandet marked klarede sig lige så godt i {round(p_is*100)} % af forsøgene (p={p_is:.3f}) – kan være held")
    elif p_is > 0.005: g.append(f"permutationstesten er tæt på grænsen (p={p_is:.3f})")
    if p_wf >= 0.05: g.append(f"på usete data klarede blandede markeder sig lige så godt i {round(p_wf*100)} % af forsøgene (p={p_wf:.3f})")
    elif p_wf > 0.02: g.append(f"walk-forward-permutationen er tæt på grænsen (p={p_wf:.3f})")
    if robust is not None and robust < 0.6: g.append(f"kun {round(robust*100)} % af nabo-indstillingerne tjener penge – kan være én heldig værdi")
    if nt['raekke'] >= 6: g.append(f"lange tabsrækker ({nt['raekke']}) – Sentinel kan stoppe botten")
    g.append('backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen')
    g.append('markedet kan skifte karakter, så fortidens edge forsvinder')
    return g


# ----------------------------------------------------------------------------- rapport
def pct(x): return f"{x*100:+.1f} %" if x is not None else '–'


def rapport(res, moenter, kilde):
    L = [f"# Legebot-laboratoriet – strategikort", '',
         f"Genereret {res['genereret']} · data {res['periode']['fra']} til {res['periode']['til']} (in-sample til {res['periode']['in_sample_til']}) · kilde: {kilde} · markeder: {', '.join(moenter)}",
         f"Permutationstest: {'grundig (søndag)' if res['grundig'] else 'nat'} · kørselstid {res['tid_sek']} sek.", '',
         'Afkast er summen af handlernes resultat i % af formuen med 1 % risiko pr. handel, efter WEEX-gebyrer (maker 0,02 %, taker 0,08 %), prisforskel og funding. '
         'Købt og holdt er lige vægtet og kun i de perioder, hvor markedet var i regimet.', '']
    for reg in ['bull', 'flat', 'bear', 'trend']:
        kort = res['regimer'].get(reg, [])
        L.append(f"## Regime: {dict(bull='bullish', flat='flat', bear='bearish', trend='alle (dagstrend)')[reg]}")
        if not kort or not kort[0]['bestaaet']:
            L.append('**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**')
        for k in kort:
            rolle = 'VINDER' if k['rang'] == 0 else f"Udfordrer {k['rang']}"
            wf, ts = k['walk_forward'], k['tests']
            L += ['', f"### {rolle}: {k['navn']} – {'BESTÅET' if k['bestaaet'] else 'IKKE BESTÅET'} · karakter {k['karakter']}/5",
                  f"- **Idé:** {k['ide']}",
                  f"- **Hvorfor edgen findes:** {k['hvorfor']} **Hvem betaler:** {k['betaler']}",
                  f"- **Indgang:** {k['regler']['indgang']}", f"- **Stop:** {k['regler']['stop']}", f"- **Exit:** {k['regler']['exit']}",
                  f"- **Størrelse:** {k['regler']['stoerrelse']}",
                  f"- **Resultat uden for træningsdata (walk-forward):** {pct(wf['netto'])} på {wf['handler']} handler · {round(wf['vinderrate']*100)} % vundne · profitfaktor {wf['profitfaktor']:.2f} · største fald {pct(-wf['stoerste_fald'])} · købt og holdt i regimet {pct(wf['koebt_og_holdt'])} (fald {pct(-wf['koebt_og_holdt_fald'])})",
                  f"- **De 4 tests:** in-sample {'✔' if ts['in_sample'] else '✘'} · permutation {'✔' if ts['permutation'] else '✘'} (p={ts['permutation_p'] if ts['permutation_p'] is None else round(ts['permutation_p'],4)}, {ts['permutationer']} stk., {ts['metode']}) · walk-forward {'✔' if ts['walk_forward'] else '✘'} · walk-forward-permutation {'✔' if ts['wf_permutation'] else '✘'} (p={round(ts['wf_permutation_p'],4)})",
                  f"- **Værste måned:** {pct(wf['vaerste_maaned'])} · **længste tabsrække:** {wf['laengste_tabsraekke']} · **holder på tværs af indstillinger:** {'–' if k['robusthed'] is None else str(round(k['robusthed']*100)) + ' % af naboerne tjener penge'}",
                  f"- **Første advarselstegn:** {k['advarsel']}",
                  f"- **HVORFOR DET KAN FEJLE:** " + '; '.join(k['kan_fejle']) + '.']
        L.append('')
    L += ['## Sidste tjek før en vinder kåres',
          '- Vinder den på data, den aldrig har set? → walk-forward-testen.',
          '- Slår den købt og holdt efter gebyrer? → målt i perioderne med regimet, pr. største fald.',
          '- Holder den på tværs af indstillinger, eller er det én heldig værdi? → robusthed (naboer).',
          '- Slog et blandet marked den? → permutationstestene.',
          '- Lækker der tal fra fremtiden? → beslutning på afsluttede lys, udførelse på næste åbning, regime og 4H-sving kun fra afsluttede lys.',
          '', 'Vælg det kedelige og beviste frem for det spændende og heldige.']
    return '\n'.join(L)


def botfil(res):
    """Den lille fil legebotten læser: vinderens indstillinger pr. regime (eller null = ingen bevist strategi). 'trend' = dagstrend."""
    ud = dict(genereret=res['genereret'], periode=res['periode'], regimer={})
    for reg, kort in res['regimer'].items():
        v = kort[0] if kort and kort[0]['bestaaet'] else None
        ud['regimer'][reg] = None if not v else dict(setup=v['setup'], bottype=v['bottype'], karakter=v['karakter'], **v['indstillinger'],
                                                     wf_netto=v['walk_forward']['netto'], wf_handler=v['walk_forward']['handler'],
                                                     p=v['tests']['permutation_p'], p_wf=v['tests']['wf_permutation_p'])
        ud['regimer'][reg + '_udfordrere'] = [dict(setup=k['setup'], bestaaet=k['bestaaet'], karakter=k['karakter'], **k['indstillinger']) for k in kort[1:3]]
    ud['alle_kort'] = res['regimer']
    return ud


def main():
    a = sys.argv[1:]
    grundig = '--soendag' in a or (_nu().weekday() == 6 and '--nat' not in a)
    hurtig = '--hurtig' in a
    moenter = MOENTER[:3] if hurtig else MOENTER
    if '--syntetisk' in a:
        DFS = [saet_funding(syntetisk(m), None) for m in moenter]; kilde = 'kunstige testkurser (IKKE rigtige)'
    else:
        DFS, ok = [], []
        for m in moenter:
            df = hent_data(m)
            if df is not None and len(df) > 20000:
                DFS.append(saet_funding(df, hent_funding(m))); ok.append(m)
            else:
                print(f"Springer {m} over – for lidt data")
        moenter = ok; kilde = 'Binance Vision USDT-M futures (15-minutters lys og rigtig funding) som stedfortræder for WEEX'
        if not DFS:
            sys.exit('Ingen data kunne hentes')
    print(f"numba: {'ja' if NUMBA else 'nej (langsomt)'} · markeder: {len(DFS)} · grundig: {grundig}")
    res = laboratorium(DFS, grundig=grundig, hurtig=hurtig, navne=moenter)
    with open('strategier.json', 'w', encoding='utf-8') as f:
        json.dump(botfil(res), f, ensure_ascii=False, indent=1, default=float)
    with open('rapport.md', 'w', encoding='utf-8') as f:
        f.write(rapport(res, moenter, kilde))
    print('\nFærdig: strategier.json og rapport.md er skrevet.')


if __name__ == '__main__':
    main()
