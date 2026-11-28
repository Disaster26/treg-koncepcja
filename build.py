# Buduje index.html z src.html: logo TREG (SVG), znak Wylinki (oficjalny fragment), karty produktow, filmy.
# Nazwy, ceny i dostepnosc wanien i biezni z aquaholm.pl (Store API) - wg klienta obowiazujace, sprawdzone 20.11.2026.
import html as H
s = open('src.html', encoding='utf-8').read()

def logo(tekst):
    # przerysowane logo treg.pl: kwadrat obrysowany + kwadrat pelny + napis "treg"; kwadraty w kolorach marek
    return (f'<svg viewBox="0 0 196 60" role="img" aria-label="TREG"><rect x="4" y="5" width="28" height="28" fill="none" stroke="#027FD1" stroke-width="3.4"/>'
            f'<rect x="15" y="16" width="27" height="27" fill="#D7140F"/>'
            f'<text x="54" y="44" fill="{tekst}" font-family="Archivo,Arial,sans-serif" font-size="47" font-weight="500" letter-spacing="5">treg</text></svg>')
s = s.replace('{{LOGO}}', logo('#4A4A4A')).replace('{{LOGO_JASNE}}', logo('#FFFFFF'))
s = s.replace('{{BADGE_STYLE}}', open('badge_style.part', encoding='utf-8').read().replace('<style>', '').replace('</style>', ''))
s = s.replace('{{BADGE_LINK}}', open('badge_link.part', encoding='utf-8').read().strip())

import json
PROD = {p['id']: p for p in json.load(open('produkty.json', encoding='utf-8'))}
KARTY = {'w9014': 19555, 'w9011': 17916, 'w8008': 17905, 'w8008c': 19099, 'w9001': 17827,
         'futura': 20185, 'premium': 20175, 'top': 20183, 'apv6000': 20272, 'apv5000': 20270, 'apv900': 20233}
ZAM = ('zam', 'Na zamówienie, realizacja 30 dni')
JEST = ('jest', 'Dostępna')
BRAK = ('brak', 'Brak w magazynie')

# (plik, ile zdjec, szer. duza, szer. mala, nazwa, opis, cena, stara, dostepnosc, alt)
WANNY = [
    ('w9014', 4, 1200, 600, 'Wanna A9014 Premium Line', '170 x 80 x 58 cm, dysze obrotowe, podgrzewacz wody, wodospad, Bluetooth, pilot', '6 990', '10 900', JEST, 'Wanna z hydromasażem A9014 z przeszkloną ścianką i niebieskim podświetleniem'),
    ('w9011', 3, 1200, 600, 'Wanna narożna A9011 Premium Line', '150 x 150 x 58 cm, Bluetooth, podgrzewacz wody, USB, pilot', '7 490', '11 900', JEST, 'Narożna wanna z hydromasażem A9011 z zielonym podświetleniem'),
    ('w8008', 4, 1200, 600, 'Wanna A9008 Premium Line', '180 x 120 x 59 cm, dysze obrotowe, podgrzewacz wody, wodospad, Bluetooth, pilot', '7 490', '11 900', ZAM, 'Biała prostokątna wanna z hydromasażem A9008 z podświetleniem LED'),
    ('w8008c', 4, 1200, 600, 'Czarna wanna A9008C Premium Line', '180 x 120 x 59 cm, dysze obrotowe, podgrzewacz wody, wodospad, Bluetooth, pilot', '7 490', '11 900', ZAM, 'Czarna prostokątna wanna z hydromasażem A9008C z podświetleniem LED'),
    ('w9001', 4, 1200, 600, 'Wanna A9001 Premium Line', '170 x 78 x 60 cm, dysze obrotowe, podgrzewacz wody, wodospad, Bluetooth, pilot', '6 990', '11 250', ZAM, 'Prostokątna wanna z hydromasażem A9001 z kolorowym podświetleniem'),
]
BIEZNIE = [
    ('futura', 1, 640, 360, 'Bieżnia APV8000 Futura Prestige 6 KM', 'ekran dotykowy Android 15,6", silnik 6 KM (10 KM szczytowo), pas 145 x 58 cm, do 180 kg', '4 990', '7 290', ZAM, 'Bieżnia elektryczna APVsport APV8000 Futura Prestige z ekranem 15,6 cala'),
    ('elitek', 1, 640, 360, 'Bieżnia APV8000 Elite Series 5 KM', 'ekran dotykowy Android 10,1", silnik 5 KM (8 KM szczytowo), pas 145 x 58 cm, do 160 kg', '4 790', '6 790', ZAM, 'Bieżnia elektryczna APVsport APV8000 Elite Series'),
    ('premium', 1, 640, 360, 'Bieżnia APV8000 Premium Line 6 KM', 'ekran dotykowy Android 10,1", silnik 6 KM (10 KM szczytowo), pas 145 x 58 cm, do 180 kg', '4 990', '7 290', ZAM, 'Bieżnia elektryczna APVsport APV8000 Premium Line'),
    ('top', 1, 640, 360, 'Bieżnia APV8000 Top Quality 5 KM', 'ekran dotykowy Android 10,1", silnik 5 KM (8 KM szczytowo), pas 145 x 58 cm', '4 790', '6 790', ZAM, 'Bieżnia elektryczna APVsport APV8000 Top Quality'),
    ('apv6000', 1, 640, 360, 'Bieżnia APV6000 z zestawem dodatków', 'ekran Android 10,1", pas 135 x 48 cm, w zestawie masażer, hantle, przyrząd do brzuszków, mata', '6 490', None, BRAK, 'Bieżnia elektryczna APVsport APV6000'),
    ('apv5000', 1, 640, 360, 'Bieżnia APV5000 z zestawem dodatków', 'ekran Android 7", pas 130 x 40 cm, w zestawie masażer, hantle, przyrząd do brzuszków, mata', '6 290', None, BRAK, 'Bieżnia elektryczna APVsport APV5000'),
    ('apv900', 1, 640, 360, 'Bieżnia APV900 z zestawem dodatków', 'ekran LCD, pas 130 x 38 cm, w zestawie masażer, hantle, przyrząd do brzuszków, mata', '4 385', None, BRAK, 'Bieżnia elektryczna APVsport APV900'),
]

