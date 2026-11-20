# Buduje podstrony miast (lista 40 miast od klienta, mail 20.11.2026 23:14) z gotowego index.html:
# ten sam wyglad (styl, naglowek, stopka, karty produktow), unikalny opis kazdego miasta, bez listy miast na stronie.
# Uruchamiac PO build.py.  Wynik: /wanny-z-hydromasazem-<miasto>/index.html + sitemap.xml
import re, html as H, unicodedata

BAZA = 'https://disaster26.github.io/treg-koncepcja/'
idx = open('index.html', encoding='utf-8').read()

def wytnij(a, b, s=idx):
    i = s.index(a); j = s.index(b, i); return s[i:j]

STYL = re.search(r'<style>.*?</style>', idx, re.S).group(0)
STYL = STYL.replace('url(fonts/', 'url(../fonts/')
STYL = STYL.replace('</style>', '''
.mia{padding:clamp(36px,5vw,80px) 0 clamp(40px,5vw,72px);background:var(--g)}
.okr{font-size:.95rem;color:var(--mut);margin-bottom:18px}.okr a{color:var(--mut)}
.mia h1{font-size:clamp(34px,3.6vw,68px);font-stretch:92%;max-width:22ch}
.mia .lead{max-width:72ch;font-size:clamp(18px,1.25vw,22px);margin-top:20px;color:var(--ink)}
.mia .lead+.lead{margin-top:14px;color:var(--mut);font-size:clamp(17px,1.1vw,20px)}
.mia .akc{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.btn.wa{background:#1a9e4b}.btn.wa::after{border:2.5px solid #fff;border-radius:50%}.btn.wa:hover{background:#13843d}
.faq{max-width:900px}.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:clamp(18px,1.2vw,22px);list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}.faq summary::after{content:"+";font-size:1.4em;line-height:.8;color:var(--aq)}
.faq details[open] summary::after{content:"\\2212"}.faq p{margin:12px 0 0;max-width:75ch;color:var(--mut)}
.mkon{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.mia .wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(28px,4vw,80px);align-items:center}
.mia .fot{position:relative;margin:0;padding:0 0 clamp(40px,5vw,90px) 0}
.mia .fot .w{display:block;width:100%;max-width:1000px;height:auto;aspect-ratio:4/3;object-fit:cover;border:3px solid var(--aq);padding:10px;background:#fff}
.mia .fot .b{position:absolute;right:-8px;bottom:0;width:min(44%,320px);height:auto;background:#fff;border-bottom:10px solid var(--apv);box-shadow:0 14px 34px rgba(0,0,0,.18)}
@media (max-width:900px){.mia .wrap{grid-template-columns:1fr}.mia .fot{display:none}}
</style>''')
STYL = re.sub(r'\n?/\*[^*]*\*/', '', STYL) if False else STYL

NAGL = wytnij('<header class="top"', '</header>') + '</header>'
STOPKA = wytnij('<footer class="stopka">', '</footer>') + '</footer>'
LB = wytnij('<div class="lb"', '</div>') + '</div>'
tor = lambda i: re.findall(r'<article class="prod">.*?</article>', wytnij(f'id="{i}"', '</section>'), re.S)
WANNY, BIEZNIE = tor('tw'), tor('tb')

def popraw_linki(s):
    s = s.replace('href="#start"', 'href="../"')
    for k in ('filmy', 'firma', 'sauny', 'opinie'):
        s = s.replace(f'href="#{k}"', f'href="../#{k}"')
    return s.replace('src="img/', 'src="../img/').replace('data-src="img/', 'data-src="../img/').replace('data-lb="img/', 'data-lb="../img/').replace('srcset="img/', 'srcset="../img/').replace(', img/', ', ../img/')

NAGL, STOPKA = popraw_linki(NAGL), popraw_linki(STOPKA)
WANNY = [popraw_linki(x) for x in WANNY]; BIEZNIE = [popraw_linki(x) for x in BIEZNIE]


