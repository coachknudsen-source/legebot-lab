# Legebot-laboratoriet – strategikort

Genereret 2026-11-25T03:41Z · data 2022-11-01 til 2026-11-23 (in-sample til 2025-11-17) · kilde: Binance Vision USDT-M futures (15-minutters lys og rigtig funding) som stedfortræder for WEEX · markeder: BTC, ETH, SOL, XRP, ADA, DOGE, LINK, DOT, AVAX, LTC, BCH, ATOM, UNI, AAVE, TRX
Permutationstest: nat · kørselstid 2411 sek.

Afkast er summen af handlernes resultat i % af formuen med 1 % risiko pr. handel, efter WEEX-gebyrer (maker 0,02 %, taker 0,08 %), prisforskel og funding. Købt og holdt er lige vægtet og kun i de perioder, hvor markedet var i regimet.

## Regime: bullish
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Pullback-køb i bullish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.
- **Hvorfor edgen findes:** Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter. **Hvem betaler:** De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 10 lys (15 min) + strukturskift, volumen ≥ 1.5× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** -7.8 % på 260 handler · 31 % vundne · profitfaktor 0.90 · største fald -26.2 % · købt og holdt i regimet +31.7 % (fald -68.0 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.3886)
- **Værste måned:** -3.7 % · **længste tabsrække:** 17 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 19.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 39 % af forsøgene (p=0.389); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (17) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Pullback-køb i bullish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.
- **Hvorfor edgen findes:** Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter. **Hvem betaler:** De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 10 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** -7.8 % på 260 handler · 31 % vundne · profitfaktor 0.90 · største fald -26.2 % · købt og holdt i regimet +31.7 % (fald -68.0 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.3886)
- **Værste måned:** -3.7 % · **længste tabsrække:** 17 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 19.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 39 % af forsøgene (p=0.389); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (17) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Pullback-køb i bullish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb, når en optrend laver et dyk, der fejer stop under et oplagt bund, og kursen derefter bryder op igen.
- **Hvorfor edgen findes:** Tradere sætter stop under oplagte bunde. Når de bliver ramt, sælges der i panik til de tålmodige købere – ofte lige før trenden fortsætter. **Hvem betaler:** De tradere, hvis stop bliver fejet, og dem der shorter for sent i en optrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 10 lys (15 min) + strukturskift, volumen ≥ 1.5× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** -7.8 % på 260 handler · 31 % vundne · profitfaktor 0.90 · største fald -26.2 % · købt og holdt i regimet +31.7 % (fald -68.0 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.3886)
- **Værste måned:** -3.7 % · **længste tabsrække:** 17 · **holder på tværs af indstillinger:** 14 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 19.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 39 % af forsøgene (p=0.389); kun 14 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (17) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Regime: flat
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Range-handel i flat regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.
- **Hvorfor edgen findes:** I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet. **Hvem betaler:** Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -14.6 % på 124 handler · 24 % vundne · profitfaktor 0.57 · største fald -16.3 % · købt og holdt i regimet -18.8 % (fald -70.5 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.8971)
- **Værste måned:** -2.4 % · **længste tabsrække:** 22 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 24.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 90 % af forsøgene (p=0.897); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (22) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Range-handel i flat regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.
- **Hvorfor edgen findes:** I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet. **Hvem betaler:** Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 20 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -14.6 % på 124 handler · 24 % vundne · profitfaktor 0.57 · største fald -16.3 % · købt og holdt i regimet -18.8 % (fald -70.5 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.8971)
- **Værste måned:** -2.4 % · **længste tabsrække:** 22 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 24.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 90 % af forsøgene (p=0.897); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (22) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Range-handel i flat regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Køb ved range-bunden og short ved range-toppen, når et sweep af niveauet bliver afvist.
- **Hvorfor edgen findes:** I et sidelæns marked bliver udbrud ofte afvist. Sweep af range-kanten fanger dem, der jagter udbruddet. **Hvem betaler:** Tradere, der køber udbrud over toppen eller sælger brud under bunden i et marked uden trend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 20 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre til lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 0.5 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** -14.6 % på 124 handler · 24 % vundne · profitfaktor 0.57 · største fald -16.3 % · købt og holdt i regimet -18.8 % (fald -70.5 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.8971)
- **Værste måned:** -2.4 % · **længste tabsrække:** 22 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 24.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 90 % af forsøgene (p=0.897); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (22) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Regime: bearish
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Breakdown-short i bearish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.
- **Hvorfor edgen findes:** Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter. **Hvem betaler:** Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre 0.25 × ATR under/over lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** -21.7 % på 255 handler · 29 % vundne · profitfaktor 0.76 · største fald -29.4 % · købt og holdt i regimet -23.2 % (fald -70.6 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.7512)
- **Værste måned:** -6.8 % · **længste tabsrække:** 21 · **holder på tværs af indstillinger:** 0 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 23.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 75 % af forsøgene (p=0.751); kun 0 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (21) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Breakdown-short i bearish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.
- **Hvorfor edgen findes:** Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter. **Hvem betaler:** Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre 0.25 × ATR under/over lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.0R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (4.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** -21.7 % på 255 handler · 29 % vundne · profitfaktor 0.76 · største fald -29.4 % · købt og holdt i regimet -23.2 % (fald -70.6 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.7512)
- **Værste måned:** -6.8 % · **længste tabsrække:** 21 · **holder på tværs af indstillinger:** 14 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 23.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 75 % af forsøgene (p=0.751); kun 14 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (21) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Breakdown-short i bearish regime – IKKE BESTÅET · karakter 1/5
- **Idé:** Short, når en nedtrend laver et hop, der fejer stop over en oplagt top, og kursen derefter bryder ned igen.
- **Hvorfor edgen findes:** Shortere sætter stop over oplagte toppe. Når de bliver købt ud, er der ingen købere tilbage, og nedtrenden fortsætter. **Hvem betaler:** Shortere, der bliver fejet ud, og købere der "køber dykket" i en nedtrend.
- **Indgang:** Sweep af det laveste/højeste niveau de seneste 40 lys (15 min) + strukturskift, volumen ≥ 1.2× normalt, bekræftet af EMA21 eller VWAP. Limit-ordre 0.25 × ATR under/over lukkekursen (maker-gebyr); annulleres efter 2 lys uden fyld.
- **Stop:** Bag sweep-lunten + 1.0 × ATR(15 min). Markedsordre (taker-gebyr).
- **Exit:** TP1 ved 2.5R med limit-ordre: halvdelen lukkes og stop flyttes til break-even inkl. gebyrer. TP2 ved næste 4H-niveau (5.0R uden niveau).
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. R:R efter gebyr ≥ 2,5.
- **Resultat uden for træningsdata (walk-forward):** -21.7 % på 255 handler · 29 % vundne · profitfaktor 0.76 · største fald -29.4 % · købt og holdt i regimet -23.2 % (fald -70.6 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✘ · walk-forward-permutation ✘ (p=0.7512)
- **Værste måned:** -6.8 % · **længste tabsrække:** 21 · **holder på tværs af indstillinger:** 17 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 23.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 75 % af forsøgene (p=0.751); kun 17 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (21) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Regime: alle (dagstrend)
**Ingen strategi bestod alle 4 tests. Profilen Forsigtig handler ikke her; Normal og Aggressiv handler kun med halv risiko.**

### VINDER: Dagstrend (udbrud på dagslys) – IKKE BESTÅET · karakter 3/5
- **Idé:** Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.
- **Hvorfor edgen findes:** Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede. **Hvem betaler:** Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.
- **Indgang:** Dagens lukkekurs bryder over de seneste 55 dages top (køb) eller under bunden (short). Markedsordre næste dag.
- **Stop:** 2.0 × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.
- **Exit:** Når lukkekursen bryder de seneste 10 dages kanal den anden vej, eller stoppet rammes.
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position.
- **Resultat uden for træningsdata (walk-forward):** +38.0 % på 415 handler · 40 % vundne · profitfaktor 1.22 · største fald -52.8 % · købt og holdt i regimet -17.9 % (fald -145.9 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✔ · walk-forward-permutation ✘ (p=0.1259)
- **Værste måned:** -10.6 % · **længste tabsrække:** 14 · **holder på tværs af indstillinger:** 25 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 16.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 13 % af forsøgene (p=0.126); kun 25 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (14) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 1: Dagstrend (udbrud på dagslys) – IKKE BESTÅET · karakter 3/5
- **Idé:** Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.
- **Hvorfor edgen findes:** Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede. **Hvem betaler:** Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.
- **Indgang:** Dagens lukkekurs bryder over de seneste 55 dages top (køb) eller under bunden (short). Markedsordre næste dag.
- **Stop:** 2.0 × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.
- **Exit:** Når lukkekursen bryder de seneste 10 dages kanal den anden vej, eller stoppet rammes.
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position. BTC-filter: ingen køb, når BTC er bearish, og ingen short, når BTC er bullish.
- **Resultat uden for træningsdata (walk-forward):** +38.0 % på 415 handler · 40 % vundne · profitfaktor 1.22 · største fald -52.8 % · købt og holdt i regimet -17.9 % (fald -145.9 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✔ · walk-forward-permutation ✘ (p=0.1259)
- **Værste måned:** -10.6 % · **længste tabsrække:** 14 · **holder på tværs af indstillinger:** 25 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 16.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 13 % af forsøgene (p=0.126); kun 25 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (14) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

### Udfordrer 2: Dagstrend (udbrud på dagslys) – IKKE BESTÅET · karakter 3/5
- **Idé:** Køb, når dagens lukkekurs bryder over de seneste N dages top, og short, når den bryder under bunden. Hold så længe trenden varer.
- **Hvorfor edgen findes:** Kryptomarkeder har lange trends, fordi nyheder og flow spreder sig langsomt. Få, store gevinster betaler for mange små tab, og de få handler holder gebyrerne nede. **Hvem betaler:** Dem, der sælger for tidligt i en optrend eller køber for tidligt i en nedtrend, og dem der handler mod trenden.
- **Indgang:** Dagens lukkekurs bryder over de seneste 55 dages top (køb) eller under bunden (short). Markedsordre næste dag.
- **Stop:** 2.0 × ATR(20 dage) fra indgangen. Stoppet følger med trenden for hver dag, der lukker.
- **Exit:** Når lukkekursen bryder de seneste 20 dages kanal den anden vej, eller stoppet rammes.
- **Størrelse:** Styres af brugerens profil i botten (risiko pr. handel, maks. pr. position, dagsmål og tabsgrænse). Testet med 1 % risiko og højst 20 % pr. position.
- **Resultat uden for træningsdata (walk-forward):** +38.0 % på 415 handler · 40 % vundne · profitfaktor 1.22 · største fald -52.8 % · købt og holdt i regimet -17.9 % (fald -145.9 %)
- **De 4 tests:** in-sample ✘ · permutation ✘ (p=None, 1000 stk., faste indstillinger) · walk-forward ✔ · walk-forward-permutation ✘ (p=0.1259)
- **Værste måned:** -10.6 % · **længste tabsrække:** 14 · **holder på tværs af indstillinger:** 25 % af naboerne tjener penge
- **Første advarselstegn:** Papirhandlen ligger under nul 3 uger i træk, eller den længste tabsrække overstiger 16.
- **HVORFOR DET KAN FEJLE:** permutationstesten blev ikke kørt for netop disse indstillinger; på usete data klarede blandede markeder sig lige så godt i 13 % af forsøgene (p=0.126); kun 25 % af nabo-indstillingerne tjener penge – kan være én heldig værdi; lange tabsrækker (14) – Sentinel kan stoppe botten; backtesten bruger Binance-kurser som stedfortræder for WEEX, og limit-ordrer antages fyldt, så snart kursen rører prisen; markedet kan skifte karakter, så fortidens edge forsvinder.

## Sidste tjek før en vinder kåres
- Vinder den på data, den aldrig har set? → walk-forward-testen.
- Slår den købt og holdt efter gebyrer? → målt i perioderne med regimet, pr. største fald.
- Holder den på tværs af indstillinger, eller er det én heldig værdi? → robusthed (naboer).
- Slog et blandet marked den? → permutationstestene.
- Lækker der tal fra fremtiden? → beslutning på afsluttede lys, udførelse på næste åbning, regime og 4H-sving kun fra afsluttede lys.

Vælg det kedelige og beviste frem for det spændende og heldige.