def karta(k, n, wd, wm, nazwa, opis, cena, stara, dost, alt, kier):
    zd = []
    for i in range(1, n + 1):
        f = (lambda w: f'img/{k}-{i}-{w}.webp') if n > 1 else (lambda w: f'img/{k}-{w}.webp')
        a = 'src' if i == 1 else 'data-src'
        zd.append(f'<button class="zd" type="button" data-lb="{f(wd)}" aria-label="Powiększ zdjęcie {i} z {n}">'
                  f'<img {a}="{f(wm)}"{f' srcset="{f(wm)} {wm}w, {f(wd)} {wd}w" sizes="(max-width:600px) 84vw, (max-width:1000px) 56vw, (max-width:1280px) 34vw, 26vw"' if i == 1 else ''} width="600" height="450" loading="lazy" decoding="async" alt="{H.escape(alt)}{"" if i == 1 else f", zdjęcie {i}"}"></button>')
    kropki = ''.join(f'<i{" class=on" if i == 0 else ""}></i>' for i in range(n)) if n > 1 else ''
    strz = '<span class="gs"><button type="button" class="gp" aria-label="Poprzednie zdjęcie"></button><button type="button" class="gn" aria-label="Następne zdjęcie"></button></span>' if n > 1 else ''
    # karta produktu w sklepie (produkty.json, dane_sklepu.py); Elite Series nie ma na aquaholm.pl
    pr = PROD.get(KARTY.get(k))
    if pr:
        dost = {'zam': ZAM, 'jest': JEST, 'brak': BRAK}[pr['dost']]
        cena = f'{pr["cena"]:,}'.replace(',', ' ')
        stara = f'{pr["stara"]:,}'.replace(',', ' ') if pr['stara'] else None
    st = f'<s>{stara} zł</s>' if stara else ''
    nz = f'<a class="pl" href="{pr["slug"]}/">{H.escape(nazwa)}</a>' if pr else H.escape(nazwa)
    if pr and dost[0] != 'brak':
        kup = (f'<button type="button" class="dok" data-kosz data-id="{pr["id"]}" data-nazwa="{H.escape(pr["nazwa"])}" data-cena="{pr["cena"]}" '
               f'data-url="{pr["slug"]}/" data-img="img/p/{pr["zdjecia"][0]["m"][0]}">Dodaj do koszyka</button>')
    elif dost[0] != 'brak':
        kup = '<a class="dok pyt" href="kontakt/">Zapytaj o bieżnię</a>'
    else:
        kup = f'<a class="dok pyt" href="{pr["slug"] + "/" if pr else "kontakt/"}">Zapytaj o termin</a>'
    return (f'<article class="prod">\n  <div class="gal" data-grupa><div class="gt">{"".join(zd)}</div>{strz}<div class="kr" aria-hidden="true">{kropki}</div></div>\n'
            f'  <div class="pin"><h3><span class="kw {kier}"></span>{nz}</h3><p class="po">{H.escape(opis)}</p>\n'
            f'  <p class="dost {dost[0]}"><span class="b" aria-hidden="true"></span>{dost[1]}</p>\n'
            f'  <p class="cena"><b>{cena} zł</b>{st}<span class="gratis">Transport gratis</span></p>{kup}</div>\n</article>')

s = s.replace('{{WANNY}}', '\n'.join(karta(*x, 'aq') for x in WANNY))
s = s.replace('{{BIEZNIE}}', '\n'.join(karta(*x, 'apv') for x in BIEZNIE))

# filmy z kanalu APVsport (osadzone na karcie APV8000 Futura Prestige w apvsport.pl); fasada: okladka + przycisk
FILMY = [
    ('r46a4RoqEwY', 'Bieżnia APV8000 Futura Prestige: przegląd'),
    ('Z4sfFoUTpzg', 'Funkcje ekranu dotykowego 15,6 cala, wersja polska'),
    ('ZPg6jSN-DGE', 'Ekran bieżni APV8000: wirtualne trasy'),
    ('3zskB507N9g', 'Jak połączyć bieżnię z aplikacją Kinomap'),
    ('J7oqwrpF1ac', 'Jak połączyć bieżnię z aplikacją Zwift'),
]
def film(i, t, duzy):
    img = (f'<img src="img/yt-{i}-960.webp" srcset="img/yt-{i}.webp 480w, img/yt-{i}-960.webp 960w" sizes="(max-width:1000px) 92vw, 55vw" width="960" height="540" loading="lazy" decoding="async" alt="">'
           if duzy else f'<img src="img/yt-{i}.webp" width="480" height="270" loading="lazy" decoding="async" alt="">')
    return (f'<figure class="film{" duzy" if duzy else ""}"><button class="fa" type="button" data-yt="{i}" aria-label="Odtwórz film: {H.escape(t)}">'
            f'{img}<span class="od" aria-hidden="true"></span></button>'
            f'<figcaption>{H.escape(t)}</figcaption></figure>')
s = s.replace('{{FILMY}}', film(*FILMY[0], True) + '\n<div class="reszta">' + ''.join(film(*f, False) for f in FILMY[1:]) + '</div>')
assert '{{' not in s
open('index.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
