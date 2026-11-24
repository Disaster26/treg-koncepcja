# Wzorcowa karta produktu treg.pl (uklad wzorowany na urbogym.pl, propozycja klienta 22.11.2026):
# galeria + cena i zakup obok, najwazniejsze cechy, staly pasek zakupu, nawigacja po sekcjach,
# cechy w blokach zdjecie + tekst, pelna tabela parametrow (wiersze cieniowane), filmy, dostawa, opinie, podobne produkty.
# Dane: aquaholm.pl (WooCommerce Store API, produkt 20185), sprawdzone 24.11.2026. Uruchamiac PO build.py.
import re, json, os, html as H
from miasta import STYL, NAGL, STOPKA, LB, BIEZNIE, BAZA, WA
E = H.escape
SLUG = 'bieznia-apv8000-futura-prestige-6km'
URL = f'{BAZA}{SLUG}/'
NAZWA = 'Bieżnia elektryczna APV8000 Futura Prestige 6 KM'

STYL_P = STYL.replace('</style>', '''
.kp{padding:clamp(22px,3vw,44px) 0 clamp(40px,5vw,80px)}
.kp .okr{font-size:.95rem;color:var(--mut);margin-bottom:18px}.kp .okr a{color:var(--mut)}
.kp-g{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(28px,4vw,80px);align-items:start}
.gl{position:relative;max-width:950px}
.gl .duze{display:block;width:100%;border:0;padding:0;background:#fff;cursor:zoom-in;aspect-ratio:950/779}
.gl .duze img{width:100%;height:100%;object-fit:contain}
.mini{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:10px;margin-top:14px}
.mini button{border:2px solid var(--line);background:#fff;padding:4px;cursor:pointer;aspect-ratio:1}
.mini button img{width:100%;height:100%;object-fit:contain}
.mini button[aria-current="true"]{border-color:var(--apv)}
.zak .marka{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--mut)}
.zak h1{font-size:clamp(30px,2.5vw,48px);font-stretch:92%;line-height:1.08;margin-top:10px}
.zak .ocz{display:inline-block;margin-top:12px;color:var(--mut);font-size:.95rem}
.zak .cena{margin-top:18px;padding-top:0}.zak .cena b{font-size:clamp(34px,2.6vw,46px)}
.zak .oszcz{display:inline-block;background:var(--apv);color:#fff;font-weight:700;font-size:.85rem;padding:4px 8px}
.zak .dost{margin-top:10px}
.kl{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:9px}
.kl li{position:relative;padding-left:30px;line-height:1.45}
.kl li::before{content:"";position:absolute;left:2px;top:.28em;width:7px;height:13px;border:solid #1e8a4f;border-width:0 3px 3px 0;transform:rotate(45deg)}
.opc{display:flex;gap:12px;align-items:flex-start;margin-top:22px;padding:14px 16px;background:var(--g);cursor:pointer}
.opc input{width:22px;height:22px;margin:2px 0 0;accent-color:var(--apv);flex:none}
.opc small{display:block;color:var(--mut)}
.kup{display:flex;gap:10px;margin-top:16px}
.ilosc{display:flex;border:2px solid var(--ink)}
.ilosc button{width:44px;border:0;background:#fff;font-size:1.3rem;cursor:pointer}
.ilosc input{width:46px;border:0;text-align:center;font:700 1.05rem Archivo,Arial,sans-serif;-moz-appearance:textfield}
.ilosc input::-webkit-inner-spin-button{display:none}
.kup .dok{flex:1;margin:0;min-height:58px;font-size:1.08rem}
.zauf{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;margin-top:22px;padding-top:20px;border-top:1px solid var(--line);font-size:.93rem}
.zauf span{display:flex;gap:10px;align-items:center}.zauf .kw{width:11px;height:11px}
.zest{margin-top:18px;font-size:.93rem;color:var(--mut)}
.zakl{position:sticky;top:var(--hh);z-index:20;background:#fff;border-bottom:1px solid var(--line)}
.zakl .wrap{display:flex;gap:clamp(16px,2.6vw,44px);overflow-x:auto;scrollbar-width:none}
.zakl a{flex:none;padding:16px 0 13px;font-weight:700;color:var(--mut);text-decoration:none;border-bottom:3px solid transparent}
.zakl a:hover,.zakl a.on{color:var(--ink);border-bottom-color:var(--apv)}
.cech{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,80px);align-items:center;margin-top:clamp(44px,5vw,90px)}
.cech:first-of-type{margin-top:0}
.cech:nth-of-type(even) .cf{order:2}
.cech .cf{margin:0}.cech .cf img{width:100%;height:auto;background:#fff}
.cech small{display:block;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:.8rem;color:var(--apv)}
.cech h3{font-size:clamp(24px,1.9vw,36px);font-stretch:92%;margin-top:8px}
.cech p{margin-top:14px;color:var(--mut);max-width:58ch}
.par{width:100%;max-width:1100px;border-collapse:collapse;font-size:clamp(15.5px,1vw,18px)}
.par th,.par td{text-align:left;padding:13px 18px;vertical-align:top}
.par th{width:46%;font-weight:600;color:var(--mut)}
.par tr:nth-child(odd){background:#eef1f4}.par tr:nth-child(even){background:#fff}
.szary .par tr:nth-child(even){background:#fff}.szary .par tr:nth-child(odd){background:#e2e7ec}
.par caption{text-align:left;font-weight:800;font-size:1.15rem;padding:0 0 12px}
.fl2{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,1.4vw,24px)}
.fl2 .film figcaption{color:var(--ink)}
.pas{position:fixed;left:0;right:0;bottom:0;z-index:40;background:#fff;box-shadow:0 -6px 24px rgba(0,0,0,.14);transform:translateY(110%);transition:transform .25s}
.pas.on{transform:none}
.pas .wrap{display:flex;align-items:center;gap:18px;padding:10px 300px 10px 0}
#tresc .sek{scroll-margin-top:calc(var(--hh) + 56px)}
.pas .n{flex:1;min-width:0;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pas b{font-size:1.4rem;font-stretch:90%}
.pas .dok{margin:0;min-height:48px;padding:0 22px}
@media (max-width:900px){.zakl{position:static}#tresc .sek{scroll-margin-top:calc(var(--hh) + 64px)}.pas .wrap{padding-right:96px}.kp-g{grid-template-columns:minmax(0,1fr)}.cech{grid-template-columns:minmax(0,1fr)}.cech:nth-of-type(even) .cf{order:0}.fl2{grid-template-columns:minmax(0,1fr)}.mini{grid-template-columns:repeat(7,minmax(54px,1fr));overflow-x:auto}}
@media (max-width:560px){.zauf{grid-template-columns:1fr}.pas .n{display:none}.pas .wrap{justify-content:flex-start;padding-right:84px}.par th,.par td{padding:11px 12px}.par th{width:52%}}
@media (prefers-reduced-motion:reduce){.pas{transition:none}}
</style>''')

