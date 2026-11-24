# Sklep treg.pl: karty wszystkich produktow, kategorie, koszyk, dostawa, regulamin, polityka prywatnosci, kontakt, o firmie.
# Dane: produkty.json (dane_sklepu.py, aquaholm.pl Store API 24.11.2026), tresci regulaminu i polityki z treg.pl (strony WP 648, 655).
# Kolejnosc: build.py -> miasta.py -> produkt.py -> sklep.py (sklep.py importuje produkt, wiec wystarczy build.py + sklep.py).
import json, os, re, html as H
import produkt
from miasta import NAGL, STOPKA, LB, BAZA, WA, idx, wytnij, popraw_linki
STYL_P = produkt.STYL_P
E = H.escape
P = json.load(open('produkty.json', encoding='utf-8'))
PID = {p['id']: p for p in P}

def zl(n): return f'{n:,}'.replace(',', ' ') + ' zł'

STYL_S = STYL_P.replace('</style>', '''
.kat{padding:clamp(28px,4vw,64px) 0 clamp(22px,3vw,40px);background:var(--g)}
.kat h1{font-size:clamp(34px,3.4vw,64px);font-stretch:92%;max-width:24ch}
.cech .cf{max-width:760px;width:100%}.cech:nth-of-type(even) .cf{justify-self:end}
.cech .cf img{aspect-ratio:4/3;object-fit:cover;width:100%;height:auto}
.kat+.sek{padding-top:clamp(24px,2.6vw,44px)}
.kat .lead{max-width:76ch;font-size:clamp(18px,1.2vw,21px);margin-top:16px}
.filtry{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px;align-items:center}
.filtry button{min-height:46px;padding:0 18px;border:2px solid var(--ink);background:#fff;font:700 1rem Archivo,Arial,sans-serif;cursor:pointer;border-radius:2px}
.filtry button[aria-pressed="true"]{background:var(--ink);color:#fff}
.filtry label{margin-left:auto;display:flex;align-items:center;gap:10px;font-weight:600}
.filtry select{min-height:46px;padding:0 12px;border:2px solid var(--line);background:#fff;font:600 1rem Archivo,Arial,sans-serif}
.ile{margin:18px 0 0;color:var(--mut)}
.siat{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,290px),1fr));gap:clamp(16px,1.6vw,28px)}
.kt{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line)}
.kt .f{display:block;aspect-ratio:4/3;background:#fff;border-bottom:1px solid var(--line)}
.kt .f img{width:100%;height:100%;object-fit:contain}
.kt .in{display:flex;flex-direction:column;flex:1;padding:16px 18px 18px}
.kt h2,.kt h3{font-size:1.12rem;line-height:1.3;font-weight:700;font-stretch:100%;letter-spacing:0;display:flex;gap:10px;align-items:baseline}.kt h2 .kw,.kt h3 .kw{flex:none}.kt h2 a,.kt h3 a{text-decoration:none;color:var(--ink);min-width:0}.kt h2 a:hover,.kt h3 a:hover{text-decoration:underline}
.kt .po{margin-top:8px;color:var(--mut);font-size:.95rem;line-height:1.45}
.kt .dost{margin-top:10px}
.kt .cena{margin-top:auto;padding-top:12px}
.kt .dok{margin-top:10px}
.szary .kt{border-color:#dfe4e9}
.kt[hidden]{display:none}
.gl .duze{aspect-ratio:auto;min-height:clamp(260px,34vw,620px);display:flex;align-items:center;justify-content:center}
.gl .duze img{width:auto;max-width:100%;height:auto;max-height:min(70vh,760px);object-fit:contain}
.mini{grid-template-columns:repeat(8,minmax(0,1fr))}
.lst{columns:2;column-gap:clamp(24px,3vw,60px);margin:18px 0 0;padding-left:0;list-style:none;max-width:1200px}
.lst li{break-inside:avoid;position:relative;padding:0 0 10px 26px;line-height:1.45}
.lst li::before{content:"";position:absolute;left:2px;top:.42em;width:9px;height:9px;background:var(--aq)}
.bz .lst li::before{background:var(--apv)}
.lst-h{font-size:clamp(20px,1.4vw,26px);margin-top:clamp(30px,3vw,50px)}
.mat{max-width:80ch;margin-top:14px;color:var(--mut)}
.dok.pyt{background:var(--ink)}
.wa-k{margin-top:12px;display:inline-flex}
.tekst{padding:clamp(30px,4vw,64px) 0 clamp(50px,6vw,90px)}
.tekst .wrap{max-width:980px}
.tekst h1{font-size:clamp(32px,3vw,54px);font-stretch:92%}
.tekst h2{font-size:clamp(22px,1.6vw,30px);margin-top:36px}
.tekst h3{font-size:1.15rem;margin-top:24px}
.tekst p,.tekst li{line-height:1.6;max-width:80ch}.tekst p{margin-top:12px}
.tekst ul,.tekst ol{margin:12px 0 0 22px}.tekst li{margin-top:6px}
.tekst .okr{margin-bottom:18px}
.kosz-s{padding:clamp(28px,4vw,60px) 0 clamp(50px,6vw,90px)}
.kosz-s h1{font-size:clamp(32px,3vw,54px);font-stretch:92%}
.kg{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:clamp(24px,4vw,70px);align-items:start;margin-top:26px}
#lista{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.poz{display:grid;grid-template-columns:120px minmax(0,1fr) auto auto auto;gap:16px;align-items:center;padding:16px 0;border-bottom:1px solid var(--line)}
.poz img{width:120px;height:96px;object-fit:contain;background:#fff}
.poz .nz{font-weight:700;color:var(--ink);text-decoration:none}.poz .nz:hover{text-decoration:underline}
.poz .cj{display:block;color:var(--mut);font-size:.93rem;margin-top:4px}
.poz .ilosc{display:flex;border:2px solid var(--ink)}.poz .ilosc button{width:40px;border:0;background:#fff;font-size:1.2rem;cursor:pointer}
.poz .ilosc input{width:44px;border:0;text-align:center;font:700 1rem Archivo,Arial,sans-serif;-moz-appearance:textfield}
.poz .wr{white-space:nowrap;font-size:1.1rem}
.poz .us{border:0;background:none;color:var(--mut);text-decoration:underline;cursor:pointer;font:600 .95rem Archivo,Arial,sans-serif;min-height:44px}
.razem{display:flex;justify-content:space-between;align-items:baseline;margin-top:18px;font-size:1.2rem}.razem b{font-size:1.7rem}
.uw{color:var(--mut);margin-top:8px}
.pusty{padding:28px;background:var(--g);margin-top:10px}
.pusty .akc{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px}
.zamf{background:var(--g);padding:clamp(20px,2.4vw,34px)}
.zamf h2{font-size:1.5rem}
.zamf fieldset{border:0;padding:0;margin:18px 0 0}
.zamf legend{font-weight:800;margin-bottom:8px}
.zamf label{display:block;font-weight:600;margin-top:10px}
.zamf input[type=text],.zamf input[type=email],.zamf input[type=tel]{display:block;width:100%;min-height:50px;margin-top:6px;padding:0 12px;border:2px solid var(--line);background:#fff;font:1rem Archivo,Arial,sans-serif}
.zamf .r2{display:grid;grid-template-columns:1fr 1fr;gap:0 14px}
.zamf .op{display:flex;gap:12px;align-items:flex-start;background:#fff;padding:12px 14px;margin-top:8px;font-weight:600;cursor:pointer}
.zamf .op input{width:20px;height:20px;margin:2px 0 0;flex:none;accent-color:var(--ink)}
.zamf .op small{display:block;font-weight:400;color:var(--mut)}
.zamf .zg{display:flex;gap:10px;font-weight:400;align-items:flex-start}.zamf .zg input{width:20px;height:20px;flex:none;margin-top:2px}
.zamf .btn{margin-top:18px;width:100%;justify-content:center}
.komunikat{margin-top:14px;padding:14px;background:#fff;border-left:4px solid var(--aq)}
@media (max-width:1000px){.kg{grid-template-columns:minmax(0,1fr)}}
@media (max-width:700px){.lst{columns:1}.filtry label{margin-left:0;width:100%}.filtry select{flex:1}
.poz{grid-template-columns:84px minmax(0,1fr) auto;grid-template-areas:"f o o" "f i w" ". u u";gap:8px 12px}.poz .fz{grid-area:f}.poz img{width:84px;height:68px}.poz .op{grid-area:o}.poz .ilosc{grid-area:i;justify-self:start}.poz .wr{grid-area:w;justify-self:end}.poz .us{grid-area:u;justify-self:start;min-height:36px}
.zamf .r2{grid-template-columns:1fr}}
</style>''')

