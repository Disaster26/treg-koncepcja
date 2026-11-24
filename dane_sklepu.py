# Przygotowuje produkty.json dla sklepu treg.pl z danych aquaholm.pl (WooCommerce Store API, /wp-json/wc/store/v1/products).
# Wg klienta (20.11.2026) obowiazuja nazwy i ceny z aquaholm.pl. Uzycie: python dane_sklepu.py <aquaholm.pl.json> <zdjecia.json>
import json, re, sys, html, unicodedata

src = json.load(open(sys.argv[1], encoding='utf-8'))
zdj = json.load(open(sys.argv[2], encoding='utf-8'))

def linie(h):
    h = re.sub(r'<br\s*/?>', '\n', h)
    h = re.sub(r'</p>|</li>|</h\d>|</tr>', '\n', h)
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h).replace('\xa0', ' ').replace('″', '"')
    return [re.sub(r'\s+', ' ', l).strip() for l in h.split('\n') if l.strip()]

def slug(t):
    t = t.replace('ł', 'l').replace('Ł', 'L')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

NAGL_MIESZ = {'cechy wyróżniające', 'opis techniczny', 'amortyzacja', 'galeria zdjęć', 'zestaw promocyjny'}
def sekcje(ls):
    out, cur = {}, '_start'
    for l in ls:
        bez = l.rstrip('!:').strip()
        if (l.endswith(':') and bez.lower() in ('akcesoria', 'opis funkcji', 'materiał wykonania')) or (bez.lower() in NAGL_MIESZ) or (len(bez) < 60 and bez == bez.upper() and re.search(r'[A-ZĄĆĘŁŃÓŚŹŻ]{4}', bez) and not l.startswith(('>', '–', '-'))):
            cur = bez.lower(); out.setdefault(cur, []); continue
        out.setdefault(cur, []).append(l)
    return out

def czysc(l):
    l = re.sub(r'^[>–\-•]\s*', '', l)
    l = re.sub(r'\s*[–-]\s*NOWOŚĆ!?', '', l)
    l = re.sub(r'\s*NOWOŚĆ!?', '', l)
    l = re.sub(r'\((?:możliwość|oświetlenie prezentujemy|suma)[^)]*\)', '', l)
    l = re.sub(r',?\s*certyfikat TUV, CE\)?', '', l)
    l = re.sub(r'\s+', ' ', l).strip(' ,;')
    l = re.sub(r'\s*\($', '', l).strip(' ,;')
    if l.count('(') > l.count(')'): l += ')'
    return l[:1].upper() + l[1:] if l else l

def liczba(t, wz):
    m = re.search(wz, t, re.I); return m.group(1) if m else None

def cena(v): return int(v) // 100

def dostepnosc(p):
    t = (p.get('stock_availability') or {}).get('text', '') or ''
    if not p['is_in_stock']: return 'brak'
    if 'zamówienie' in t.lower(): return 'zam'
    return 'jest'