GAL = [('pf-g1', 950, 779, 'Bieżnia APV8000 Futura Prestige z ekranem dotykowym 15,6 cala, widok z boku'),
       ('pf-g2', 451, 570, 'Konsola i ekran bieżni APV8000 Futura Prestige, widok z przodu'),
       ('pf-g3', 769, 659, 'Składanie bieżni APV8000 z siłownikiem gazowym'),
       ('pf-g4', 699, 715, 'Złożona bieżnia APV8000 Futura Prestige'),
       ('pf-g5', 701, 622, 'Bieżnia APV8000 z zestawem dodatków: masażer, hantle, rama do brzuszków'),
       ('pf-g6', 850, 594, 'Tył pasa biegowego bieżni APV8000'),
       ('pf-pokretlo', 680, 506, 'Pokrętło sterujące z wyświetlaczem LED w bieżni APV8000')]

def src(n, w):
    return f'../img/{n}-{w}.webp'
def srcset(n, w):
    return f'{src(n, 480)} 480w, {src(n, w)} {w}w' if w > 480 else f'{src(n, w)} {w}w'

g0 = GAL[0]
galeria = (f'<div class="gl" data-grupa><button class="duze" type="button" data-lb="{src(g0[0], g0[1])}" aria-label="Powiększ zdjęcie">'
           f'<img id="duze" src="{src(g0[0], g0[1])}" srcset="{srcset(g0[0], g0[1])}" sizes="(max-width:900px) 92vw, 52vw" width="{g0[1]}" height="{g0[2]}" fetchpriority="high" alt="{E(g0[3])}"></button>'
           '<div class="mini">' + ''.join(
               f'<button type="button" data-duze="{src(n, w)}" data-alt="{E(a)}"{" aria-current=\"true\"" if i == 0 else ""} aria-label="Zdjęcie {i + 1} z {len(GAL)}"><img src="{src(n, 480 if w > 480 else w)}" width="120" height="120" loading="lazy" decoding="async" alt=""></button>'
               for i, (n, w, h, a) in enumerate(GAL)) + '</div></div>')