def podstrona(tytul, opis, sciezka, tresc, ld=None, skrypty=''):
    url = BAZA + sciezka
    ldtag = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>' if ld else ''
    return f'''<!doctype html>
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
{STYL_S}
{ldtag}
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
{NAGL}
<main id="tresc">
{tresc}
</main>
{STOPKA}
{LB}
{skrypty}
<script src="../app.js" defer></script>
<script src="../koszyk.js" defer></script>
<script src="../wa.js" data-firma="TREG" data-kolor="#1e2124" defer></script>
</body>
</html>
'''

def zapisz(sciezka, s):
    os.makedirs(sciezka, exist_ok=True)
    open(f'{sciezka}/index.html', 'w', encoding='utf-8').write(s)
    STRONY.append(sciezka + '/')
STRONY = []

DOST = {'jest': ('jest', 'Dostępna od ręki'), 'zam': ('zam', 'Na zamówienie, realizacja 30 dni'), 'brak': ('brak', 'Chwilowo brak, zapytaj o termin')}
SCH = {'jest': 'InStock', 'zam': 'BackOrder', 'brak': 'OutOfStock'}
def kier(p): return 'aq' if p['typ'] == 'wanna' else 'apv'
def img(p, i, w): z = p['zdjecia'][i]; return '../img/p/' + (z['d'][0] if w == 'd' else z['m'][0])
def tech(p, klucz):
    for k, v in p.get('tech', []):
        if k.lower().startswith(klucz.lower()): return v
    return None
def ladnie(v):
    v = re.sub(r'(\d)(kg|KM|W|cm|l)\b', r'\1 \2', v)
    return v.replace(' – ', '-').replace('–', '-').replace('″', '"').replace('"', ' cala')

def opis_krotki(p):
    if p['typ'] == 'wanna':
        x = [f'{p["wym"][0]} x {p["wym"][1]} x {p["wym"][2]} cm']
        if p['dysze_pow'] and p['dysze_wod']: x.append(f'{int(p["dysze_pow"]) + int(p["dysze_wod"])} dysz')
        if p['grzalka']: x.append(f'podgrzewacz {p["grzalka"]} W')
        x += [n for k, n in (('wodospad', 'wodospad'), ('bluetooth', 'Bluetooth'), ('pilot', 'pilot')) if p['cechy_n'].get(k)]
        return ', '.join(x)
    if p['typ'] == 'bieznia':
        x = []
        m = tech(p, 'Moc silnika')
        if m: x.append('silnik ' + ladnie(m.split('(')[0]).strip())
        if p['pas']: x.append('pas ' + p['pas'].replace('x', ' x ') + ' cm')
        x.append(f'ekran Android {p["ekran"].replace(".", ",")} cala' if p['ekran'] else 'ekran LCD')
        o = tech(p, 'Maksymalne obciążenie')
        if o: x.append('do ' + ladnie(o))
        return ', '.join(x)
    return (p.get('wyroznienia') or [''])[0]

def karta(p, nag='h3'):
    k = kier(p); d = DOST[p['dost']]
    st = f'<s>{zl(p["stara"])}</s>' if p['stara'] else ''
    z = p['zdjecia'][0]
    if p['dost'] != 'brak':
        kup = (f'<button type="button" class="dok" data-kosz data-id="{p["id"]}" data-nazwa="{E(p["nazwa"])}" data-cena="{p["cena"]}" '
               f'data-url="../{p["slug"]}/" data-img="../img/p/{z["m"][0]}">Dodaj do koszyka</button>')
    else:
        kup = f'<a class="dok pyt" href="../{p["slug"]}/">Zobacz i zapytaj o termin</a>'
    atr = f'data-typ="{p["typ"]}" data-cena="{p["cena"]}" data-dost="{p["dost"]}"'
    if p['typ'] == 'wanna': atr += f' data-ksztalt="{p["ksztalt"]}" data-kolor="{p["kolor"]}"'
    if p['typ'] == 'bieznia': atr += f' data-model="{"apv8000" if p["model"] == "APV8000" else "inne"}"'
    return (f'<article class="kt" {atr}><a class="f" href="../{p["slug"]}/" tabindex="-1" aria-hidden="true">'
            f'<img src="../img/p/{z["m"][0]}" srcset="../img/p/{z["m"][0]} {z["m"][1]}w, ../img/p/{z["d"][0]} {z["d"][1]}w" sizes="(max-width:640px) 92vw, (max-width:1100px) 45vw, 22vw" width="{z["m"][1]}" height="{z["m"][2]}" loading="lazy" decoding="async" alt="{E(p["nazwa"])}"></a>'
            f'<div class="in"><{nag}><span class="kw {k}"></span><a href="../{p["slug"]}/">{E(p["nazwa"])}</a></{nag}><p class="po">{E(opis_krotki(p))}</p>'
            f'<p class="dost {d[0]}"><span class="b" aria-hidden="true"></span>{d[1]}</p><p class="cena"><b>{zl(p["cena"])}</b>{st}</p>{kup}</div></article>')

FILMY_W = {'A9009': [('UxqKd6TiJ00', 'Wanna A9009, biała: hydromasaż i podświetlenie LED')], 'A9009C': [('Kwkem9694PE', 'Wanna A9009C, czarna: hydromasaż i podświetlenie LED')],
           'A9008C': [('IQyb91JjEAs', 'Wanna A9008C, czarna: prezentacja')], 'A9014': [('c0Il79_bJFk', 'Wanna A9014: prezentacja')]}
FILMY_F = [('r46a4RoqEwY', 'Prezentacja serii Futura Prestige'), ('Z4sfFoUTpzg', 'Funkcje ekranu dotykowego 15,6 cala, wersja polska'),
           ('ZPg6jSN-DGE', 'Wirtualne trasy na ekranie bieżni'), ('3zskB507N9g', 'Jak połączyć bieżnię z aplikacją Kinomap'), ('J7oqwrpF1ac', 'Jak połączyć bieżnię z aplikacją Zwift')]