import json, os
from itertools import combinations
from miasta_dane import M, FAQ
assert len(M) == 40 and len({m[0] for m in M}) == 40

def slug(t):
    t = t.replace('ł', 'l').replace('Ł', 'L')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

def rot(lst, k):
    k %= len(lst); return lst[k:] + lst[:k]

KOMB = list(combinations(range(len(FAQ)), 3))
WA = 'https://wa.me/48660489335'
FW = ['w9014', 'w9011', 'w8008', 'w8008c', 'w9001']
FB = ['futura', 'premium', 'top']
E = H.escape
strony = []
for i, (m, w, dop, woj, wst, krot) in enumerate(M):
    sl = 'wanny-z-hydromasazem-' + slug(m)
    url = f'{BAZA}{sl}/'
    f = dict(w=w, d=dop)
    tytul = f'Wanny z hydromasażem i bieżnie {w} | TREG'
    opis = f'Wanny z hydromasażem Aquaholm i bieżnie APVsport z dostawą do {dop}. {krot} Raty 0%, PayPo, BLIK.'
    if len(opis) > 160:
        opis = f'Wanny z hydromasażem i bieżnie z dostawą do {dop}. {krot} Raty 0%, PayPo, BLIK.'
    assert len(opis) <= 160, (m, len(opis))
    faq = [(q.format(**f), a.format(**f)) for q, a in (FAQ[j] for j in KOMB[(i * 7) % len(KOMB)])]
    faqh = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    ld = json.dumps({'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'TREG', 'item': BAZA},
            {'@type': 'ListItem', 'position': 2, 'name': f'Wanny z hydromasażem i bieżnie {w}', 'item': url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]},
        ensure_ascii=False).replace('</', '<\\/')
    tw = '\n'.join(rot(WANNY, i)); tb = '\n'.join(rot(BIEZNIE, i * 2))
    strona = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{E(tytul)}</title>
<meta name="description" content="{E(opis)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="../fonts/archivo-rdzen.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../fonts/archivo-pl.woff2" crossorigin>
{STYL}
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
{NAGL}

<main id="tresc">
<section class="mia" aria-labelledby="h1">
  <div class="wrap">
    <div>
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / {E(m)}</nav>
    <h1 id="h1">Wanny z hydromasażem i bieżnie elektryczne {E(w)}</h1>
    <p class="lead">{E(wst)}</p>
    <div class="akc">
      <a class="btn aq" href="#wanny">Zobacz wanny</a>
      <a class="btn apv" href="#bieznie">Zobacz bieżnie</a>
      <a class="btn wa" href="{WA}" target="_blank" rel="noopener">Zapytaj na WhatsAppie</a>
    </div>
    </div>
    <figure class="fot"><img class="w" src="../img/{FW[i % len(FW)]}-1-1200.webp" width="1200" height="900" fetchpriority="high" decoding="async" alt="Wanna z hydromasażem Aquaholm Premium Line"><img class="b" src="../img/{FB[i % len(FB)]}-640.webp" width="640" height="560" loading="lazy" decoding="async" alt="Bieżnia elektryczna APVsport APV8000"></figure>
  </div>
</section>

<section class="sek" id="wanny" data-k="aq" aria-labelledby="h-wanny">
  <div class="wrap">
    <div class="sg">
      <div>
        <h2 id="h-wanny"><span class="kw aq"></span>Wanny z hydromasażem Aquaholm</h2>
        <p class="lead">Seria Premium Line, prostokątne i narożne, białe i czarne. Przy każdej wannie wymiary, wyposażenie, cena i dostępność ze sklepu.</p>
      </div>
      <div class="nav" data-nav="tw"><button type="button" data-k="-1" aria-label="Poprzednie wanny"></button><button type="button" data-k="1" aria-label="Następne wanny"></button></div>
    </div>
    <div class="tor" id="tw" data-tor>
{tw}
    </div>
  </div>