CECHY = [
    ('pf-ekran', 990, 590, 'Ekran', 'Dotykowy ekran Android 15,6 cala, menu po polsku',
     'Duży, kolorowy ekran TFT obsługuje się jak tablet. Po połączeniu z internetem włączysz film albo stronę internetową, a w trybie wirtualnych tras pobiegniesz po górach, lesie czy ulicach miasta. Bieżnia współpracuje z aplikacjami Kinomap, Zwift i FitShow oraz łączy się ze smartfonem i tabletem.',
     'Ekran dotykowy Android 15,6 cala w bieżni APV8000 z wirtualną trasą'),
    ('pf-bieg', 990, 590, 'Silnik i rama', 'Silnik 6 KM, rama do 180 kg',
     'Silnik AC o mocy stałej 6 KM (10 KM mocy szczytowej) rozpędza pas od 1 do 25 km/h i pracuje cicho dzięki technologii Silent Motion. Stabilna rama przenosi obciążenie do 180 kg, więc z bieżni wygodnie skorzysta cała rodzina.',
     'Trening marszowy na pasie biegowym bieżni APV8000'),
    ('pf-pokretlo', 680, 506, 'Sterowanie', 'Pokrętło z wyświetlaczem LED i przyciski w rączkach',
     'Prędkość zmienisz pokrętłem na konsoli albo przyciskami w rączkach, bez odrywania rąk od uchwytów. Nachylenie pasa ustawia się elektronicznie. Na konsoli są gniazdo audio i port USB, a obok miejsce na telefon i bidon.',
     'Pokrętło sterujące z wyświetlaczem LED na konsoli bieżni APV8000'),
    ('pf-salon', 990, 590, 'Pas biegowy', 'Długi pas 145 x 58 cm z amortyzacją',
     'Pas o wymiarach 145 x 58 cm daje swobodę także przy szybkim biegu. Zaawansowany system amortyzacji zmniejsza obciążenie kości i stawów, a system kompensacji nierówności stabilizuje bieżnię na podłodze.',
     'Bieżnia APV8000 Futura Prestige w sali, długi pas biegowy'),
    ('pf-g3', 769, 659, 'Składanie', 'Składa się jednym ruchem, przejedzie na kółkach',
     'Teleskopowy system składania z siłownikiem gazowym podnosi pas bez wysiłku. Złożoną bieżnię przesuniesz na kółkach transportowych pod ścianę albo do innego pokoju.',
     'Składanie bieżni APV8000 z siłownikiem gazowym'),
    ('pf-dodatki', 1093, 410, 'W cenie', 'Zestaw dodatków do bieżni',
     'Do bieżni dołączamy wyposażenie o wartości katalogowej 800 zł: masażer, twister, 2 hantle, ramę do brzuszków z gąbkami, wygłuszającą matę pod bieżnię chroniącą podłogę oraz olej silikonowy do konserwacji pasa.',
     'Zestaw dodatków do bieżni APV8000: masażer, twister, hantle, rama do brzuszków, mata'),
]
cechy = ''.join(
    f'<div class="cech"><figure class="cf"><img src="{src(n, 480)}" srcset="{srcset(n, w)}" sizes="(max-width:900px) 92vw, 46vw" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{E(alt)}"></figure>'
    f'<div><small>{E(m)}</small><h3>{E(t)}</h3><p>{E(p)}</p></div></div>'
    for n, w, h, m, t, p, alt in CECHY)