# filmy od klienta (WhatsApp 24.11), pelne, z dzwiekiem, natywna rozdzielczosc: klienci/Treg/montaz2.py
FILMY_N = {'A9001C': (960, 544), 'A9009': (960, 544), 'A9001': (960, 544), 'A9006': (1024, 576), 'A9007C': (1024, 576), 'A9004C': (1024, 576), 'A9014': (1024, 576)}
def film_nat(p):
    if p['typ'] != 'wanna' or p['kod'] not in FILMY_N: return ''
    w, h = FILMY_N[p['kod']]; n = 'wanna-' + p['kod'].lower()
    return (f'<figure class="film nat" style="grid-column:1/-1;max-width:{w}px;margin:0"><video controls playsinline preload="none" poster="../film/{n}.webp" width="{w}" height="{h}" '
            f'style="display:block;width:100%;height:auto;aspect-ratio:{w}/{h};border-radius:6px;background:#0b0e11" aria-label="Film: wanna {E(p["kod"])} w działaniu">'
            f'<source src="../film/{n}.mp4" type="video/mp4"></video><figcaption>Wanna {E(p["kod"])} w działaniu: hydromasaż, podświetlenie LED i panel sterowania (film z dźwiękiem)</figcaption></figure>')
def filmy_dla(p):
    if p['typ'] == 'wanna': return FILMY_W.get(p['kod'], [])
    if p['typ'] == 'bieznia' and p.get('seria') == 'Futura Prestige':
        return [f for f in FILMY_F if p['ekran'] == '15.6' or f[0] in ('r46a4RoqEwY', '3zskB507N9g', 'J7oqwrpF1ac')]
    return []

def blok(p, i, mala, tytul, tekst):
    i = min(i, len(p['zdjecia']) - 1); z = p['zdjecia'][i]
    return (f'<div class="cech"><figure class="cf"><img src="../img/p/{z["m"][0]}" srcset="../img/p/{z["m"][0]} {z["m"][1]}w, ../img/p/{z["d"][0]} {z["d"][1]}w" sizes="(max-width:900px) 92vw, 46vw" '
            f'width="{z["d"][1]}" height="{z["d"][2]}" style="max-width:{z["d"][1]}px" loading="lazy" decoding="async" alt="{E(p["krotka"])}, zdjęcie {i + 1}"></figure>'
            f'<div><small>{E(mala)}</small><h3>{E(tytul)}</h3><p>{E(tekst)}</p></div></div>')

def tresc_wanny(p):
    c = p['cechy_n']; f = ' '.join(p['funkcje'] + p['akcesoria']).lower()
    L, W, Hh = p['wym']
    ks = {'narozna': 'Narożny kształt dobrze wykorzystuje miejsce w rogu łazienki.',
          'podwojna': 'To szeroka, podwójna wanna, wygodna do wspólnej kąpieli.',
          'prostokatna': 'Prostokątną wannę łatwo ustawić przy ścianie, w rogu albo na środku ściany.'}[p['ksztalt']]
    kol = ('Czarny akryl z kolorowym podświetleniem wygląda efektownie zwłaszcza wieczorem.' if p['kolor'] == 'czarna'
           else 'Biały akryl na wysoki połysk pasuje do jasnych i ciemnych łazienek.')
    lead = f'Wanna {p["kod"]} z serii Premium Line ma wymiary {L} x {W} x {Hh} cm' + (f' i mieści ok. {p["pojemnosc"]} l wody' if p['pojemnosc'] else '') + f'. {ks} {kol}'
    bl = []
    if p['dysze_pow'] and p['dysze_wod']:
        t = 'Masaż powietrzny w dnie wanny' + (f' napędza pompa {p["pompa_pow"]} W' if p['pompa_pow'] else '') + ', a hydromasaż wodny w ścianach' + (f' pompa {p["pompa_wod"]} W.' if p['pompa_wod'] else ' mocna pompa wodna.')
        if p['dysze_plecy']: t += f' Plecy masuje po {p["dysze_plecy"]} obrotowych dysz na każde stanowisko.'
        if 'regulator siły' in f: t += ' Siłę masażu wodnego ustawisz regulatorem.'
        bl.append(('Hydromasaż', f'{p["dysze_pow"]} dysz powietrznych i {p["dysze_wod"]} dysz wodnych', t))
    if p['grzalka']:
        t = 'Podgrzewacz utrzymuje temperaturę wody, więc długa kąpiel z hydromasażem nie stygnie.'
        if 'czujniki' in f: t += ' Czujniki chronią pompy, gdy w wannie jest za mało wody.'
        bl.append(('Ciepła woda', f'Podgrzewacz wody {p["grzalka"]} W', t))
    if c.get('led rgb'):
        t = 'Kolorowe podświetlenie wanny i dysz dopasujesz do nastroju.'
        if 'słuchawka' in f: t += ' Słuchawka prysznicowa LED zmienia kolor zależnie od temperatury wody i nie potrzebuje baterii.'
        bl.append(('Światło', 'Oświetlenie LED RGB' + (' w siedmiu kolorach' if 'siedem kolorów' in f else ''), t))
    funk = [n for k, n in (('radio', 'radio FM'), ('bluetooth', 'muzykę przez Bluetooth')) if c.get(k)]
    t = 'Z podświetlanego panelu włączysz masaż, oświetlenie' + (', ' + ' i '.join(funk) if funk else '') + '.'
    if c.get('usb'): t += ' Wanna ma też port USB.'
    if c.get('ozon') and c.get('samoosusz'): t += ' Dezynfekcja ozonowa i samoosuszanie dysz pomagają utrzymać wannę w czystości.'
    bl.append(('Sterowanie', 'Panel dotykowy' + (' i pilot w zestawie' if c.get('pilot') else ''), t))
    bloki = ''.join(blok(p, i + 1, *b) for i, b in enumerate(bl))
    lst = ''
    if p['funkcje']: lst += '<h3 class="lst-h">Wyposażenie i funkcje</h3><ul class="lst">' + ''.join(f'<li>{E(x)}</li>' for x in p['funkcje']) + '</ul>'
    if p['akcesoria']: lst += '<h3 class="lst-h">W zestawie</h3><ul class="lst">' + ''.join(f'<li>{E(x)}</li>' for x in p['akcesoria']) + '</ul>'
    if p['material']: lst += f'<h3 class="lst-h">Materiał</h3><p class="mat">{E(p["material"])}</p>'
    par = [('Kod produktu', p['kod']), ('Producent / seria', 'Aquaholm / Premium Line'),
           ('Kształt', {'narozna': 'narożna', 'podwojna': 'prostokątna, podwójna', 'prostokatna': 'prostokątna'}[p['ksztalt']]),
           ('Kolor', 'czarny' if p['kolor'] == 'czarna' else 'biały'), ('Wymiary (dł. x szer. x wys.)', f'{L} x {W} x {Hh} cm')]
    if p['pojemnosc']: par.append(('Pojemność', f'ok. {p["pojemnosc"]} l'))
    if p['dysze_pow']: par.append(('Dysze powietrzne', p['dysze_pow'] + ' szt.'))
    if p['dysze_wod']: par.append(('Dysze wodne', p['dysze_wod'] + ' szt.'))
    if p['dysze_plecy']: par.append(('Dysze do masażu pleców', f'po {p["dysze_plecy"]} szt. na stanowisko'))
    if p['pompa_pow']: par.append(('Pompa powietrzna', p['pompa_pow'] + ' W'))
    if p['pompa_wod']: par.append(('Pompa wodna', p['pompa_wod'] + ' W'))
    if p['grzalka']: par.append(('Podgrzewacz wody', p['grzalka'] + ' W'))
    for k, n in (('led rgb', 'Oświetlenie LED RGB'), ('bluetooth', 'Bluetooth'), ('usb', 'Port USB'), ('radio', 'Radio FM'), ('wodospad', 'Wodospad'), ('pilot', 'Pilot zdalnego sterowania'), ('ozon', 'Dezynfekcja ozonowa')):
        if c.get(k): par.append((n, 'tak'))
    par += [(a, ladnie(b)) for a, b in p['elektryka']]
    if p['ean']: par.append(('EAN', p['ean']))
    if p['realizacja30']: par.append(('Czas realizacji', '30 dni'))
    kl = [f'{L} x {W} x {Hh} cm' + (f', ok. {p["pojemnosc"]} l' if p['pojemnosc'] else '')]
    if p['dysze_pow'] and p['dysze_wod']: kl.append(f'{p["dysze_pow"]} dysz powietrznych i {p["dysze_wod"]} wodnych')
    if p['dysze_plecy']: kl.append(f'Dysze obrotowe do masażu pleców')
    if p['grzalka']: kl.append(f'Podgrzewacz wody {p["grzalka"]} W')
    if c.get('led rgb'): kl.append('Oświetlenie LED RGB')
    kl.append(', '.join([n for k, n in (('bluetooth', 'Bluetooth'), ('usb', 'USB'), ('radio', 'radio FM'), ('pilot', 'pilot')) if c.get(k)]) or 'Panel dotykowy')
    if c.get('wodospad'): kl.append('Bateria z wodospadem')
    return lead, bloki, lst, par, kl[:6], 'Wanna z hydromasażem do domu'

