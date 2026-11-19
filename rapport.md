# Legebot-laboratoriet – strategikort

Genereret 2026-11-19T00:29Z · data 2022-11-01 til 2026-11-17 (in-sample til 2025-11-13) · kilde: Binance Vision 15-minutters lys (USDT-par) som stedfortræder for WEEX · markeder: BTC, ETH, SOL, XRP, ADA, DOGE, LINK, DOT, AVAX, LTC, BCH, ATOM, UNI, AAVE, TRX
Permutationstest: nat · kørselstid 2424 sek.

Afkast er summen af handlernes resultat i % af formuen med 1 % risiko pr. handel, efter WEEX-gebyrer (maker 0,02 %, taker 0,08 %), prisforskel og funding. Købt og holdt er lige vægtet og kun i de perioder, hvor markedet var i regimet.

## Regime: bullish
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Pullback-køb i bullish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.
- **Hvorfor edgen findes:** Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter. **Hvem betaler:** De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 20 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -24.0 % på 353 handler · 29 % vundne · profitfaktor 0.79 · største fald -37.9 % · købt og holdt i regimet +41.3 % (fald -71.0 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.5504)
- **Værste måned:** -5.2 % · **længste tabsrække:** 14 · **holder på tværs af indstillinger:** 29 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 16.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 55 % af forsøgene (p=0.550); kun 29 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (14) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Pullback-køb i bullish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.
- **Hvorfor edgen findes:** Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter. **Hvem betaler:** De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 20 lys (15 min) + strukturskift, volumen ≥ 1.5× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -24.0 % på 353 handler · 29 % vundne · profitfaktor 0.79 · største fald -37.9 % · købt og holdt i regimet +41.3 % (fald -71.0 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.5504)
- **Værste måned:** -5.2 % · **længste tabsrække:** 14 · **holder på tværs af indstillinger:** 29 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 16.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 55 % af forsøgene (p=0.550); kun 29 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (14) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Pullback-køb i bullish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.
- **Hvorfor edgen findes:** Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter. **Hvem betaler:** De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 20 lys (15 min) + strukturskift, volumen ≥ 1.5× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -24.0 % på 353 handler · 29 % vundne · profitfaktor 0.79 · største fald -37.9 % · købt og holdt i regimet +41.3 % (fald -71.0 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.5504)
- **Værste måned:** -5.2 % · **længste tabsrække:** 14 · **holder på tværs af indstillinger:** 67 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 16.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 55 % af forsøgene (p=0.550); lange tabsrækker (14) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Regime: flat
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Range-handel i flat regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.
- **Hvorfor edgen findes:** I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet. **Hvem betaler:** Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre 0.25 × ATR under/over lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -11.0 % på 126 handler · 27 % vundne · profitfaktor 0.66 · største fald -12.6 % · købt og holdt i regimet -22.6 % (fald -66.2 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.8841)
- **Værste måned:** -2.0 % · **længste tabsrække:** 11 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 13.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 88 % af forsøgene (p=0.884); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (11) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Range-handel i flat regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.
- **Hvorfor edgen findes:** I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet. **Hvem betaler:** Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -11.0 % på 126 handler · 27 % vundne · profitfaktor 0.66 · største fald -12.6 % · købt og holdt i regimet -22.6 % (fald -66.2 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.8841)
- **Værste måned:** -2.0 % · **længste tabsrække:** 11 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 13.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 88 % af forsøgene (p=0.884); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (11) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Range-handel i flat regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.
- **Hvorfor edgen findes:** I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet. **Hvem betaler:** Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre 0.25 × ATR under/over lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -11.0 % på 126 handler · 27 % vundne · profitfaktor 0.66 · største fald -12.6 % · købt og holdt i regimet -22.6 % (fald -66.2 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.8841)
- **Værste måned:** -2.0 % · **længste tabsrække:** 11 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 13.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 88 % af forsøgene (p=0.884); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (11) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Regime: bearish
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Breakdown-short i bearish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.
- **Hvorfor edgen findes:** Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter. **Hvem betaler:** Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.5× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -14.9 % på 242 handler · 28 % vundne · profitfaktor 0.84 · største fald -31.4 % · købt og holdt i regimet -20.0 % (fald -70.3 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.4625)
- **Værste måned:** -7.4 % · **længste tabsrække:** 20 · **holder på tværs af indstillinger:** 40 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 22.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 46 % af forsøgene (p=0.463); kun 40 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (20) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Breakdown-short i bearish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.
- **Hvorfor edgen findes:** Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter. **Hvem betaler:** Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.5× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -14.9 % på 242 handler · 28 % vundne · profitfaktor 0.84 · største fald -31.4 % · købt og holdt i regimet -20.0 % (fald -70.3 %)
- **De 4 tests:** in-sample ✔ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.4625)
- **Værste måned:** -7.4 % · **længste tabsrække:** 20 · **holder på tværs af indstillinger:** 67 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 22.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 46 % af forsøgene (p=0.463); lange tabsrækker (20) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Breakdown-short i bearish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.
- **Hvorfor edgen findes:** Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter. **Hvem betaler:** Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -14.9 % på 242 handler · 28 % vundne · profitfaktor 0.84 · største fald -31.4 % · købt og holdt i regimet -20.0 % (fald -70.3 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.4625)
- **Værste måned:** -7.4 % · **længste tabsrække:** 20 · **holder på tværs af indstillinger:** 20 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 22.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 46 % af forsøgene (p=0.463); kun 20 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (20) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Regime: alle (dagstrend)
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Dagstrend (udbrud på dagslys) – IKKE BESTÅET · karakter 3/5
- **Idé:** Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.
- **Hvorfor edgen findes:** Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede. **Hvem betaler:** Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.
- **Indgang:** Dagens lukkekurs bryder over de seneste 55 dages top (køb) eller under bunden (short). Markedsordre næste dag.
- **Stop:** 2.0 × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.
- **Exit:** Når lukkekursen bryder de seneste 10 dages kanal den anden vej, eller stoppet rammes.
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position.
- **Resultat uden for træningsdata (walk-forward):** +50.3 % på 441 handler · 39 % vundne · profitfaktor 1.28 · største fald -52.5 % · købt og holdt i regimet -12.5 % (fald -142.7 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✔ · walk-forward-permutation ✘ (p=0.1119)
- **Værste måned:** -15.0 % · **længste tabsrække:** 13 · **holder på tværs af indstillinger:** 67 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 15.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 11 % af forsøgene (p=0.112); lange tabsrækker (13) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Dagstrend (udbrud på dagslys) – IKKE BESTÅET · karakter 3/5
- **Idé:** Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.
- **Hvorfor edgen findes:** Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede. **Hvem betaler:** Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.
- **Indgang:** Dagens lukkekurs bryder over de seneste 55 dages top (køb) eller under bunden (short). Markedsordre næste dag.
- **Stop:** 2.0 × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.
- **Exit:** Når lukkekursen bryder de seneste 20 dages kanal den anden vej, eller stoppet rammes.
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position.
- **Resultat uden for træningsdata (walk-forward):** +50.3 % på 441 handler · 39 % vundne · profitfaktor 1.28 · største fald -52.5 % · købt og holdt i regimet -12.5 % (fald -142.7 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✔ · walk-forward-permutation ✘ (p=0.1119)
- **Værste måned:** -15.0 % · **længste tabsrække:** 13 · **holder på tværs af indstillinger:** 67 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 15.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 11 % af forsøgene (p=0.112); lange tabsrækker (13) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Dagstrend (udbrud på dagslys) – IKKE BESTÅET · karakter 3/5
- **Idé:** Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.
- **Hvorfor edgen findes:** Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede. **Hvem betaler:** Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.
- **Indgang:** Dagens lukkekurs bryder over de seneste 20 dages top (køb) eller under bunden (short). Markedsordre næste dag.
- **Stop:** 3.0 × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.
- **Exit:** Når lukkekursen bryder de seneste 20 dages kanal den anden vej, eller stoppet rammes.
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position.
- **Resultat uden for træningsdata (walk-forward):** +50.3 % på 441 handler · 39 % vundne · profitfaktor 1.28 · største fald -52.5 % · købt og holdt i regimet -12.5 % (fald -142.7 %)
- **De 4 tests:** in-sample ✔ · permutation ✘ (p=0.1209, 1000 stk., faste indstillinger) · walk-forward ✔ · walk-forward-permutation ✘ (p=0.1119)
- **Værste måned:** -15.0 % · **længste tabsrække:** 13 · **holder på tværs af indstillinger:** 100 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 15.
- **HVORFOR DET KAN FEJLE:** et blandet marked klarede sig lige så godt i 12 % af forsøgene (p=0.121) – kan være held; på usete data klarede blandede markeder sig lige så godt i 11 % af forsøgene (p=0.112); lange tabsrækker (13) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Sidste tjek før en vinder kåres
- Vinder den på data, den aldrig har set? → walk-forward-testen.
- Slår den købt og holdt efter gebyrer? → målt i perioderne med regimet, pr. største fald.
- Holder den på tværs af indstillinger, eller er det én heldig værdi? → robusthed (naboer).
- Slog et blandet marked den? → permutationstestene.
- Lækker der tal fra fremtiden? → beslutning på afsluttede lys, udførelse på næste åbning, regime og 4H-sving kun fra afsluttede lys.

Vælg det kedelige og beviste frem for det spændende og heldige.