PARAM = [('Model / seria', 'APV8000 / Futura Prestige'), ('Moc silnika', '6 KM AC (moc stała), 10 KM (moc szczytowa)'),
         ('Prędkość', '1-25 km/h'), ('Maksymalne obciążenie', '180 kg'), ('Wymiary pasa biegowego', '145 x 58 cm'),
         ('Ekran', 'dotykowy TFT 15,6 cala, Android, menu w języku polskim, dostęp do internetu'),
         ('Regulacja nachylenia', 'elektroniczna'), ('Amortyzacja', 'tak, system amortyzacji pasa'),
         ('System kompensacji nierówności', 'tak'), ('Pomiar pulsu', 'sensory dotykowe w rączkach'),
         ('Zmiana prędkości', 'w rączkach lub z panelu głównego'), ('Program ręczny', 'tak'),
         ('Wejście audio i USB', 'tak'), ('Aplikacje', 'Kinomap, Zwift, FitShow'),
         ('Hamulec bezpieczeństwa', 'tak'), ('Koła transportowe', 'tak'), ('Składana konstrukcja', 'tak, siłownik gazowy'),
         ('Miejsce na butelkę', 'tak'), ('Zasilanie', '220-230 V'), ('Kategoria', 'SB (zgodnie z EN 957)'),
         ('Wymiary urządzenia', '204 x 92,5 x 138 cm'), ('Wymiary opakowania', '207 x 97 x 44 cm'),
         ('Waga bieżni / w opakowaniu', '114 kg / 130 kg'), ('Certyfikaty', 'CE, RoHS'), ('EAN', '9331582499908'),
         ('Czas realizacji', '30 dni')]
tabela = '<table class="par"><caption>Parametry techniczne</caption><tbody>' + ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in PARAM) + '</tbody></table>'

FILMY = [('r46a4RoqEwY', 'Prezentacja serii Futura Prestige'), ('Z4sfFoUTpzg', 'Funkcje ekranu dotykowego 15,6 cala, wersja polska'),
         ('ZPg6jSN-DGE', 'Wirtualne trasy na ekranie bieżni'), ('3zskB507N9g', 'Jak połączyć bieżnię z aplikacją Kinomap'),
         ('J7oqwrpF1ac', 'Jak połączyć bieżnię z aplikacją Zwift')]
filmy = ''.join(f'<figure class="film"><button class="fa" type="button" data-yt="{i}" aria-label="Odtwórz film: {E(t)}"><img src="../img/yt-{i}.webp" width="480" height="270" loading="lazy" decoding="async" alt=""><span class="od" aria-hidden="true"></span></button><figcaption>{E(t)}</figcaption></figure>' for i, t in FILMY)

podobne = '\n'.join(x for x in BIEZNIE if 'APV8000 Futura Prestige 6 KM' not in x)

ld = json.dumps({'@context': 'https://schema.org', '@graph': [
    {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'TREG', 'item': BAZA},
        {'@type': 'ListItem', 'position': 2, 'name': 'Bieżnie elektryczne', 'item': BAZA + 'bieznie-elektryczne/'},
        {'@type': 'ListItem', 'position': 3, 'name': NAZWA, 'item': URL}]},
    {'@type': 'Product', 'name': NAZWA, 'sku': 'APV8000-FP-6KM', 'gtin13': '9331582499908',
     'brand': {'@type': 'Brand', 'name': 'APVsport'},
     'image': [BAZA + 'img/pf-g1-950.webp', BAZA + 'img/pf-g3-769.webp'],
     'description': 'Bieżnia elektryczna z silnikiem 6 KM (10 KM szczytowo), pasem 145 x 58 cm, dotykowym ekranem Android 15,6 cala i obciążeniem do 180 kg.',
     'offers': {'@type': 'Offer', 'url': URL, 'priceCurrency': 'PLN', 'price': '4990.00',
                'availability': 'https://schema.org/BackOrder', 'itemCondition': 'https://schema.org/NewCondition',
                'seller': {'@type': 'Organization', 'name': 'TREG Łukasz Pawluczuk'}}}]},
    ensure_ascii=False).replace('</', '<\\/')

strona = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Bieżnia APV8000 Futura Prestige 6 KM, ekran 15,6" | TREG</title>
<meta name="description" content="Bieżnia elektryczna APV8000 Futura Prestige: silnik 6 KM, pas 145 x 58 cm, ekran dotykowy Android 15,6 cala, do 180 kg. 4 990 zł, raty 0%, PayPo, BLIK.">
<link rel="canonical" href="{URL}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="../fonts/archivo-rdzen.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../fonts/archivo-pl.woff2" crossorigin>
{STYL_P}
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
{NAGL}