def tresc_biezni(p):
    w = ' '.join(p['wyroznienia']); moc = tech(p, 'Moc silnika') or ''; obc = tech(p, 'Maksymalne obciążenie') or ''; pr = tech(p, 'Prędkość') or ''
    mk = ladnie(moc.split('(')[0]).replace(' AC', '').strip()
    szczyt = re.search(r'(\d+)\s*KM \(moc szczytowa\)', moc)
    ekr = f'dotykowym ekranem Android {p["ekran"].replace(".", ",")} cala' if p['ekran'] else 'wyświetlaczem LCD'
    lead = f'{p["model"]}{" " + p["seria"] if p.get("seria") else ""} to bieżnia elektryczna z silnikiem {mk}' + (f' ({szczyt.group(1)} KM mocy szczytowej)' if szczyt else '') + \
           (f', pasem {p["pas"].replace("x", " x ")} cm' if p['pas'] else '') + f' i {ekr}.' + (f' Unosi użytkownika do {ladnie(obc)}.' if obc else '')
    if p.get('komercyjna'): lead += ' To wersja komercyjna tej bieżni.'
    if p.get('zestaw'): lead += ' W zestawie dodatki: masażer, hantle, przyrząd do brzuszków i mata.'
    bl = []
    t = (f'Silnik rozpędza pas w zakresie {ladnie(pr)}' if pr else 'Mocny silnik zapewnia płynną pracę pasa') + ('; dzięki technologii Silent Motion pracuje cicho.' if 'Silent Motion' in w else '.')
    if obc: t += f' Stabilna rama przenosi obciążenie do {ladnie(obc)}.'
    bl.append(('Silnik i rama', f'Silnik {mk}' + (f', obciążenie do {ladnie(obc)}' if obc else ''), t))
    if p['ekran']:
        t = 'Kolorowy ekran dotykowy z menu po polsku obsługuje się jak tablet.'
        if 'internetu' in w: t += ' Po połączeniu z internetem otworzysz stronę albo film.'
        if p['aplikacje']: t += ' Bieżnia współpracuje z aplikacjami ' + ', '.join(p['aplikacje'][:-1]) + ' i ' + p['aplikacje'][-1] + '.'
        if 'Bluetooth' in w: t += ' Ma też Bluetooth do połączenia z telefonem lub tabletem.'
        bl.append(('Ekran', f'Dotykowy ekran Android {p["ekran"].replace(".", ",")} cala', t))
    else:
        bl.append(('Ekran', 'Czytelny wyświetlacz LCD', 'Na wyświetlaczu widać czas, prędkość, tętno, kalorie i dystans. Prędkość zmienisz przyciskami w rączkach albo na panelu.'))
    if p['pas']:
        t = ('System amortyzacji zmniejsza obciążenie kości i stawów podczas biegu.' if p['amortyzacja'] else 'Pas biegowy pracuje równo i stabilnie.')
        if tech(p, 'System kompensacji') == 'tak': t += ' System kompensacji nierówności stabilizuje bieżnię na podłodze.'
        kat = tech(p, 'Maksymalny kąt')
        if kat: t += f' Nachylenie pasa ustawisz elektronicznie, maksymalnie {ladnie(kat).replace(" °", "°")}.'
        bl.append(('Pas biegowy', f'Pas {p["pas"].replace("x", " x ")} cm' + (' z amortyzacją' if p['amortyzacja'] else ''), t))
    if 'siłownik' in w:
        bl.append(('Składanie', 'Składa się z pomocą siłownika gazowego', 'Pas podnosi się bez wysiłku, a złożoną bieżnię przesuniesz na kółkach transportowych pod ścianę albo do innego pokoju.'))
    bloki = ''.join(blok(p, i + 1, *b) for i, b in enumerate(bl))
    lst = '<h3 class="lst-h">Najważniejsze cechy</h3><ul class="lst">' + ''.join(f'<li>{E(ladnie(x).replace(" cala (Android)", " cala, Android"))}</li>' for x in p['wyroznienia']) + '</ul>' if p['wyroznienia'] else ''
    if p['gratisy'] and p['model'] == 'APV8000':
        lst += '<h3 class="lst-h">W cenie</h3><p class="mat">Zestaw dodatków o wartości katalogowej 800 zł: masażer, twister, 2 hantle, rama do brzuszków z gąbkami, wygłuszająca mata pod bieżnię i olej silikonowy do pasa.</p>'
    par = [('Model', p['model'] + (f' / {p["seria"]}' if p.get('seria') else ''))] + [(k, ladnie(v)) for k, v in p['tech']]
    if p['ekran']: par.insert(1, ('Ekran', f'dotykowy TFT {p["ekran"].replace(".", ",")} cala, Android, menu po polsku'))
    elif p['ekran_lcd']: par.insert(1, ('Ekran', 'LCD'))
    if p['realizacja30']: par.append(('Czas realizacji', '30 dni'))
    kl = [x for x in [f'Silnik {mk}' + (f', {szczyt.group(1)} KM mocy szczytowej' if szczyt else ''), f'Pas biegowy {p["pas"].replace("x", " x ")} cm' if p['pas'] else None,
                      (f'Dotykowy ekran Android {p["ekran"].replace(".", ",")} cala' if p['ekran'] else 'Wyświetlacz LCD'),
                      f'Prędkość {ladnie(pr)}' + (f', obciążenie do {ladnie(obc)}' if obc else '') if pr else None,
                      'Składanie z siłownikiem gazowym' if 'siłownik' in w else None,
                      ('Aplikacje ' + ', '.join(p['aplikacje'])) if p['aplikacje'] else ('Bluetooth' if 'Bluetooth' in w else None)] if x]
    return lead, bloki, lst, par, kl[:6], 'Bieżnia elektryczna do domu'

