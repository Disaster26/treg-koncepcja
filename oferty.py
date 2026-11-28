# Karty produktow jako uporzadkowane kopie ofert z aquaholm.pl (prosba klienta 28.11.2026):
# ta sama kolejnosc elementow co w sklepie klienta, pelny oryginalny opis (tylko formatowanie i literowki),
# wszystkie zdjecia galerii, filmy, rysunki techniczne, podobne produkty jak u klienta.
# Zrodlo: oferty_zrodlo.json (strony produktow aquaholm.pl pobrane 28.11.2026, parser: _src/wyciag.py),
# obrazy: _src/aq2811/raw -> img/o (WebP, bez powiekszania).
import json, os, re, html as H
from bs4 import BeautifulSoup, NavigableString, Tag

E = H.escape
Z = json.load(open('oferty_zrodlo.json', encoding='utf-8'))
O = {int(k): v for k, v in Z['oferty'].items()}
KOLEJNOSC = Z['kolejnosc_sklep']          # /sklep/ aquaholm.pl
KOL_WANNY = Z['kolejnosc_wanny']          # /kategoria-produktu/wanny/
KOL_BIEZNIE = Z['kolejnosc_bieznie']      # /kategoria-produktu/bieznie-elektryczne-do-biegania-i-chodzenia/
PERM = {v['url']: k for k, v in O.items()}
RAW = '_src/aq2811/raw/'
MAPA = json.load(open('_src/aq2811/raw_mapa.json', encoding='utf-8')) if os.path.exists('_src/aq2811/raw_mapa.json') else {}
OBR = json.load(open('img/o/obrazy.json', encoding='utf-8')) if os.path.exists('img/o/obrazy.json') else {}

# --- obrazy: WebP w natywnym rozmiarze (maks. 1600 px), miniatury galerii 160 px
def obraz(url, miniatura=False):
    k = url + ({True: '#t', False: '', 'm': '#m'}[miniatura])
    if k in OBR: return OBR[k]
    from PIL import Image
    src = RAW + MAPA[url]
    im = Image.open(src)
    if getattr(im, 'is_animated', False): im.seek(0)
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    if im.mode == 'RGBA' and im.getextrema()[3][0] == 255: im = im.convert('RGB')
    w, h = im.size
    cel = {True: 160, False: min(w, 1600), 'm': min(w, 560)}[miniatura]
    if cel < w: im = im.resize((cel, round(h * cel / w)), Image.LANCZOS)
    n = os.path.splitext(MAPA[url])[0] + {True: '-t', False: '', 'm': '-m'}[miniatura] + '.webp'
    os.makedirs('img/o', exist_ok=True)
    im.save('img/o/' + n, 'WEBP', quality=84 if miniatura is False else 80, method=6)
    OBR[k] = (n, im.size[0], im.size[1])
    return OBR[k]

def zapisz_obrazy():
    json.dump(OBR, open('img/o/obrazy.json', 'w', encoding='utf-8'), indent=0)

# --- nazwy: oryginalny tytul klienta uporzadkowany (nazwa + dopisek z cechami)
DUZE = {'LED', 'RGB', 'USB', 'TFT', 'LCD', 'FM', 'TUV', 'CE', 'AC', 'UV', 'SB', 'PL', 'ENG', 'KM', 'II', 'RRSO', 'BLIK', 'LED,', 'RGB,'}
NAZWY_W = {'ANDROID': 'Android', 'AQUAHOLM': 'Aquaholm', 'APVSPORT': 'APVsport', 'BLUETOOTH': 'Bluetooth', 'KINOMAP': 'Kinomap',
           'ZWIFT': 'Zwift', 'FITSHOW': 'FitShow', 'PREMIUM': 'Premium', 'LINE': 'Line', 'FUTURA': 'Futura', 'PRESTIGE': 'Prestige',
           'TOP': 'Top', 'QUALITY': 'Quality', 'PRO': 'Pro', 'SAFE': 'Safe', 'PAYPO': 'PayPo', 'ROHS': 'RoHS', 'AMBIENTE': 'Ambiente'}