<main id="tresc">
<section class="kp" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / <a href="../bieznie-elektryczne/">Bieżnie elektryczne</a> / APV8000 Futura Prestige 6 KM</nav>
    <div class="kp-g">
      {galeria}
      <div class="zak" id="zakup">
        <span class="marka"><span class="kw apv"></span>APVsport</span>
        <h1 id="h1">{E(NAZWA)}</h1>
        <a class="ocz" href="#opinie">Opinie kupujących z Opinii Zaufanych Ceneo</a>
        <p class="cena"><b>4 990 zł</b><s>7 290 zł</s><span class="oszcz">taniej o 2 300 zł</span></p>
        <p class="dost zam"><span class="b" aria-hidden="true"></span>Na zamówienie, realizacja 30 dni</p>
        <ul class="kl">
          <li>Silnik 6 KM, 10 KM mocy szczytowej</li>
          <li>Dotykowy ekran Android 15,6 cala, menu po polsku</li>
          <li>Pas biegowy 145 x 58 cm z amortyzacją</li>
          <li>Prędkość 1-25 km/h, obciążenie do 180 kg</li>
          <li>Elektroniczna regulacja nachylenia</li>
          <li>Aplikacje Kinomap, Zwift i FitShow</li>
        </ul>
        <label class="opc"><input type="checkbox" id="pas"><span><b>Dodaj pas piersiowy do pomiaru tętna: 125 zł</b> <s>139 zł</s><small>Tętno wyświetla się na ekranie bieżni.</small></span></label>
        <div class="kup">
          <div class="ilosc"><button type="button" data-il="-1" aria-label="Mniej">-</button><input id="il" type="number" min="1" value="1" aria-label="Ilość"><button type="button" data-il="1" aria-label="Więcej">+</button></div>
          <button type="button" class="dok" data-kosz data-id="20185" data-nazwa="{E(NAZWA)}" data-cena="4990" data-url="./" data-img="../img/pf-g1-480.webp">Dodaj do koszyka</button>
        </div>
        <div class="zauf">
          <span><span class="kw apv"></span>Raty 0%</span><span><span class="kw aq"></span>PayPo: zapłać za 30 dni</span>
          <span><span class="kw apv"></span>BLIK i przelew</span><span><span class="kw aq"></span>Gwarancja najniższej ceny</span>
          <span><span class="kw apv"></span>Serwis w całym kraju</span><span><span class="kw aq"></span>Wysyłka ubezpieczona</span>
        </div>
        <p class="zest">W cenie zestaw dodatków o wartości 800 zł: masażer, twister, 2 hantle, rama do brzuszków, mata i olej silikonowy.</p>
      </div>
    </div>
  </div>
</section>

<nav class="zakl" aria-label="Sekcje produktu"><div class="wrap"><a href="#opis">Opis</a><a href="#parametry">Parametry</a><a href="#filmy">Filmy</a><a href="#dostawa">Dostawa i płatności</a><a href="#opinie">Opinie</a><a href="#podobne">Podobne</a></div></nav>

<section class="sek" id="opis" aria-labelledby="h-opis">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-opis"><span class="kw apv"></span>Profesjonalna bieżnia do domu</h2><p class="lead">APV8000 ma to, co znajdziesz w dobrej siłowni: długi i szeroki pas, mocny silnik i rozbudowany ekran. Najważniejsze cechy w skrócie:</p></div></div>
    {cechy}
  </div>
</section>

<section class="sek szary" id="parametry" aria-labelledby="h-par">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-par">Parametry</h2></div></div>
    {tabela}
  </div>
</section>

<section class="sek" id="filmy" aria-labelledby="h-fil">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-fil">Filmy</h2><p class="lead">Odtwarzacz YouTube włącza się dopiero po kliknięciu.</p></div></div>
    <div class="fl2">{filmy}</div>
  </div>
</section>