def tresc_akc(p):
    lead = ' '.join(p['opis'][:2]) if p.get('opis') else ''
    lead = lead.replace('Prezentujemy Państwu', 'Proponujemy').replace('Prezentujemy', 'Proponujemy').replace('Prezentowana mata', 'Mata')
    if p['id'] == 20522:
        lead = 'Zestaw dodatków do bieżni APV8000: profesjonalny masażer, twister, 2 hantle, rama do robienia brzuszków z gąbkami, wygłuszająca mata pod bieżnię i olej silikonowy do konserwacji pasa.'
    lst = '<h3 class="lst-h">Cechy</h3><ul class="lst">' + ''.join(f'<li>{E(x)}</li>' for x in p['wyroznienia']) + '</ul>' if p['wyroznienia'] else ''
    return lead, '', lst, [], p['wyroznienia'][:6], 'Akcesorium do bieżni'

def strona_produktu(p):
    k = kier(p); d = DOST[p['dost']]
    lead, bloki, lst, par, kl, h2 = {'wanna': tresc_wanny, 'bieznia': tresc_biezni, 'akcesorium': tresc_akc}[p['typ']](p)
    kat = ('wanny-z-hydromasazem', 'Wanny z hydromasażem') if p['typ'] == 'wanna' else ('bieznie-elektryczne', 'Bieżnie elektryczne')
    marka = 'Aquaholm' if p['typ'] == 'wanna' else 'APVsport'
    Z = p['zdjecia']; z0 = Z[0]
    gal = (f'<div class="gl"><button class="duze" type="button" data-lb="../img/p/{z0["d"][0]}" aria-label="Powiększ zdjęcie">'
           f'<img id="duze" src="../img/p/{z0["d"][0]}" srcset="../img/p/{z0["m"][0]} {z0["m"][1]}w, ../img/p/{z0["d"][0]} {z0["d"][1]}w" sizes="(max-width:900px) 92vw, 52vw" width="{z0["d"][1]}" height="{z0["d"][2]}" fetchpriority="high" alt="{E(p["nazwa"])}"></button>')
    if len(Z) > 1:
        gal += '<div class="mini">' + ''.join(
            f'<button type="button" data-duze="../img/p/{z["d"][0]}" data-alt="{E(p["krotka"])}, zdjęcie {i + 1}"{" aria-current=\"true\"" if i == 0 else ""} aria-label="Zdjęcie {i + 1} z {len(Z)}">'
            f'<img src="../img/p/{z["m"][0]}" width="120" height="120" loading="lazy" decoding="async" alt=""></button>' for i, z in enumerate(Z)) + '</div>'
    gal += '</div>'
    st = (f'<s>{zl(p["stara"])}</s><span class="oszcz">taniej o {zl(p["stara"] - p["cena"])}</span>' if p['stara'] else '')
    if p['dost'] != 'brak':
        kup = (f'<div class="kup"><div class="ilosc"><button type="button" data-il="-1" aria-label="Mniej">-</button><input id="il" type="number" min="1" value="1" aria-label="Ilość"><button type="button" data-il="1" aria-label="Więcej">+</button></div>'
               f'<button type="button" class="dok" data-kosz data-id="{p["id"]}" data-nazwa="{E(p["nazwa"])}" data-cena="{p["cena"]}" data-url="./" data-img="../img/p/{z0["m"][0]}">Dodaj do koszyka</button></div>')
    else:
        kup = (f'<div class="kup"><a class="dok pyt" href="{WA}" target="_blank" rel="noopener">Zapytaj o termin na WhatsAppie</a></div>'
               f'<p class="zest">Albo zadzwoń: <a href="tel:+48503538038">503 538 038</a>, pon.-pt. 9:00-18:00.</p>')
    opc = ('<label class="opc"><input type="checkbox" id="pas"><span><b>Dodaj pas piersiowy do pomiaru tętna: 125 zł</b> <s>139 zł</s><small>Tętno wyświetla się na ekranie bieżni.</small></span></label>'
           if p.get('pas_opcja') and p['dost'] != 'brak' else '')
    zest = ('<p class="zest">W cenie zestaw dodatków o wartości 800 zł: masażer, twister, 2 hantle, rama do brzuszków, mata i olej silikonowy.</p>'
            if p.get('gratisy') and p.get('model') == 'APV8000' else '')
    if p['typ'] == 'wanna' and p['dost'] == 'zam':
        zest = '<p class="zest"><b>Czekasz, zyskujesz:</b> wanna z terminem realizacji 30 dni kosztuje mniej niż ta sama wanna od ręki.</p>'
    fl = filmy_dla(p)
    fn = film_nat(p)
    filmy = fn + ''.join(f'<figure class="film"><button class="fa" type="button" data-yt="{i}" aria-label="Odtwórz film: {E(t)}"><img src="../img/yt-{i}.webp" width="480" height="270" loading="lazy" decoding="async" alt=""><span class="od" aria-hidden="true"></span></button><figcaption>{E(t)}</figcaption></figure>' for i, t in fl)
    tabela = ('<table class="par"><caption>Parametry techniczne</caption><tbody>' + ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in par) + '</tbody></table>') if par else ''
    pod = sorted([x for x in P if x['typ'] == p['typ'] and x['id'] != p['id']] if p['typ'] != 'akcesorium' else [x for x in P if x['id'] != p['id'] and (x['typ'] == 'akcesorium' or x['id'] in (20185, 20175, 20177))],
                 key=lambda x: (x['dost'] == 'brak', abs(x['cena'] - p['cena'])))[:8]
    zakl = [('opis', 'Opis')] + ([('parametry', 'Parametry')] if tabela else []) + ([('filmy', 'Filmy')] if (fl or fn) else []) + [('dostawa', 'Dostawa i płatności'), ('opinie', 'Opinie'), ('podobne', 'Podobne')]
    sek_par = f'<section class="sek szary" id="parametry" aria-labelledby="h-par"><div class="wrap"><div class="sg"><div><h2 id="h-par">Parametry</h2></div></div>{tabela}</div></section>' if tabela else ''
    sek_fil = f'<section class="sek" id="filmy" aria-labelledby="h-fil"><div class="wrap"><div class="sg"><div><h2 id="h-fil">Filmy</h2><p class="lead">{"Film odtwarza się po kliknięciu. " if fn else ""}{"Odtwarzacz YouTube włącza się dopiero po kliknięciu." if fl else ""}</p></div></div><div class="fl2">{filmy}</div></div></section>' if (fl or fn) else ''
    dostawa = wytnij('<div class="info4">', '</section>', produkt.strona)
    url = BAZA + p['slug'] + '/'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'TREG', 'item': BAZA},
                                                        {'@type': 'ListItem', 'position': 2, 'name': kat[1], 'item': BAZA + kat[0] + '/'},
                                                        {'@type': 'ListItem', 'position': 3, 'name': p['nazwa'], 'item': url}]},
        {'@type': 'Product', 'name': p['nazwa'], 'sku': p['sku'] or str(p['id']), **({'gtin13': p['ean']} if p.get('ean') else {}),
         'brand': {'@type': 'Brand', 'name': marka}, 'image': [BAZA + 'img/p/' + z['d'][0] for z in Z[:3]], 'description': opis_krotki(p),
         'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'PLN', 'price': f'{p["cena"]}.00', 'availability': 'https://schema.org/' + SCH[p['dost']],
                    'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@type': 'Organization', 'name': 'TREG Łukasz Pawluczuk'}}}]}
    tytul = f'{p["nazwa"]} | TREG'
    opis = f'{p["nazwa"]}: {opis_krotki(p)}. {zl(p["cena"])}, raty 0%, PayPo, BLIK.'
    if len(opis) > 160: opis = f'{p["krotka"]}: {opis_krotki(p)}. {zl(p["cena"])}, raty 0%, PayPo.'
    if len(opis) > 160: opis = opis[:157].rsplit(' ', 1)[0] + '...'
    tresc = f'''<section class="kp{' bz' if k == 'apv' else ''}" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / <a href="../{kat[0]}/">{kat[1]}</a> / {E(p['krotka'])}</nav>
    <div class="kp-g">
      {gal}
      <div class="zak" id="zakup">
        <span class="marka"><span class="kw {k}"></span>{marka}</span>
        <h1 id="h1">{E(p['nazwa'])}</h1>
        <a class="ocz" href="#opinie">Opinie kupujących z Opinii Zaufanych Ceneo</a>
        <p class="cena"><b>{zl(p['cena'])}</b>{st}</p>
        <p class="dost {d[0]}"><span class="b" aria-hidden="true"></span>{d[1]}</p>
        <ul class="kl">{''.join(f'<li>{E(x)}</li>' for x in kl)}</ul>
        {opc}
        {kup}
        <div class="zauf">
          <span><span class="kw apv"></span>Raty 0%</span><span><span class="kw aq"></span>PayPo: zapłać za 30 dni</span>
          <span><span class="kw apv"></span>BLIK i przelew</span><span><span class="kw aq"></span>Gwarancja najniższej ceny</span>
          <span><span class="kw apv"></span>Serwis w całym kraju</span><span><span class="kw aq"></span>Wysyłka ubezpieczona</span>
        </div>
        {zest}
      </div>
    </div>
  </div>
</section>
<nav class="zakl" aria-label="Sekcje produktu"><div class="wrap">{''.join(f'<a href="#{a}">{b}</a>' for a, b in zakl)}</div></nav>
<section class="sek{' bz' if k == 'apv' else ''}" id="opis" aria-labelledby="h-opis">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-opis"><span class="kw {k}"></span>{h2}</h2><p class="lead">{E(lead)}</p></div></div>
    {bloki}
    {lst}
  </div>
</section>
{sek_par}
{sek_fil}
<section class="sek szary" id="dostawa" aria-labelledby="h-dostawa">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-dostawa">Dostawa, płatności i zwroty</h2><p class="lead">Szczegóły na stronie <a href="../dostawa-i-platnosci/">Dostawa i płatności</a> i w <a href="../regulamin/">regulaminie</a>.</p></div></div>
    {dostawa}</section>
<section class="sek opinie" id="opinie" aria-labelledby="h-opinie">
  <div class="wrap">
    <div>
      <h2 id="h-opinie">Opinie kupujących</h2>
      <p>Opinie zbieramy w programie Opinie Zaufane Ceneo: po każdym zamówieniu kupujący dostaje krótką ankietę. Po uruchomieniu sklepu opinie pokażą się w tym miejscu.</p>
      <a class="btn wa" href="{WA}" target="_blank" rel="noopener">Zapytaj na WhatsAppie</a>
    </div>
    <div class="miejsce"><b>Opinie Zaufane Ceneo</b><span>Miejsce na opinie i ocenę sklepu treg.pl.</span></div>
  </div>
</section>
<section class="sek szary" id="podobne" aria-labelledby="h-pod">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-pod"><span class="kw {k}"></span>{'Podobne wanny' if p['typ'] == 'wanna' else ('Podobne bieżnie' if p['typ'] == 'bieznia' else 'Do bieżni')}</h2></div></div>
    <div class="siat">{''.join(karta(x) for x in pod)}</div>
  </div>
</section>
<div class="pas" id="pasek" aria-hidden="true"><div class="wrap"><span class="n">{E(p['nazwa'])}</span><b>{zl(p['cena'])}</b><a class="dok" href="#zakup" tabindex="-1">{'Kup teraz' if p['dost'] != 'brak' else 'Zapytaj o termin'}</a></div></div>'''
    skr = re.search(r'<script>\n\(function\(\)\{var d=document,du=.*?</script>', produkt.strona, re.S).group(0)
    skr = skr.replace("['opis','parametry','filmy','dostawa','opinie','podobne']", json.dumps([a for a, b in zakl]).replace('"', "'"))
    skr = skr.replace("d.querySelectorAll('.mini button').forEach(function(b){b.addEventListener('click',function(){du.removeAttribute('srcset');",
                      "d.querySelectorAll('.mini button').forEach(function(b){b.addEventListener('click',function(){du.removeAttribute('srcset');du.removeAttribute('width');du.removeAttribute('height');")
    zapisz(p['slug'], podstrona(tytul, opis, p['slug'] + '/', tresc, ld, skr))