produkty = []
for p in src:
    nazwa0 = html.unescape(p['name'])
    opis = linie(p['description'])
    caly = ' '.join(opis)
    sek = sekcje(opis)
    d = dict(id=p['id'], zrodlo=p['permalink'], nazwa_zrodlo=nazwa0, cena=cena(p['prices']['price']),
             stara=cena(p['prices']['regular_price']), dost=dostepnosc(p), sku=p['sku'],
             zdjecia=zdj.get(str(p['id']), []))
    if d['stara'] <= d['cena']: d['stara'] = None
    ean = liczba(re.sub('<[^>]+>', ' ', p['short_description']) + ' ' + caly, r'EAN\s*:?\s*(\d{13})')
    d['ean'] = ean
    d['realizacja30'] = 'Czas realizacji: 30 dni' in nazwa0 or 'Czas realizacji: 30 dni' in caly
    n = nazwa0.lower()
    if 'wanna' in n:
        d['typ'] = 'wanna'
        kod = liczba(nazwa0, r'\b(A?9\d{3}[A-Z]?)\b')
        wym = re.search(r'(\d+)\s*cm\s*x\s*(\d+)\s*cm\s*x\s*(\d+)\s*cm', nazwa0)
        d['kod'] = kod; d['wym'] = [int(x) for x in wym.groups()]
        d['ksztalt'] = 'narozna' if 'narożna' in n else ('podwojna' if 'podwójna' in n else 'prostokatna')
        d['kolor'] = 'czarna' if 'czarna' in n else 'biala'
        pref = {'narozna': 'Wanna narożna', 'podwojna': 'Podwójna wanna', 'prostokatna': 'Wanna'}[d['ksztalt']]
        if d['kolor'] == 'czarna':
            pref = {'narozna': 'Czarna wanna narożna', 'podwojna': 'Podwójna czarna wanna', 'prostokatna': 'Czarna wanna'}[d['ksztalt']]
        d['nazwa'] = f'{pref} z hydromasażem {kod} {d["wym"][0]} x {d["wym"][1]} x {d["wym"][2]} cm'
        d['krotka'] = f'{pref} {kod} Premium Line'
        d['slug'] = slug(f'{pref} z hydromasazem {kod} {d["wym"][0]}x{d["wym"][1]}')
        d['cechy_n'] = {k: (k in n or k in caly.lower()) for k in ('bluetooth', 'usb', 'pilot', 'wodospad', 'podgrzewacz', 'radio', 'ozon', 'samoosusz', 'led rgb', 'dysze obrotowe')}
        d['dysze_pow'] = liczba(caly, r'dysz powietrznych\s*[–-]\s*(\d+)') or liczba(caly, r'\((\d+) nowoczesnych wielokolorowych dysz')
        d['dysze_wod'] = liczba(caly, r'dysz wodnych\s*[–-]\s*(\d+)') or liczba(caly, r'masaż wodny \((\d+) dużych')
        d['dysze_plecy'] = liczba(caly, r'na plecy\s*[–-]\s*po\s*(\d+)') or liczba(caly, r'(\d+) dysze do masażu pleców')
        d['pompa_pow'] = liczba(caly, r'pompy powietrznej\s*[–-]\s*(\d+)\s*W') or liczba(caly, r'pompa powietrza o mocy (\d+)\s*W')
        d['pompa_wod'] = liczba(caly, r'pompy wodnej\s*[–-]\s*(\d+)\s*W')
        d['grzalka'] = liczba(caly, r'podgrzewacza wody\s*[–-]\s*(\d+)\s*W') or liczba(caly, r'podgrzewacz wody (\d+)\s*W')
        d['pojemnosc'] = liczba(caly, r'pojemność\s*:?\s*(\d+)')
        d['wyroznienia'] = [czysc(l) for l in sek.get('cechy wyróżniające', []) if l.startswith('>')]
        d['funkcje'] = [czysc(l) for l in sek.get('opis funkcji', []) if l.startswith(('>', '–'))]
        d['akcesoria'] = [czysc(l) for l in sek.get('akcesoria', []) if l.startswith(('>', '–'))]
        d['material'] = ' '.join(sek.get('materiał wykonania', []))
        d['elektryka'] = [tuple(x.strip() for x in czysc(l).split(':', 1)) for l in sek.get('parametry elektryczne', []) if ':' in l]
    elif 'bieżnia' in n and not n.startswith(('mata', 'zestaw', 'pas piersiowy')):
        d['typ'] = 'bieznia'
        m = re.search(r'APV(8000|6000|5000|900|600)(\s*S\b)?', nazwa0)
        model = 'APV' + m.group(1); s_wersja = bool(m.group(2))
        seria = liczba(nazwa0, r'SERIA\s+(FUTURA PRESTIGE|TOP QUALITY|PREMIUM LINE)')
        moc = liczba(nazwa0, r'(\d)\s*KM')
        kom = 'KOMERCYJNA' in nazwa0
        zestaw = 'dodatkowe wyposażenie' in n
        if model == 'APV8000':
            ser = seria.title()
            d['nazwa'] = f'Bieżnia elektryczna {model} {ser} {moc} KM' + (', wersja komercyjna' if kom else '')
            d['krotka'] = f'Bieżnia {model} {ser} {moc} KM' + (' komercyjna' if kom else '')
        else:
            d['nazwa'] = f'Bieżnia elektryczna {model}{" S" if s_wersja else ""}' + (' z zestawem dodatków' if zestaw else '')
            d['krotka'] = f'Bieżnia {model}{" S" if s_wersja else ""}' + (' z zestawem dodatków' if zestaw else '')
        d['model'] = model; d['seria'] = seria.title() if seria else None; d['komercyjna'] = kom; d['zestaw'] = zestaw
        d['slug'] = slug(d['krotka'])
        tech = []
        for l in sek.get('opis techniczny', []) + sek.get('_start', []):
            if ':' in l and len(l) < 120 and not l.lower().startswith(('czas realizacji', 'grupa')):
                k, v = [x.strip() for x in l.split(':', 1)]
                if k and v and k.lower() not in [t[0].lower() for t in tech]: tech.append((k[:1].upper() + k[1:], v))
        d['tech'] = tech
        d['ekran'] = liczba(nazwa0 + ' ' + caly, r'(\d+[.,]\d)\s*(?:"|cala|cali)') or liczba(nazwa0 + ' ' + caly, r'ekran[^.]{0,30}?(\d+)\s*(?:"|cala|cali)')
        d['ekran_lcd'] = 'ekran LCD' in nazwa0
        d['pas'] = liczba(nazwa0 + ' ' + caly, r'(\d{3}\s*x\s*\d{2})\s*cm')
        d['moc'] = liczba(caly, r'Moc silnika:\s*([^\n]+?)(?:Prędkość|$)')
        d['wyroznienia'] = [czysc(l) for l in sek.get('cechy wyróżniające', []) if l.startswith(('–', '-'))]
        d['gratisy'] = 'gratisy' in sek or 'GRATIS' in caly
        d['pas_opcja'] = 'zestaw promocyjny' in sek
        d['amortyzacja'] = 'amortyzacja' in sek
        d['aplikacje'] = [a for a in ('Kinomap', 'Zwift', 'FitShow') if a.lower() in caly.lower()]
    else:
        d['typ'] = 'akcesorium'
        if n.startswith('mata'): d['nazwa'] = 'Mata wygłuszająca APVsport pod bieżnię 175 x 75 cm'; d['krotka'] = 'Mata wygłuszająca pod bieżnię'
        elif 'pas piersiowy' in n: d['nazwa'] = 'Pas piersiowy do pomiaru tętna'; d['krotka'] = d['nazwa']
        else: d['nazwa'] = 'Zestaw dodatków do bieżni APV8000'; d['krotka'] = d['nazwa']
        d['slug'] = slug(d['nazwa'])
        d['opis'] = [l for l in opis if not l.startswith(('–', '>')) and l.lower() not in NAGL_MIESZ and len(l) > 40]
        d['wyroznienia'] = [czysc(l) for l in sek.get('cechy wyróżniające', []) if l.startswith(('–', '-'))] or [czysc(l) for l in opis if l.startswith('–')]
    if d['dost'] == 'jest' and d['realizacja30']: d['dost'] = 'zam'
    if p['id'] == 20185: d['slug'] = 'bieznia-apv8000-futura-prestige-6km'  # wzorcowa karta (produkt.py)
    produkty.append(d)

sl = [p['slug'] for p in produkty]
assert len(sl) == len(set(sl)), [s for s in sl if sl.count(s) > 1]
json.dump(produkty, open('produkty.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for p in produkty: print(p['typ'], p['slug'], '|', p['nazwa'], p['cena'], p['dost'], len(p['zdjecia']))