<section class="sek szary" id="dostawa" aria-labelledby="h-dostawa">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-dostawa">Dostawa, płatności i zwroty</h2></div></div>
    <div class="info4">
      <div><h3><span class="kw aq"></span>Dostawa</h3><ul><li>Kurierem, także przesyłki nadwymiarowe i bardzo ciężkie</li><li>Każda bieżnia solidnie zapakowana i ubezpieczona</li><li>Koszt dostawy doliczany według cennika z dnia zakupu</li></ul></div>
      <div><h3><span class="kw apv"></span>Płatności</h3><ul><li>Raty 0%</li><li>PayPo: zapłata po 30 dniach</li><li>BLIK i przelew</li><li>Gotówką przy odbiorze</li></ul></div>
      <div><h3><span class="kw aq"></span>Gwarancja i serwis</h3><ul><li>Dokument gwarancyjny i instrukcja w komplecie</li><li>Serwis gwarancyjny i pogwarancyjny w całym kraju</li><li>Własny magazyn części zamiennych</li></ul></div>
      <div><h3><span class="kw apv"></span>Zwroty</h3><ul><li>14 dni na odstąpienie od umowy</li><li>Zwrot pieniędzy w ciągu 7 dni roboczych</li><li>Przesyłkę sprawdza się przy kurierze</li></ul></div>
    </div>
  </div>
</section>

<section class="sek opinie" id="opinie" aria-labelledby="h-opinie">
  <div class="wrap">
    <div>
      <h2 id="h-opinie">Opinie kupujących</h2>
      <p>Opinie zbieramy w programie Opinie Zaufane Ceneo: po każdym zamówieniu kupujący dostaje krótką ankietę. Po uruchomieniu sklepu opinie o tej bieżni pokażą się w tym miejscu.</p>
      <a class="btn wa" href="{WA}" target="_blank" rel="noopener">Zapytaj o bieżnię na WhatsAppie</a>
    </div>
    <div class="miejsce"><b>Opinie Zaufane Ceneo</b><span>Miejsce na opinie i ocenę sklepu treg.pl.</span></div>
  </div>
</section>

<section class="sek szary" id="podobne" data-k="apv" aria-labelledby="h-pod">
  <div class="wrap">
    <div class="sg">
      <div><h2 id="h-pod"><span class="kw apv"></span>Podobne bieżnie</h2></div>
      <div class="nav" data-nav="tp"><button type="button" data-k="-1" aria-label="Poprzednie bieżnie"></button><button type="button" data-k="1" aria-label="Następne bieżnie"></button></div>
    </div>
    <div class="tor" id="tp" data-tor>
{podobne}
    </div>
  </div>
</section>
</main>

<div class="pas" id="pasek" aria-hidden="true"><div class="wrap"><span class="n">{E(NAZWA)}</span><b>4 990 zł</b><a class="dok" href="#zakup" tabindex="-1">Kup teraz</a></div></div>
{STOPKA}
{LB}
<script>
(function(){{var d=document,du=d.getElementById('duze'),bd=du.parentNode;
d.querySelectorAll('.mini button').forEach(function(b){{b.addEventListener('click',function(){{du.removeAttribute('srcset');du.src=b.dataset.duze;du.alt=b.dataset.alt;bd.dataset.lb=b.dataset.duze;d.querySelectorAll('.mini button').forEach(function(x){{x.setAttribute('aria-current',x===b)}})}})}});
var il=d.getElementById('il');d.querySelectorAll('[data-il]').forEach(function(b){{b.addEventListener('click',function(){{il.value=Math.max(1,(+il.value||1)+(+b.dataset.il))}})}});
var p=d.getElementById('pasek'),z=d.getElementById('zakup');
if('IntersectionObserver' in window)new IntersectionObserver(function(e){{var on=!e[0].isIntersecting&&e[0].boundingClientRect.top<0;p.classList.toggle('on',on);p.setAttribute('aria-hidden',!on)}}).observe(z);
var zl=[].slice.call(d.querySelectorAll('.zakl a'));
if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting)zl.forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)}})}})}},{{rootMargin:'-45% 0px -50% 0px'}});
['opis','parametry','filmy','dostawa','opinie','podobne'].forEach(function(id){{var s=d.getElementById(id);if(s)io.observe(s)}})}}
}})();
</script>
<script src="../app.js" defer></script>
<script src="../koszyk.js" defer></script>
<script src="../wa.js" data-firma="TREG" data-kolor="#1e2124" defer></script>
</body>
</html>
'''
os.makedirs(SLUG, exist_ok=True)
open(f'{SLUG}/index.html', 'w', encoding='utf-8').write(strona)
sm = open('sitemap.xml', encoding='utf-8').read()
if SLUG not in sm:
    sm = sm.replace('</urlset>', f'<url><loc>{URL}</loc></url>\n</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('produkt ok', len(strona))