# --- karty produktow (APV8000 Futura Prestige 6 KM ma recznie dopracowana karte w produkt.py)
for p in P:
    if p['id'] != 20185: strona_produktu(p)

# --- kategorie
def kategoria(sciezka, h1, tytul, opis, lead, prod, filtry, dodatkowe=''):
    fb = ''.join(f'<button type="button" data-f="{f}" aria-pressed="{"true" if f == "" else "false"}">{E(n)}</button>' for f, n in filtry)
    tresc = f'''<section class="kat" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / {E(h1)}</nav>
    <h1 id="h1">{E(h1)}</h1>
    <p class="lead">{E(lead)}</p>
    <div class="filtry" role="group" aria-label="Filtruj produkty">{fb}<label>Sortuj<select id="sort"><option value="">polecane</option><option value="r">cena: od najniższej</option><option value="m">cena: od najwyższej</option></select></label></div>
    <p class="ile" id="ile" aria-live="polite"></p>
  </div>
</section>
<section class="sek" aria-label="Produkty">
  <div class="wrap"><div class="siat" id="siat">{''.join(karta(x, 'h2') for x in prod)}</div></div>
</section>
{dodatkowe}
<section class="sek szary" aria-labelledby="h-dostawa">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-dostawa">Dostawa, płatności i serwis</h2><p class="lead">Więcej na stronie <a href="../dostawa-i-platnosci/">Dostawa i płatności</a>.</p></div></div>
    {wytnij('<div class="info4">', '</section>', produkt.strona)}</section>'''
    skr = '''<script>
(function(){var d=document,s=d.getElementById('siat'),k=[].slice.call(s.children),bt=[].slice.call(d.querySelectorAll('[data-f]')),so=d.getElementById('sort'),ile=d.getElementById('ile'),f='';
function odm(n){return n===1?'produkt':(n%10>=2&&n%10<=4&&(n%100<10||n%100>=20)?'produkty':'produktów')}
function rob(){var n=0;k.forEach(function(e){var ok=!f||f.split(';').every(function(w){var a=w.split(':');return e.dataset[a[0]]===a[1]});e.hidden=!ok;if(ok)n++});
var v=so.value,l=k.slice();if(v)l.sort(function(a,b){return v==='r'?a.dataset.cena-b.dataset.cena:b.dataset.cena-a.dataset.cena});l.forEach(function(e){s.appendChild(e)});ile.textContent=n+' '+odm(n)}
bt.forEach(function(b){b.addEventListener('click',function(){f=b.dataset.f;bt.forEach(function(x){x.setAttribute('aria-pressed',x===b)});rob()})});so.addEventListener('change',rob);rob()})();
</script>'''
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'TREG', 'item': BAZA}, {'@type': 'ListItem', 'position': 2, 'name': h1, 'item': BAZA + sciezka + '/'}]},
        {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BAZA + x['slug'] + '/'} for i, x in enumerate(prod)]}]}
    zapisz(sciezka, podstrona(tytul, opis, sciezka + '/', tresc, ld, skr))