def zdanie(t):
    """WIELKIE LITERY -> zwykle zdanie, skroty i nazwy wlasne zostaja."""
    sl = re.split(r'(\s+|[,/()+])', t)
    wy = []
    for s in sl:
        g = re.sub(r'[^\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]', '', s)
        if not g: wy.append(s); continue
        if re.search(r'\d', g) or g in DUZE or g in ('V', 'W', 'Hz', 'HP', 'PE', 'A'): wy.append(s); continue
        if g.upper() in NAZWY_W: wy.append(s.replace(g, NAZWY_W[g.upper()])); continue
        wy.append(s.lower())
    t = ''.join(wy).strip()
    m = re.search(r'[a-ząćęłńóśźż]', t)
    if m and not re.match(r'^\W*\d', t[:m.start()]) and t[:m.start()].strip(' >–-') == '':
        t = t[:m.start()] + t[m.start()].upper() + t[m.start() + 1:]
    return t

def caps(t):
    lit = re.sub(r'[^A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]', '', t)
    return len(lit) >= 6 and sum(c.isupper() for c in lit) / len(lit) > .7

def jednostki(t):
    t = re.sub(r'(\d)\s*[xX×]\s*(\d)', r'\1 x \2', t)
    t = re.sub(r'(\d)(cm|mm|kg|KM|W|V|zł|km/h|l|Hz)(?![\wąćęłńóśźż])', r'\1 \2', t)
    t = re.sub(r'(\d)\s?szt\.', r'\1 szt.', t)
    return t

def nazwa_oferty(o):
    n = re.sub(r'\s+', ' ', o['nazwa']).strip()
    n = re.sub(r'\.*\s*Czas realizacji: \d+ dni', '', n).strip(' .')
    n = re.sub(r'^\d grupa\s+', '', n, flags=re.I)
    m = re.match(r'(.*?)\s+(\d{3})cm x (\d{2,3})cm x (\d{2})cm\s*(.*)$', n)
    if 'hydromasa' in n and m:                                      # wanny
        glowna, L, W, Hh, cechy = m.groups()
        glowna = glowna.replace('PREMIUM LINE', 'Premium Line')
        km = re.search(r'\b(\d{4}S)\b', glowna)
        if km: glowna = glowna.replace(' ' + km.group(1), '') + ' ' + km.group(1)
        cechy = zdanie(cechy.replace('NOWOŚĆ!', '').strip(' ,')).replace('dysze obrotowe bluetooth', 'dysze obrotowe, Bluetooth').replace('Dysze obrotowe bluetooth', 'Dysze obrotowe, Bluetooth')
        cechy = cechy.replace('Dysze obrotowe Bluetooth', 'Dysze obrotowe, Bluetooth')
        return f'{glowna} {L} x {W} x {Hh} cm', cechy[:1].lower() + cechy[1:] if not cechy.startswith(('Bluetooth', 'USB')) else cechy
    if o['id'] in (20739, 20530, 20522):
        return {20739: ('Mata wygłuszająca APVsport pod bieżnię', 'model APV8000 oraz inny sprzęt sportowy'),
                20530: ('Pas piersiowy telemetryczny do pomiaru tętna', ''),
                20522: ('Zestaw dodatków do bieżni APV8000', 'masażer, twister, 2 hantle, rama do robienia brzuszków z gąbkami, mata pod bieżnię, olej silikonowy')}[o['id']]
    m = re.search(r'model APV8000,? SERIA ([A-Z ]+?) (\d)KM, pas biegowy (\d+)x(\d+)cm', n)
    if m:                                                           # APV8000
        seria = zdanie(m.group(1)).title().replace('Line', 'Line')
        g = f'Elektryczna bieżnia do biegania i chodzenia APV8000 {seria} {m.group(2)} KM'
        if n.startswith('WERSJA KOMERCYJNA'): g += ', wersja komercyjna'
        return g, f'pas biegowy {m.group(3)} x {m.group(4)} cm'
    m = re.match(r'APVsport Bieżnia elektryczna do biegania i chodzenia (APV\d+(?: S)?), (.*)$', n)
    if m:
        reszta = jednostki(m.group(2)).replace('ANDROID', 'Android').replace('10.1 cala', '10,1 cala').replace(' PROMOCJA! –', ':').replace('wyposażenie masażer', 'wyposażenie: masażer')
        return f'Bieżnia elektryczna do biegania i chodzenia APVsport {m.group(1)}', reszta
    return n, ''

