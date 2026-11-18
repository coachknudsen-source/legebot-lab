# Legebot-laboratoriet

Tester hver nat legebottens fire strategier (tre 15-minutters setups og dagstrend) på 4 års 15-minutters kurser og kårer én vinder pr. regime (bullish, flat, bearish) og for dagstrend.
En strategi bliver kun vinder, hvis den består alle 4 tests og slår købt og holdt efter gebyrer.

- `strategier.json`: læses automatisk af legebotten (indstillingen `lab_url`).
- `rapport.md`: strategikort med idé, regler, resultater, de 4 tests og "hvorfor det kan fejle".

Botten tager selv nye vindere i brug. Har et regime ingen vinder, handler profilen Forsigtig ikke i det regime,
og Normal og Aggressiv handler med halv risiko.

Gebyrer som på WEEX futures: limit-ordrer 0,02 %, markedsordrer 0,08 % + prisforskel + funding. Kursdata fra Binance som stedfortræder.

Kører gratis på GitHub Actions (offentligt repo). Handler aldrig selv og har ingen nøgler.

Test uden internet: `python lab.py --syntetisk --hurtig` og `python test_lab.py`.