W = [p for p in P if p['typ'] == 'wanna']
W.sort(key=lambda p: (p['dost'] == 'brak', p['ksztalt'] != 'prostokatna', p['kolor'] == 'czarna', p['cena']))
kategoria('wanny-z-hydromasazem', 'Wanny z hydromasażem', 'Wanny z hydromasażem Aquaholm: prostokątne, narożne, podwójne | TREG',
          f'{len(W)} wanien z hydromasażem Aquaholm Premium Line: prostokątne, narożne i podwójne, białe i czarne. Podgrzewacz, LED RGB, Bluetooth. Raty 0%.',
          f'{len(W)} modeli z serii Premium Line: prostokątne, narożne i podwójne, białe i czarne. Większość z podgrzewaczem wody, oświetleniem LED RGB, Bluetooth i pilotem. Wanna na zamówienie z realizacją 30 dni kosztuje mniej niż ta sama wanna od ręki.',
          W, [('', 'Wszystkie'), ('ksztalt:prostokatna', 'Prostokątne'), ('ksztalt:narozna', 'Narożne'), ('ksztalt:podwojna', 'Podwójne'), ('kolor:biala', 'Białe'), ('kolor:czarna', 'Czarne'), ('dost:jest', 'Od ręki')])
B = [p for p in P if p['typ'] == 'bieznia']
B.sort(key=lambda p: (p['dost'] == 'brak', p['model'] != 'APV8000', p.get('komercyjna', False), -p['cena'] if p['model'] == 'APV8000' else p['cena']))
A = [p for p in P if p['typ'] == 'akcesorium']
akc = f'''<section class="sek szary" aria-labelledby="h-akc">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-akc"><span class="kw apv"></span>Akcesoria do bieżni</h2><p class="lead">Pas do pomiaru tętna, mata pod bieżnię i zestaw dodatków.</p></div></div>
    <div class="siat">{''.join(karta(x) for x in A)}</div>
  </div>
</section>'''
kategoria('bieznie-elektryczne', 'Bieżnie elektryczne', 'Bieżnie elektryczne APVsport APV8000, APV6000, APV5000 | TREG',
          f'{len(B)} bieżni elektrycznych APVsport: APV8000 z silnikiem do 6 KM i pasem 145 x 58 cm, APV6000, APV5000, APV900, APV600. Akcesoria. Raty 0%.',
          'Bieżnie APVsport do domu i do intensywnego treningu: APV8000 z silnikiem do 6 KM, pasem 145 x 58 cm i ekranem Android, a także APV6000, APV5000, APV900 i APV600. Doradzimy przy wyborze modelu, mamy własny serwis i części.',
          B, [('', 'Wszystkie'), ('model:apv8000', 'APV8000'), ('model:inne', 'Pozostałe modele'), ('dost:zam', 'Dostępne do zamówienia')], akc)

# --- koszyk
kosz = f'''<section class="kosz-s" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / Koszyk</nav>
    <h1 id="h1">Koszyk</h1>
    <div class="pusty" id="pusty" hidden><p>Koszyk jest pusty.</p><div class="akc"><a class="btn aq" href="../wanny-z-hydromasazem/">Wanny z hydromasażem</a><a class="btn apv" href="../bieznie-elektryczne/">Bieżnie elektryczne</a></div></div>
    <div class="kg" data-pelny hidden>
      <div>
        <ul id="lista" aria-label="Produkty w koszyku"></ul>
        <p class="razem"><span>Razem za produkty</span><b id="suma">0 zł</b></p>
        <p class="uw">Koszt dostawy doliczamy zgodnie z cennikiem dostaw z dnia zamówienia. Zamawiając wannę lub bieżnię na zamówienie, przed wysyłką potwierdzimy termin realizacji.</p>
      </div>
      <form class="zamf" id="zamowienie" novalidate>
        <h2>Dane do zamówienia</h2>
        <div class="r2"><label>Imię i nazwisko<input type="text" name="n" autocomplete="name" required></label><label>Telefon<input type="tel" name="t" autocomplete="tel" required></label></div>
        <label>E-mail<input type="email" name="e" autocomplete="email" required></label>
        <label>Ulica i numer<input type="text" name="u" autocomplete="street-address" required></label>
        <div class="r2"><label>Kod pocztowy<input type="text" name="k" autocomplete="postal-code" required></label><label>Miejscowość<input type="text" name="m" autocomplete="address-level2" required></label></div>
        <fieldset><legend>Dostawa</legend>
          <label class="op"><input type="radio" name="dost" checked><span>Kurier<small>Także przesyłki nadwymiarowe i bardzo ciężkie, ubezpieczone.</small></span></label>
        </fieldset>
        <fieldset><legend>Płatność</legend>
          <label class="op"><input type="radio" name="pl" checked><span>Płatność online: BLIK, przelew, karta</span></label>
          <label class="op"><input type="radio" name="pl"><span>Raty 0%</span></label>
          <label class="op"><input type="radio" name="pl"><span>PayPo: zapłać za 30 dni</span></label>
          <label class="op"><input type="radio" name="pl"><span>Przelew tradycyjny</span></label>
          <label class="op"><input type="radio" name="pl"><span>Płatność przy odbiorze</span></label>
        </fieldset>
        <label class="zg"><input type="checkbox" required><span>Akceptuję <a href="../regulamin/">regulamin sklepu</a> i zapoznałem się z <a href="../polityka-prywatnosci/">polityką prywatności</a>.</span></label>
        <button class="btn ciem" type="submit">Zamawiam i płacę</button>
        <p class="komunikat" id="komunikat" tabindex="-1" hidden>To podgląd sklepu. Zamówienia i płatności zaczną działać po uruchomieniu sklepu na WooCommerce.</p>
      </form>
    </div>
  </div>
</section>'''
zapisz('koszyk', podstrona('Koszyk | TREG', 'Koszyk sklepu TREG: wanny z hydromasażem Aquaholm i bieżnie elektryczne APVsport.', 'koszyk/', kosz))

# --- strony tresci z treg.pl
def czysty_html(h):
    h = re.sub(r'<(script|style|iframe|img|figure)[^>]*>.*?</\1>|<img[^>]*>', '', h, flags=re.S)
    h = re.sub(r'<(/?)(span|div|font|section|a)[^>]*>', '', h)
    h = re.sub(r'<(p|h1|h2|h3|h4|ul|ol|li|strong|b|em|br)\s[^>]*>', r'<\1>', h)
    h = re.sub(r'<h1>', '<h2>', h).replace('</h1>', '</h2>')
    h = re.sub(r'<p>\s*(?:&nbsp;|\s)*</p>', '', h)
    return h.strip()

def tekst(sciezka, h1, tytul, opis, html_tresc, ld_typ='WebPage'):
    t = f'<section class="tekst" aria-labelledby="h1"><div class="wrap"><nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / {E(h1)}</nav><h1 id="h1">{E(h1)}</h1>{html_tresc}</div></section>'
    zapisz(sciezka, podstrona(tytul, opis, sciezka + '/', t))