# --- opis: oryginalny HTML klienta -> uporzadkowane bloki
POPRAWKI = [('obciążęnie', 'obciążenie'), ('tą serię', 'tę serię'), ('facebooka', 'Facebooka'), ('m. in.', 'm.in.'), ('do bieżni do bieżni', 'do bieżni'),
            ('IPhonem', 'iPhone’em'), ('Koloroterapia powszechnie wykorzystuje się', 'Koloroterapię powszechnie wykorzystuje się'),
            ('odporny przed uszkodzeniami', 'odporny na uszkodzenia'), ('wykonana z stali', 'wykonana ze stali'), ('nie uwierające', 'nieuwierające')]
def tekst_popraw(t):
    t = t.replace('\xa0', ' ').replace('″', '″')
    for a, b in POPRAWKI: t = t.replace(a, b)
    t = jednostki(t)
    t = re.sub(r'(\d)\.(\d)(?=\s?(?:″|"|cala|cali))', r'\1,\2', t)
    t = re.sub(r',(?=[^\d\s])', ', ', t)
    t = re.sub(r'\s+([.,!?;:)])', r'\1', t)
    t = re.sub(r'\(\s+', '(', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    return t

YT_TYT = {}
def tokeny(el, fmt, out):
    for c in el.children:
        if isinstance(c, NavigableString):
            if c.__class__.__name__ in ('Comment', 'Doctype'): continue
            s = str(c).replace('\n', ' ')
            if s: out.append(('t', s, frozenset(fmt)))
            continue
        if not isinstance(c, Tag): continue
        n = c.name
        if n == 'br': out.append(('br',)); continue
        if n == 'img':
            out.append(('img', c.get('src', ''), c.get('width'))); continue
        if n == 'iframe':
            m = re.search(r'embed/([\w-]{11})', c.get('src', ''))
            if m: out.append(('yt', m.group(1), c.get('title', ''))); continue
        if n in ('p', 'div') and out: out.append(('br',))
        f = set(fmt)
        if n in ('strong', 'b'): f.add('b')
        if n in ('del', 's'): f.add('del')
        if n in ('em', 'i'): f.add('i')
        st = c.get('style', '') or ''
        if re.search(r'color:\s*#(?:ff0000|e10000|f00\b)', st, re.I): f.add('red')
        if n == 'a' and c.get('href'): f = {x for x in f if not x.startswith('a=')}; f.add('a=' + c['href'])
        tokeny(c, f, out)
        if n in ('p', 'div'): out.append(('br',))

def linia_html(toks, sl_url):
    """tokeny tekstu jednej linii -> (html, tekst, cala_pogrubiona, czerwona)"""
    czesci = []; txt = ''; bold_txt = ''; red = False
    for _, s, f in toks:
        txt += s
        if 'b' in f: bold_txt += s
        if 'red' in f: red = True
        czesci.append((s, f))
    # sklej sasiednie fragmenty o tym samym formacie
    sc = []
    for s, f in czesci:
        if sc and sc[-1][1] == f: sc[-1] = (sc[-1][0] + s, f)
        else: sc.append((s, f))
    wy = ''
    for s, f in sc:
        s = tekst_popraw(s)
        h = E(s)
        if 'b' in f and s.strip(): h = re.sub(r'^(\s*)(.*?)(\s*)$', r'\1<strong>\2</strong>\3', h, flags=re.S)
        if 'del' in f and s.strip(): h = f'<del>{h}</del>'
        a = [x for x in f if x.startswith('a=')]
        if a:
            href = a[0][2:]
            if href in PERM and PERM[href] in sl_url:
                sl, nz = sl_url[PERM[href]]
                href = '../' + sl + '/'
                if 'aquaholm.pl' in s: h = E(nz)
            elif 'aquaholm.pl' in href: h = re.sub(r'\s*\|\s*aquaholm\.pl', '', h)
            h = f'<a href="{E(href)}">{h}</a>'
        wy += h
    wy = re.sub(r'</strong>(\s*)<strong>', r'\1', wy)
    wy = re.sub(r'\s+', ' ', wy).strip()
    t = re.sub(r'\s+', ' ', tekst_popraw(txt)).strip()
    cala_b = len(re.sub(r'\W', '', bold_txt)) >= max(1, len(re.sub(r'\W', '', txt)) - 1)
    return wy, t, cala_b, red

ZN_LISTY = re.compile(r'^\s*(?:<strong>\s*)?(?:&gt;|–|-|•|\d{1,2}\.)\s*(?:</strong>\s*)?')
def rownowaz(h):
    # usuwa niesparowane </strong>/</del> i domyka otwarte znaczniki
    wy = []; st = []
    for cz in re.split(r'(</?(?:strong|del)>)', h):
        m = re.match(r'<(/?)(strong|del)>$', cz)
        if not m: wy.append(cz); continue
        if not m.group(1):
            if m.group(2) in st: continue          # zagniezdzone to samo
            st.append(m.group(2)); wy.append(cz)
        elif st and st[-1] == m.group(2): st.pop(); wy.append(cz)
    wy += [f'</{t}>' for t in reversed(st)]
    h = ''.join(wy)
    h = re.sub(r'<(strong|del)>\s*</\1>', ' ', h)
    return re.sub(r'\s+', ' ', h).strip()

def nowosc(h):
    h = re.sub(r'\s*(?:–|-)?\s*(?:<strong>)?\s*NOWOŚĆ!\s*(?:</strong>)?', ' <span class="nw">Nowość</span>', h)
    h = re.sub(r'\s*(?:<strong>)?\s*GRATIS!?\s*(?:</strong>)?(?=\s|$|<)', lambda m: ' <strong>gratis</strong>' if 'strong' not in m.group(0) else ' <strong>gratis</strong>', h)
    return rownowaz(h.replace('<strong>gratis</strong></strong>', 'gratis</strong>'))

def kv(t):
    m = re.match(r'^([^:]{2,48}):\s*(.+)$', t)
    return (m.group(1).strip(), m.group(2).strip()) if m and not re.search(r'https?$', m.group(1)) else None

def pasek_ikon():
    # korzysci zakupu (tresc klienta), wlasne ikony w stylu treg: kwadrat z logo, grafit + niebieski/czerwony
    ik = [('<path d="M8 16 16 8"/><rect x="6" y="6.5" width="3.5" height="3.5"/><rect x="14.5" y="14" width="3.5" height="3.5"/>', 'Promocja'),
          ('<path d="M12 3.5 5 6v5.5c0 4.2 2.9 7.6 7 9 4.1-1.4 7-4.8 7-9V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>', 'Gwarancja najniższej ceny lub zwrot różnicy'),
          ('<rect x="3.5" y="5.5" width="17" height="13"/><path d="M3.5 9.5h17"/><path d="M7 15h4"/><text x="16.4" y="16.4" text-anchor="middle" font-size="5.6" font-weight="800" fill="currentColor" stroke="none" font-family="Archivo,Arial,sans-serif">0%</text>', 'Zakupy na raty 0%, RRSO 0%'),
          ('<path d="M2.5 7h11v9h-11z"/><path d="M13.5 10h4l3 3v3h-7"/><rect x="4.5" y="15.5" width="3" height="3"/><rect x="15.5" y="15.5" width="3" height="3"/>', 'Darmowa dostawa'),
          ('<path d="M4 9.5 12 5l8 4.5v9L12 23l-8-4.5z" transform="translate(0 -2)"/><path d="M4 7.5 12 12l8-4.5M12 12v9"/>', 'Wygodna dostawa'),
          ('<rect x="3.5" y="5" width="17" height="15.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/><text x="12" y="18.3" text-anchor="middle" font-size="6.6" font-weight="800" fill="currentColor" stroke="none" font-family="Archivo,Arial,sans-serif">30</text>', 'Kup teraz, zapłać za 30 dni z PayPo')]
    return '<ul class="ikony" aria-label="Korzyści zakupu">' + ''.join(
        f'<li><span class="ik"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="miter" aria-hidden="true">{sv}</svg></span><span>{E(t)}</span></li>' for sv, t in ik) + '</ul>'

def opis_html(o, sl_url, alt):
    soup = BeautifulSoup(o['opis_html'], 'html.parser')
    toks = []
    tokeny(soup, set(), toks)
    toks.append(('br',))
    # podzial na bloki: linie tekstu, obrazy, filmy; granica akapitu = podwojny br albo element blokowy
    wiersze = []; biez = []
    for t in toks:
        if t[0] == 't': biez.append(t); continue
        if biez and ''.join(x[1] for x in biez).strip(): wiersze.append(('l', biez))
        biez = []
        if t[0] == 'br': wiersze.append(('br',))
        else: wiersze.append(t)
    # akapit = ciag linii bez pustej linii pomiedzy (podwojny br) i bez obrazow
    out = []; poprz = None; nr_l = 0; img_rzad = []; yt_n = 0; galeria = []
    def zamknij_img():
        nonlocal img_rzad
        if img_rzad:
            out.append(('img', img_rzad)); img_rzad = []
    pusty = 0
    for w in wiersze:
        if w[0] == 'br':
            zamknij_img()
            pusty += 1
            if pusty >= 2: nr_l = 0
            continue
        if w[0] == 'img':
            src = w[1]
            if 'promocja-2-' in src: zamknij_img(); out.append(('ikony',)); pusty = 0; continue
            if 'texland.pl' in src and 'promocja' in src: zamknij_img(); out.append(('promo',)); pusty = 0; continue
            if src not in MAPA: continue
            img_rzad.append((src, w[2])); pusty = 0; nr_l = 0; continue
        zamknij_img()
        if w[0] == 'yt':
            out.append(('yt', w[1], w[2])); pusty = 0; nr_l = 0; continue
        h, t, cb, red = linia_html(w[1], sl_url)
        if not t: continue
        if pusty >= 2 or poprz is None: nr_l = 0
        out.append(('l', h, t, cb, red, nr_l)); nr_l += 1; pusty = 0
        poprz = w
    zamknij_img()
    # klasyfikacja linii
    el = []
    for i, x in enumerate(out):
        if x[0] != 'l': el.append(x); continue
        _, h, t, cb, red, nr = x
        nast = out[i + 1] if i + 1 < len(out) else None
        nast_l = nast and nast[0] == 'l' and nast[5] > nr
        if ZN_LISTY.match(h) and not re.match(r'^\d+\s*[x×]', t):
            hh = ZN_LISTY.sub('', h, count=1).strip()
            tt = re.sub(r'^(?:>|–|-|•|\d{1,2}\.)\s*', '', t).strip()
            el.append(('li', nowosc(hh), tt, red, bool(re.match(r'^\d{1,2}\.', t)))); continue
        if nr == 0 and len(t) <= 120 and (cb or caps(t) or (nast_l and len(t) <= 40 and not re.search(r'[.!?:]$', t))) and not kv(t):
            hh = zdanie(E(re.sub(r'<[^>]+>', '', H.unescape(h)))) if caps(t) else re.sub(r'</?strong>', '', h)
            el.append(('h', hh.strip().rstrip(':').strip(), red)); continue
        if caps(t) and len(t) <= 90:
            hh = zdanie(re.sub(r'<[^>]+>', '', H.unescape(h)))
            el.append(('p', nowosc(f'<strong>{E(hh)}</strong>' if cb else E(hh)), t, red)); continue
        el.append(('p', nowosc(h), t, red))
    # skladanie HTML
    html = []; i = 0
    def wiersz_kv(t, h):
        a, b = kv(t)
        if caps(a) or (a.isupper() and len(a) >= 3): a = zdanie(a)
        if caps(b): b = zdanie(b)
        hb = h.split(':', 1)[1].strip() if ':' in h else E(b)
        hb = re.sub(r'^</strong>\s*', '', hb)
        if caps(re.sub(r'<[^>]+>', '', hb)): hb = E(b)
        hb = re.sub(r'^(<strong>)?\s*', r'\1', hb)
        if hb.count('<strong>') != hb.count('</strong>'): hb = re.sub(r'</?strong>', '', hb)
        a = a[:1].upper() + a[1:]
        return f'<tr><th scope="row">{E(a)}</th><td>{nowosc(hb)}</td></tr>'
    while i < len(el):
        x = el[i]
        if x[0] in ('li', 'p'):
            # ciag elementow tego samego typu
            j = i
            while j < len(el) and el[j][0] == x[0] and el[j][3] == x[3]: j += 1
            grp = el[i:j]
            red = x[3]
            kvs = [kv(re.sub(r'\s+', ' ', g[2])) for g in grp]
            if len(grp) >= 3 and all(kvs) and all(len(k[1]) <= 70 for k in kvs):
                blok = '<table class="par"><tbody>' + ''.join(wiersz_kv(g[2], g[1]) for g in grp) + '</tbody></table>'
            elif x[0] == 'li':
                tag = 'ol' if all(g[4] for g in grp) else 'ul'
                blok = f'<{tag} class="ol">' + ''.join(f'<li>{g[1]}</li>' for g in grp) + f'</{tag}>'
            else:
                # akapity, ale ciagi >=3 linii klucz: wartosc w srodku -> tabela
                blok = ''; k = 0
                while k < len(grp):
                    m = k
                    while m < len(grp) and kvs[m] and len(kvs[m][1]) <= 70: m += 1
                    if m - k >= 3:
                        blok += '<table class="par"><tbody>' + ''.join(wiersz_kv(g[2], g[1]) for g in grp[k:m]) + '</tbody></table>'; k = m
                    else:
                        blok += f'<p>{grp[k][1]}</p>'; k += 1
            if red: blok = f'<div class="wyr">{blok}</div>'
            html.append(blok); i = j; continue
        if x[0] == 'h':
            html.append(f'<h3{" class=\"red\"" if x[2] else ""}>{nowosc(x[1])}</h3>'); i += 1; continue
        if x[0] == 'ikony': html.append(pasek_ikon()); i += 1; continue
        if x[0] == 'promo': html.append('<p class="promo">Promocja</p>'); i += 1; continue
        if x[0] in ('yt', 'img'):
            # zdjecia, rysunki i filmy stojace obok siebie -> rowna siatka po 2 w rzedzie
            kom = []
            while i < len(el) and el[i][0] in ('yt', 'img'):
                y = el[i]
                if y[0] == 'yt':
                    yid, tyt = y[1], (zdanie(y[2]) if caps(y[2]) else y[2])
                    p = obraz_yt(yid)
                    kom.append(f'<figure class="mk mf"><button class="fa" type="button" data-yt="{yid}" aria-label="Odtwórz film: {E(tyt)}">'
                               f'<img src="../img/o/{p[0]}" width="{p[1]}" height="{p[2]}" loading="lazy" decoding="async" alt=""><span class="od" aria-hidden="true"></span></button></figure>')
                else:
                    for src, w in y[1]:
                        n, sw, sh = obraz(src)
                        kom.append(f'<figure class="mk"><button type="button" class="oi" data-lb="../img/o/{n}" aria-label="Powiększ zdjęcie">'
                                   f'<img src="../img/o/{n}" width="{sw}" height="{sh}" style="max-width:min(100%,{sw}px);max-height:min(100%,{sh}px)" loading="lazy" decoding="async" alt="{E(alt)}"></button></figure>')
                i += 1
            html.append(f'<div class="siatka{" jeden" if len(kom) == 1 else ""}">' + ''.join(kom) + '</div>'); continue
        i += 1
    return '\n'.join(html)

def obraz_yt(yid):
    for q in ('maxresdefault', 'hqdefault'):
        u = f'https://i.ytimg.com/vi/{yid}/{q}.jpg'
        if u in MAPA:
            k = u + '#yt'
            if k in OBR: return OBR[k]
            from PIL import Image
            im = Image.open(RAW + MAPA[u]).convert('RGB')
            w, h = im.size
            if q == 'hqdefault':                     # 480x360 z czarnymi pasami -> kadr 16:9
                im = im.crop((0, 45, 480, 315)); w, h = im.size
            if w > 960: im = im.resize((960, round(h * 960 / w)), Image.LANCZOS)
            n = f'yt-{yid}.webp'
            im.save('img/o/' + n, 'WEBP', quality=80, method=6)
            OBR[k] = (n, im.size[0], im.size[1]); return OBR[k]
    raise SystemExit('brak okladki ' + yid)

CSS = '''
.kp .podt{display:block;margin-top:6px;font-size:clamp(17px,1.1vw,19px);color:var(--mut);line-height:1.4}
.gl2{min-width:0}
.gl2 .duze-w{position:relative;background:#fff;border:1px solid var(--line)}
.gl2 .duze{display:flex;align-items:center;justify-content:center;width:100%;min-height:clamp(260px,34vw,600px);border:0;padding:0;background:#fff;cursor:zoom-in}
.gl2 .duze img{display:block;width:auto;max-width:100%;height:auto;max-height:min(72vh,640px);object-fit:contain}
.gl2 .gp,.gl2 .gn{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border:0;background:rgba(30,33,36,.78);color:#fff;font-size:26px;line-height:1;cursor:pointer;display:grid;place-items:center}
.gl2 .gp{left:8px}.gl2 .gn{right:8px}
.gl2 .gp:hover,.gl2 .gn:hover{background:#1e2124}
.gl2 .licz{position:absolute;right:10px;bottom:10px;background:rgba(255,255,255,.92);padding:3px 9px;font-size:.88rem;font-weight:700;color:var(--ink)}
.gl2 .mini2{display:flex;gap:8px;margin-top:10px;overflow-x:auto;scroll-snap-type:x proximity;padding-bottom:6px;scrollbar-width:thin}
.gl2 .mini2 button{flex:none;width:76px;height:76px;padding:3px;border:2px solid var(--line);background:#fff;cursor:pointer;scroll-snap-align:start}
.gl2 .mini2 button img{width:100%;height:100%;object-fit:contain}
.gl2 .mini2 button[aria-current="true"]{border-color:var(--ink)}
.zak .cena small{font-size:.9rem;color:var(--mut);font-weight:600;margin-left:6px}
.zak .ean{margin-top:12px;color:var(--mut);font-size:.95rem}
.odz{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:8px}
.odz li{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#f4fbf7;border:1px solid #c2ebd5;color:#1a6e3f;font-weight:700;font-size:.98rem}
.odz svg{flex:none}
.zak .meta{margin-top:18px;padding-top:14px;border-top:1px solid var(--line);font-size:.93rem;color:var(--mut);line-height:1.6}
.zak .meta a{color:var(--mut)}
.pods{padding:clamp(26px,3vw,48px) 0;background:var(--g)}
.pods h2{font-size:clamp(24px,1.8vw,32px)}
.pods .sg{display:flex;justify-content:space-between;align-items:end;gap:16px}
.ptor{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(240px,calc((100% - 3*20px)/4));gap:20px;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;margin-top:18px;padding-bottom:8px;scrollbar-width:thin}
.pk{scroll-snap-align:start;background:#fff;border:1px solid #dfe4e9;display:flex;flex-direction:column}
.pk .f{display:block;aspect-ratio:1;background:#fff}.pk .f img{width:100%;height:100%;object-fit:contain}
.pk .in{padding:12px 14px 14px;display:flex;flex-direction:column;flex:1;gap:6px}
.pk h3{font-size:1.08rem;line-height:1.35;font-weight:700;font-stretch:100%;letter-spacing:0}.pk h3 a{color:var(--ink);text-decoration:none}.pk h3 a:hover{text-decoration:underline}
.pk .cz{margin-top:auto;font-size:.88rem;color:var(--mut)}
.pk .c{font-weight:800;font-size:1.3rem}.pk .c s{font-weight:500;color:var(--mut);font-size:.9rem;margin-left:6px}
.pods .nav button{width:48px;height:48px}
.opis-s{padding:clamp(30px,4vw,64px) 0 clamp(50px,6vw,90px)}
.opis-s h2{font-size:clamp(26px,2vw,36px)}
.opis-s .info-h{margin-top:clamp(40px,4vw,64px);font-size:clamp(26px,2vw,36px)}.info-t{margin-top:14px;max-width:900px}
.opis{margin-top:10px}
.opis p,.opis li{text-align:justify;hyphens:auto;-webkit-hyphens:auto}
.siatka{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(14px,1.4vw,24px);margin-top:20px}
.siatka.jeden{grid-template-columns:minmax(0,1fr);max-width:calc(50% - 12px);margin-left:auto;margin-right:auto}
.siatka .mk{margin:0;aspect-ratio:16/10;background:#fff;border:1px solid var(--line);overflow:hidden;position:relative}
.siatka .oi{display:flex;align-items:center;justify-content:center;width:100%;height:100%;border:0;padding:0;background:#fff;cursor:zoom-in}
.siatka .oi img{width:auto;height:auto;object-fit:contain;transition:transform .45s ease}
.siatka .mf{background:#0b0e11}.siatka .fa{width:100%;height:100%;aspect-ratio:auto}
.siatka .fa img{transition:transform .45s ease,opacity .2s}
.siatka .fa iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
@media (hover:hover){.siatka .mk:hover .oi img{transform:scale(1.18)}.siatka .mk:hover .fa img{transform:scale(1.08)}}
@media (prefers-reduced-motion:reduce){.siatka img{transition:none}}
@media (max-width:640px){.siatka{grid-template-columns:minmax(0,1fr)}.siatka.jeden{max-width:none}}
.opis p,.opis li{line-height:1.65}
.opis p{margin-top:12px}
.opis h3{font-size:clamp(20px,1.35vw,25px);margin-top:clamp(32px,3vw,48px);padding-top:clamp(20px,2vw,28px);border-top:1px solid var(--line)}
.opis h3:first-child{margin-top:18px;border-top:0;padding-top:0}
.opis h3.red,.opis .wyr{color:#b3120e}
.opis .wyr{background:#fff4f3;border-left:4px solid #d7140f;padding:6px 18px 16px;margin-top:16px}
.opis .wyr p:first-child{margin-top:10px}
.opis .ol{margin:12px 0 0;padding-left:0;list-style:none}
.opis ol.ol{counter-reset:o}
.opis .ol li{position:relative;padding:7px 0 7px 28px;border-bottom:1px solid #eef1f4}
.opis .ol li:last-child{border-bottom:0}
.opis ul.ol li::before{content:"";position:absolute;left:4px;top:1.05em;width:8px;height:8px;background:var(--ink)}
.opis ol.ol li{counter-increment:o}.opis ol.ol li::before{content:counter(o) ".";position:absolute;left:0;top:7px;font-weight:800}
.opis .par{margin-top:14px;width:100%;max-width:none}
.opis .par th{width:42%}
.opis .nw{display:inline-block;margin-left:6px;padding:1px 7px;background:#d7140f;color:#fff;font-size:.74rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;vertical-align:.12em;border-radius:2px}
.opis .of-z{display:flex;flex-direction:column;align-items:center;gap:14px;margin-top:18px}
.opis .of-z.rz{flex-direction:row;flex-wrap:wrap;justify-content:center}
.opis .oi{display:block;width:100%;border:0;padding:0;background:none;cursor:zoom-in}
.opis .of-z.rz{flex-wrap:nowrap;align-items:flex-start}.opis .of-z.rz .oi{flex:1 1 0;min-width:0}
.opis .oi img{display:block;width:100%;height:auto;margin:0 auto}
.opis .film.of{width:100%;margin:18px 0 0}
.opis .film.of figcaption{color:var(--mut);font-size:.93rem;margin-top:8px}
.opis .promo{display:inline-block;margin-top:16px;padding:6px 16px;background:#d7140f;color:#fff;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.ikony{list-style:none;margin:6px 0 0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px}
.ikony li{position:relative;display:flex;align-items:center;gap:14px;padding:16px 16px 16px 14px;background:#fff;border:1px solid var(--line);border-top:3px solid var(--aq);font-weight:700;font-size:.95rem;line-height:1.3;text-align:left;color:var(--ink)}
.ikony li:nth-child(even){border-top-color:var(--apv)}
.ikony .ik{flex:none;position:relative;display:grid;place-items:center;width:52px;height:52px;background:var(--ink);color:#fff}
.ikony .ik::before{content:"";position:absolute;left:-6px;top:-6px;width:20px;height:20px;border:2.5px solid var(--aq);background:#fff;z-index:-1}
.ikony li:nth-child(even) .ik{background:var(--apv)}.ikony li:nth-child(even) .ik::before{border-color:var(--ink)}
.ikony li{z-index:0}
@media (max-width:1400px){.ikony{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:1100px){.ptor{grid-auto-columns:minmax(220px,calc((100% - 2*20px)/3))}}
@media (max-width:640px){.ptor{grid-auto-columns:84%}.opis .of-z.rz{flex-wrap:wrap}.ikony{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.ikony li{flex-direction:column;align-items:flex-start;gap:10px;padding:12px;font-size:.88rem}.ikony .ik{width:42px;height:42px}.ikony .ik svg{width:24px;height:24px}.gl2 .gp,.gl2 .gn{width:44px;height:44px}.gl2 .mini2 button{width:64px;height:64px}.opis .of-z.rz .oi{flex:1 1 100%}}
'''