</section>

<section class="sek szary" id="bieznie" data-k="apv" aria-labelledby="h-bieznie">
  <div class="wrap">
    <div class="sg">
      <div>
        <h2 id="h-bieznie"><span class="kw apv"></span>Bieżnie elektryczne APVsport</h2>
        <p class="lead">Seria APV8000 z pasem biegowym 145 x 58 cm i dotykowym ekranem Android, z silnikiem 5 KM, 6 KM albo w wersji komercyjnej.</p>
      </div>
      <div class="nav" data-nav="tb"><button type="button" data-k="-1" aria-label="Poprzednie bieżnie"></button><button type="button" data-k="1" aria-label="Następne bieżnie"></button></div>
    </div>
    <div class="tor" id="tb" data-tor>
{tb}
    </div>
  </div>
</section>

<section class="sek" id="dostawa" aria-labelledby="h-dostawa">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-dostawa">Dostawa do {E(dop)}, płatności i zwroty</h2></div></div>
    <div class="info4">
      <div><h3><span class="kw aq"></span>Dostawa</h3><ul><li>Kurierem, także przesyłki nadwymiarowe i bardzo ciężkie</li><li>W Polsce zwykle 1 dzień roboczy od nadania (deklaracja firmy kurierskiej)</li><li>Koszt dostawy doliczany według cennika z dnia zakupu</li></ul></div>
      <div><h3><span class="kw apv"></span>Płatności</h3><ul><li>Raty 0%</li><li>PayPo: zapłata po 30 dniach</li><li>BLIK i przelew</li><li>Gotówką przy odbiorze</li></ul></div>
      <div><h3><span class="kw aq"></span>Gwarancja i serwis</h3><ul><li>Dokument gwarancyjny i instrukcja montażu w komplecie</li><li>Serwis gwarancyjny i pogwarancyjny w całym kraju, 33 punkty serwisowe</li><li>Własny magazyn części zamiennych</li></ul></div>
      <div><h3><span class="kw apv"></span>Zwroty</h3><ul><li>14 dni na odstąpienie od umowy</li><li>Zwrot pieniędzy w ciągu 7 dni roboczych</li><li>Przesyłkę sprawdza się przy kurierze</li></ul></div>
    </div>
  </div>
</section>

<section class="sek szary" id="pytania" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-faq">Pytania o zakup i dostawę</h2></div></div>
    <div class="faq">{faqh}</div>
  </div>
</section>

<section class="sek" id="kontakt" aria-labelledby="h-kontakt">
  <div class="wrap">
    <h2 id="h-kontakt">Zadzwoń albo napisz</h2>
    <p class="lead" style="max-width:62ch;color:var(--mut);margin-top:14px">Odpowiemy na pytania o model, termin i dostawę {E(w)}. Telefon od poniedziałku do piątku, 9:00-18:00.</p>
    <div class="mkon">
      <a class="btn ciem" href="tel:+48503538038">Zadzwoń: 503 538 038</a>
      <a class="btn wa" href="{WA}" target="_blank" rel="noopener">WhatsApp: 660 489 335</a>
      <a class="btn aq" href="mailto:sklep@treg.pl">sklep@treg.pl</a>
    </div>
  </div>
</section>
</main>

{STOPKA}
{LB}
<script src="../app.js" defer></script>
<script src="../wa.js" data-firma="TREG" data-kolor="#1e2124" defer></script>
</body>
</html>
'''
    os.makedirs(sl, exist_ok=True)
    open(f'{sl}/index.html', 'w', encoding='utf-8').write(strona)
    strony.append(sl)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + f'<url><loc>{BAZA}</loc></url>\n' + ''.join(f'<url><loc>{BAZA}{s}/</loc></url>\n' for s in strony) + '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('miasta:', len(strony))