ZR = 'tresci'
def wczytaj(n): return json.load(open(f'{ZR}/{n}', encoding='utf-8'))['content']['rendered']
reg = czysty_html(wczytaj('regulamin.json'))
reg = re.sub(r'Regulamin Sklepu Internetowego treg\.pl', '', reg, count=1)
reg = re.sub(r'<p>\s*(?:<strong>\s*</strong>|<b>\s*</b>)?\s*</p>', '', reg)
tekst('regulamin', 'Regulamin sklepu', 'Regulamin sklepu internetowego treg.pl | TREG', 'Regulamin sklepu internetowego treg.pl prowadzonego przez TREG Łukasz Pawluczuk z Bielska Podlaskiego: zamówienia, płatności, dostawa, zwroty i reklamacje.', reg)
pol = czysty_html(wczytaj('polityka.json'))
tekst('polityka-prywatnosci', 'Polityka prywatności', 'Polityka prywatności | TREG', 'Polityka prywatności serwisu treg.pl: administrator danych TREG Łukasz Pawluczuk, cele i podstawy przetwarzania, prawa użytkowników, pliki cookies.', pol)

dost_html = f'''<p>Sklep treg.pl prowadzi TREG Łukasz Pawluczuk z Bielska Podlaskiego. Wanny i bieżnie wysyłamy kurierem w całej Polsce, każdą przesyłkę solidnie pakujemy i ubezpieczamy.</p>
<h2>Dostawa</h2>
<ul><li>Kurierem: przedmioty o standardowych wymiarach, paczka do 25 kg.</li><li>Kurierem: przedmioty nadwymiarowe i bardzo ciężkie, czyli wanny i bieżnie.</li><li>Koszty wysyłki pokrywa kupujący, doliczamy je do zamówienia zgodnie z cennikiem dostaw obowiązującym w dniu zamówienia.</li>
<li>Produkty oznaczone „na zamówienie” mają czas realizacji 30 dni. Przed wysyłką potwierdzimy termin.</li></ul>
<p><b>Sprawdź przesyłkę przy kurierze.</b> Reklamacje uszkodzeń mechanicznych powstałych w transporcie rozpatrujemy na podstawie protokołu reklamacyjnego spisanego w obecności doręczyciela.</p>
<h2>Płatności</h2>
<ul><li>Płatność online: BLIK, przelew, karta.</li><li>Raty 0%.</li><li>PayPo: zapłać za 30 dni.</li><li>Przelew bankowy.</li><li>Płatność przy odbiorze gotówką (przy dostawie kurierem).</li></ul>
<h2>Zwroty</h2>
<p>Kupując przez internet jako konsument, możesz odstąpić od umowy w ciągu 14 dni od otrzymania towaru, bez podawania przyczyny. Zwracany towar musi być nieużywany, w oryginalnym opakowaniu i kompletny (z osprzętem). Pieniądze za zwrócony towar odeślemy na podane konto lub adres w ciągu 7 dni roboczych. Koszty zwrotu ponosi kupujący. Pokrywamy koszty przesyłek wynikłych z błędnej realizacji zamówienia przez nasz sklep. Szczegóły w <a href="../regulamin/">regulaminie</a>.</p>
<h2>Gwarancja i serwis</h2>
<p>Mamy profesjonalny serwis gwarancyjny i pogwarancyjny na terenie całego kraju oraz magazyn części zamiennych do naszych produktów. Do każdego produktu dołączamy dokument gwarancyjny z dowodem zakupu, instrukcją montażu i obsługi oraz drukiem reklamacyjnym. Typ i okres gwarancji zależą od modelu i są opisane w dokumencie gwarancyjnym.</p>
<p>Zwroty i reklamacje prosimy kierować na adres: TREG Łukasz Pawluczuk, ul. 30 Lipca 2, 17-100 Bielsk Podlaski, tel. <a href="tel:+48503538038">503 538 038</a>, e-mail <a href="mailto:sklep@treg.pl">sklep@treg.pl</a>.</p>'''
tekst('dostawa-i-platnosci', 'Dostawa i płatności', 'Dostawa, płatności, zwroty i serwis | TREG', 'Dostawa wanien i bieżni kurierem w całej Polsce, płatność BLIK, raty 0%, PayPo, przelew lub przy odbiorze. Zwroty 14 dni, serwis i części.', dost_html)

kon = popraw_linki(wytnij('<section class="sek kontakt" id="kontakt"', '</section>') + '</section>')
kon = kon.replace('<h2 id="h-kontakt">Zadzwoń albo napisz</h2>', '<h1 id="h-kontakt">Kontakt</h1><p class="lead" style="margin-top:12px">TREG Łukasz Pawluczuk, ul. 30 Lipca 2, 17-100 Bielsk Podlaski, NIP 543-200-95-88, REGON 200140166.</p>')
kon = f'<div class="wrap" style="padding-top:clamp(22px,3vw,40px)"><nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / Kontakt</nav></div>' + kon
zapisz('kontakt', podstrona('Kontakt: TREG Bielsk Podlaski, tel. 503 538 038 | TREG', 'Kontakt ze sklepem TREG: tel. 503 538 038 (pon.-pt. 9-18), sklep@treg.pl, ul. 30 Lipca 2, 17-100 Bielsk Podlaski. Wanny z hydromasażem i bieżnie.', 'kontakt/', kon,
                           {'@context': 'https://schema.org', '@type': 'Store', 'name': 'TREG Łukasz Pawluczuk', 'telephone': '+48503538038', 'email': 'sklep@treg.pl', 'url': BAZA,
                            'address': {'@type': 'PostalAddress', 'streetAddress': 'ul. 30 Lipca 2', 'postalCode': '17-100', 'addressLocality': 'Bielsk Podlaski', 'addressCountry': 'PL'}}))

fir = popraw_linki(wytnij('<section class="sek firma" id="firma"', '</section>') + '</section>')
fir = fir.replace('poster="film/', 'poster="../film/').replace('data-src="film/', 'data-src="../film/')
fir = fir.replace('<h2 id="h-firma">TREG: jedna firma, dwa kierunki</h2>', '<h1 id="h-firma">TREG: jedna firma, dwa kierunki</h1>')
fir = fir.replace('href="#wanny"', 'href="../wanny-z-hydromasazem/"').replace('href="#bieznie"', 'href="../bieznie-elektryczne/"')
opi = popraw_linki(wytnij('<section class="sek szary opinie" id="opinie"', '</section>') + '</section>').replace('href="#kontakt"', 'href="../kontakt/"')
zapisz('o-firmie', podstrona('O firmie TREG z Bielska Podlaskiego: Aquaholm i APVsport | TREG', 'TREG Łukasz Pawluczuk z Bielska Podlaskiego: wanny z hydromasażem Aquaholm i bieżnie elektryczne APVsport. Produkcja, serwis i magazyn części.', 'o-firmie/',
                             f'<div class="wrap" style="padding-top:clamp(22px,3vw,40px)"><nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / O firmie</nav></div>' + fir + opi))

# --- mapa strony
sm = open('sitemap.xml', encoding='utf-8').read()
for s in STRONY:
    if BAZA + s not in sm: sm = sm.replace('</urlset>', f'<url><loc>{BAZA}{s}</loc></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('sklep ok', len(STRONY))
