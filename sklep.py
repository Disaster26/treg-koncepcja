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
.kroki{list-style:none;margin:20px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;counter-reset:k}
.kroki li{counter-increment:k;display:flex;align-items:center;gap:10px;min-height:54px;padding:8px 14px;background:var(--g);font-weight:700;color:var(--mut);line-height:1.2}
.kroki li::before{content:counter(k);flex:none;display:grid;place-items:center;width:32px;height:32px;border:2.5px solid currentColor;font-weight:800}
.kroki li.ok{color:var(--ink)}.kroki li.ok::before{background:var(--ink);border-color:var(--ink);color:#fff}
.kroki li[aria-current]{background:var(--ink);color:#fff}.kroki li[aria-current]::before{border-color:#fff;background:transparent;color:#fff}
.potw{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(24px,4vw,70px);align-items:start;margin-top:26px}
.potw .ok-h{font-size:clamp(24px,1.8vw,34px);display:flex;gap:14px;align-items:center}
.potw .ok-h::before{content:"";flex:none;width:30px;height:30px;background:var(--ink);box-shadow:-8px -8px 0 -2px #fff,-8px -8px 0 0 var(--aq)}
.potw dl{margin:18px 0 0;display:grid;grid-template-columns:minmax(0,12em) minmax(0,1fr);border-top:1px solid var(--line)}
.potw dt,.potw dd{margin:0;padding:12px 0;border-bottom:1px solid var(--line)}.potw dt{color:var(--mut);font-weight:600}.potw dd{font-weight:700}
.potw ol{margin:14px 0 0;padding-left:22px}.potw ol li{margin-top:10px;line-height:1.5}
.potw .bok{background:var(--g);padding:clamp(20px,2.4vw,34px)}
.potw .bok h2{font-size:1.4rem}
.potw .akc{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}
@media (max-width:1000px){.potw{grid-template-columns:minmax(0,1fr)}}
@media (max-width:700px){.kroki{grid-template-columns:1fr 1fr}.kroki li{font-size:.95rem;min-height:50px;padding:8px 10px}.potw dl{grid-template-columns:1fr}.potw dt{padding-bottom:0;border-bottom:0}.potw dd{padding-top:2px}}
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
<meta name="robots" content="noindex,nofollow" data-podglad>
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

DOST = {'jest': ('jest', 'Dostępny'), 'zam': ('zam', 'Czas realizacji: 14 dni'), 'brak': ('brak', 'Brak w magazynie')}
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
            f'<div class="in"><{nag}><span class="kw {k}"></span><a href="../{p["slug"]}/">{E(p["nazwa"])}</a></{nag}>{f'<p class="po">{E(p["podtytul"])}</p>' if p.get('podtytul') else ''}'
            f'<p class="dost {d[0]}"><span class="b" aria-hidden="true"></span>{d[1]}</p><p class="cena"><b>{zl(p["cena"])}</b>{st}<span class="gratis">Transport gratis</span></p>{kup}</div></article>')


# --- karty produktow: uporzadkowane kopie ofert z aquaholm.pl (oferty.py), kolejnosc elementow jak u klienta
import oferty
SL = {p['id']: (p['slug'], ', '.join(x for x in oferty.nazwa_oferty(oferty.O[p['id']]) if x)) for p in P}
for p in P:                                   # nazwy, ceny i dostepnosc wg aktualnych ofert klienta (28.11.2026)
    o = oferty.O[p['id']]
    p['nazwa'], p['podtytul'] = oferty.nazwa_oferty(o)
    c = [int(round(x)) for x in o['ceny']]
    p['cena'], p['stara'] = (c[1], c[0]) if len(c) > 1 else (c[0], None)
    p['dost'] = 'brak' if 'Brak w magazynie' in o['stock'] else ('zam' if 'Czas realizacji' in o['nazwa'] else 'jest')
STYL_S = STYL_S.replace('</style>', oferty.CSS + '</style>')
IK_ODZ = {'Darmowa wysyłka': '<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
          'Dostępne Raty 0%': '<polyline points="20 6 9 17 4 12"/>',
          'Zapłać za 30 dni PayPo': '<rect x="3" y="4" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/>',
          'Dostępne Płatności Blik': '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'}
ODZ_TXT = {'Dostępne Płatności Blik': 'Dostępne płatności BLIK'}

def mini_karta(x):
    z = x['zdjecia'][0]
    st = f'<s>{zl(x["stara"])}</s>' if x['stara'] else ''
    cz = {'zam': 'Czas realizacji: 14 dni', 'brak': 'Brak w magazynie', 'jest': ''}[x['dost']]
    czh = f'<span class="cz">{cz}</span>' if cz else ''
    return (f'<article class="pk"><a class="f" href="../{x["slug"]}/" tabindex="-1" aria-hidden="true"><img src="../img/p/{z["m"][0]}" width="{z["m"][1]}" height="{z["m"][2]}" loading="lazy" decoding="async" alt=""></a>'
            f'<div class="in"><h3><a href="../{x["slug"]}/">{E(x["nazwa"])}</a></h3>{czh}<span class="c">{zl(x["cena"])}{st}</span></div></article>')

SKR_P = '''<script>
(function(){var d=document,du=d.getElementById('duze'),bd=du.parentNode,mb=[].slice.call(d.querySelectorAll('.mini2 button')),nr=d.getElementById('nrz'),cur=0;
function pokaz(i){if(!mb.length)return;cur=(i+mb.length)%mb.length;var b=mb[cur];du.src=b.dataset.duze;du.width=b.dataset.w;du.height=b.dataset.h;du.style.maxWidth='min(100%,'+b.dataset.w+'px)';du.alt=du.alt.replace(/zdjęcie \\d+$/,'zdjęcie '+(cur+1));bd.dataset.lb=b.dataset.duze;
mb.forEach(function(x){x.setAttribute('aria-current',x===b)});if(nr)nr.textContent=cur+1;var s=b.parentNode;s.scrollTo({left:b.offsetLeft-s.offsetLeft-s.clientWidth/2+b.clientWidth/2,behavior:'smooth'})}
mb.forEach(function(b,i){b.addEventListener('click',function(){pokaz(i)})});
var gp=d.querySelector('.gl2 .gp'),gn=d.querySelector('.gl2 .gn');if(gp){gp.addEventListener('click',function(){pokaz(cur-1)});gn.addEventListener('click',function(){pokaz(cur+1)})}
var tx=0;bd.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});bd.addEventListener('touchend',function(e){var dd=e.changedTouches[0].clientX-tx;if(Math.abs(dd)>45){pokaz(cur+(dd<0?1:-1))}});
var il=d.getElementById('il');if(il)d.querySelectorAll('[data-il]').forEach(function(b){b.addEventListener('click',function(){il.value=Math.max(1,(+il.value||1)+(+b.dataset.il))})});
var p=d.getElementById('pasek'),z=d.getElementById('zakup');
if('IntersectionObserver' in window)new IntersectionObserver(function(e){var on=!e[0].isIntersecting&&e[0].boundingClientRect.top<0;p.classList.toggle('on',on);p.setAttribute('aria-hidden',!on)}).observe(z);
/* podobne produkty: karuzela przesuwa sie sama od prawej do lewej, stop po najechaniu / dotyku */
var t=d.getElementById('ptor');if(t&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var st=false,wid=true;
['pointerenter','focusin','touchstart'].forEach(function(e){t.addEventListener(e,function(){st=true},{passive:true})});t.addEventListener('pointerleave',function(){st=false});
if('IntersectionObserver' in window)new IntersectionObserver(function(e){wid=e[0].isIntersecting}).observe(t);
setInterval(function(){if(st||!wid||d.hidden||t.scrollWidth<=t.clientWidth+4)return;var k=t.children[0].getBoundingClientRect().width+16;
if(t.scrollLeft+t.clientWidth>=t.scrollWidth-4)t.scrollTo({left:0,behavior:'smooth'});else t.scrollBy({left:k,behavior:'smooth'})},3000)}
})();
</script>'''

def strona_produktu(p):
    o = oferty.O[p['id']]
    k = kier(p)
    kat = ('wanny-z-hydromasazem', 'Wanny z hydromasażem') if p['typ'] == 'wanna' else ('bieznie-elektryczne', 'Bieżnie elektryczne')
    marka = 'Aquaholm' if p['typ'] == 'wanna' else 'APVsport'
    alt = p['nazwa']
    # galeria: wszystkie zdjecia z oferty klienta, kolejnosc jak u niego, natywny rozmiar
    G = [oferty.obraz(u) for u, w, h in o['galeria']]
    T = [oferty.obraz(u, True) for u, w, h in o['galeria']]
    g0 = G[0]
    gal = (f'<div class="gl2" id="gal"><div class="duze-w"><button class="duze" type="button" data-lb="../img/o/{g0[0]}" aria-label="Powiększ zdjęcie">'
           f'<img id="duze" src="../img/o/{g0[0]}" width="{g0[1]}" height="{g0[2]}" style="max-width:min(100%,{g0[1]}px)" fetchpriority="high" alt="{E(alt)}, zdjęcie 1"></button>')
    if len(G) > 1:
        gal += (f'<button class="gp" type="button" aria-label="Poprzednie zdjęcie">&#8249;</button><button class="gn" type="button" aria-label="Następne zdjęcie">&#8250;</button>'
                f'<span class="licz"><span id="nrz">1</span> / {len(G)}</span></div><div class="mini2">' + ''.join(
                f'<button type="button" data-duze="../img/o/{g[0]}" data-w="{g[1]}" data-h="{g[2]}"' + (' aria-current="true"' if i == 0 else '') + f' aria-label="Zdjęcie {i + 1} z {len(G)}">'
                f'<img src="../img/o/{t[0]}" width="{t[1]}" height="{t[2]}" loading="lazy" decoding="async" alt=""></button>' for i, (g, t) in enumerate(zip(G, T))) + '</div>')
    else:
        gal += '</div>'
    gal += '</div>'
    st = f'<s>{zl(p["stara"])}</s>' if p['stara'] else ''
    dost = {'zam': '<p class="dost zam"><span class="b" aria-hidden="true"></span>Czas realizacji: 14 dni</p>',
            'brak': '<p class="dost brak"><span class="b" aria-hidden="true"></span>Brak w magazynie</p>', 'jest': ''}[p['dost']]
    odz = ''.join(f'<li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IK_ODZ.get(x, "")}</svg>{E(ODZ_TXT.get(x, x))}</li>' for x in o['odznaki'])
    odz = f'<ul class="odz">{odz}</ul>' if odz else ''
    z0 = p['zdjecia'][0]
    kupuj = o['koszyk'] and p['dost'] != 'brak'
    if kupuj:
        kup = (f'<div class="kup"><div class="ilosc"><button type="button" data-il="-1" aria-label="Mniej">-</button><input id="il" type="number" min="1" value="1" aria-label="Ilość"><button type="button" data-il="1" aria-label="Więcej">+</button></div>'
               f'<button type="button" class="dok" data-kosz data-id="{p["id"]}" data-nazwa="{E(p["nazwa"])}" data-cena="{p["cena"]}" data-url="./" data-img="../img/p/{z0["m"][0]}">Dodaj do koszyka</button></div>')
    else:
        kup = f'<div class="kup"><a class="dok pyt" href="{WA}" target="_blank" rel="noopener">Zapytaj o termin na WhatsAppie</a></div>'
    meta = (f'SKU: {E(o["sku"])}<br>' if o['sku'] else '') + f'Kategoria: <a href="../{kat[0]}/">{kat[1]}</a>'
    pod = [PID[i] for i in o['podobne'] if isinstance(i, int) and i in PID]
    nav = ('<div class="nav" data-nav="ptor"><button type="button" data-k="-1" aria-label="Poprzednie produkty"></button>'
           '<button type="button" data-k="1" aria-label="Następne produkty"></button></div>') if len(pod) > 2 else ''
    sek_pod = (f'<section class="pods" aria-labelledby="h-pod"><div class="wrap"><div class="sg"><h2 id="h-pod">Podobne produkty</h2>{nav}</div>'
               f'<div class="ptor" id="ptor" data-tor>{"".join(mini_karta(x) for x in pod)}</div></div></section>') if pod else ''
    opis = oferty.opis_html(o, SL, alt)
    url = BAZA + p['slug'] + '/'
    pelna = p['nazwa'] + (f', {p["podtytul"]}' if p['podtytul'] else '')
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'TREG', 'item': BAZA},
                                                        {'@type': 'ListItem', 'position': 2, 'name': kat[1], 'item': BAZA + kat[0] + '/'},
                                                        {'@type': 'ListItem', 'position': 3, 'name': p['nazwa'], 'item': url}]},
        {'@type': 'Product', 'name': pelna, 'sku': o['sku'] or str(p['id']), **({'gtin13': o['ean']} if o.get('ean') else {}),
         'brand': {'@type': 'Brand', 'name': marka}, 'image': [BAZA + 'img/o/' + g[0] for g in G[:3]],
         'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'PLN', 'price': f'{p["cena"]}.00', 'availability': 'https://schema.org/' + SCH[p['dost']],
                    'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@type': 'Organization', 'name': 'TREG Łukasz Pawluczuk'}}}]}
    tytul = f'{p["nazwa"]} | TREG'
    opis_m = f'{pelna}. Cena {zl(p["cena"])}' + (f' (wcześniej {zl(p["stara"])})' if p['stara'] else '') + '.'
    if len(opis_m) > 160: opis_m = opis_m[:157].rsplit(' ', 1)[0] + '...'
    bz = ' bz' if k == 'apv' else ''
    info = ('<h2 class="info-h">Informacje dodatkowe</h2><table class="par info-t"><tbody>' + ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in o['info']) + '</tbody></table>') if o['info'] else ''
    podt = f'<span class="podt">{E(p["podtytul"])}</span>' if p['podtytul'] else ''
    ean = f'<p class="ean">EAN: {E(o["ean"])}</p>' if o.get('ean') else ''
    tresc = f'''<section class="kp{bz}" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / <a href="../{kat[0]}/">{kat[1]}</a> / {E(p['nazwa'])}</nav>
    <div class="kp-g">
      {gal}
      <div class="zak" id="zakup">
        <span class="marka"><span class="kw {k}"></span>{marka}</span>
        <h1 id="h1">{E(p['nazwa'])}{podt}</h1>
        <p class="cena"><b>{zl(p['cena'])}</b>{st}<small>z VAT</small></p>
        {dost}
        {ean}
        {odz}
        {kup}
        <p class="meta">{meta}</p>
      </div>
    </div>
  </div>
</section>
{sek_pod}
<section class="opis-s{bz}" id="opis" aria-labelledby="h-opis">
  <div class="wrap">
    <h2 id="h-opis">Opis</h2>
    <div class="opis" data-grupa>
{opis}
    </div>
    {info}
  </div>
</section>
<div class="pas" id="pasek" aria-hidden="true"><div class="wrap"><span class="n">{E(p['nazwa'])}</span><b>{zl(p['cena'])}</b><a class="dok" href="#zakup" tabindex="-1">{'Kup teraz' if kupuj else 'Zapytaj o termin'}</a></div></div>'''
    zapisz(p['slug'], podstrona(tytul, opis_m, p['slug'] + '/', tresc, ld, SKR_P))

for p in P: strona_produktu(p)
oferty.zapisz_obrazy()

# --- kategorie
def kategoria(sciezka, h1, tytul, opis, lead, prod, filtry, dodatkowe=''):
    fb = ''.join(f'<button type="button" data-f="{f}" aria-pressed="{"true" if f == "" else "false"}">{E(n)}</button>' for f, n in filtry)
    tresc = f'''<section class="kat" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / {E(h1)}</nav>
    <h1 id="h1">{E(h1)}</h1>
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
W.sort(key=lambda p: oferty.KOL_WANNY.index(p['id']))   # kolejnosc jak na aquaholm.pl/kategoria-produktu/wanny/
kategoria('wanny-z-hydromasazem', 'Wanny z hydromasażem', 'Wanny z hydromasażem Aquaholm: prostokątne, narożne, podwójne | TREG',
          f'{len(W)} wanien z hydromasażem Aquaholm Premium Line: prostokątne, narożne i podwójne, białe i czarne. Podgrzewacz, LED RGB, Bluetooth. Raty 0%.',
          f'{len(W)} modeli z serii Premium Line: prostokątne, narożne i podwójne, białe i czarne. Większość z podgrzewaczem wody, oświetleniem LED RGB, Bluetooth i pilotem.',
          W, [('', 'Wszystkie'), ('ksztalt:prostokatna', 'Prostokątne'), ('ksztalt:narozna', 'Narożne'), ('ksztalt:podwojna', 'Podwójne'), ('kolor:biala', 'Białe'), ('kolor:czarna', 'Czarne'), ('dost:jest', 'Od ręki')])
B = [p for p in P if p['typ'] in ('bieznia', 'akcesorium')]
B.sort(key=lambda p: oferty.KOL_BIEZNIE.index(p['id']))  # kolejnosc jak na aquaholm.pl: bieznie i akcesoria razem, jak u klienta
A = [p for p in P if p['typ'] == 'akcesorium']
kategoria('bieznie-elektryczne', 'Bieżnie elektryczne', 'Bieżnie elektryczne APVsport APV8000, APV6000, APV5000 | TREG',
          f'{len(B) - len(A)} bieżni elektrycznych APVsport: APV8000 z silnikiem do 6 KM i pasem 145 x 58 cm, APV6000, APV5000, APV900, APV600. Akcesoria. Raty 0%.',
          'Bieżnie APVsport do domu i do intensywnego treningu: APV8000 z silnikiem do 6 KM, pasem 145 x 58 cm i ekranem Android, a także APV6000, APV5000, APV900 i APV600. Doradzimy przy wyborze modelu, mamy własny serwis i części.',
          B, [('', 'Wszystkie'), ('model:apv8000', 'APV8000'), ('model:inne', 'Pozostałe modele'), ('typ:akcesorium', 'Akcesoria'), ('dost:zam', 'Dostępne do zamówienia')])

# --- koszyk
def kroki(n):
    t = ['Koszyk', 'Dane i dostawa', 'Płatność', 'Potwierdzenie']
    li = ''.join(f'<li class="ok">{x}</li>' if i + 1 < n else (f'<li aria-current="step">{x}</li>' if i + 1 == n else f'<li>{x}</li>') for i, x in enumerate(t))
    return f'<ol class="kroki" aria-label="Etapy zamówienia">{li}</ol>'

kosz = f'''<section class="kosz-s" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / Koszyk</nav>
    <h1 id="h1">Koszyk</h1>
    {kroki(1)}
    <div class="pusty" id="pusty" hidden><p>Koszyk jest pusty.</p><div class="akc"><a class="btn aq" href="../wanny-z-hydromasazem/">Wanny z hydromasażem</a><a class="btn apv" href="../bieznie-elektryczne/">Bieżnie elektryczne</a></div></div>
    <div class="kg" data-pelny hidden>
      <div>
        <ul id="lista" aria-label="Produkty w koszyku"></ul>
        <p class="razem"><span>Razem za produkty</span><b id="suma">0 zł</b></p>
        <p class="razem"><span>Dostawa kurierem</span><b>0 zł, transport gratis</b></p>
        <p class="uw">Transport gratis na wszystkie produkty, także na wanny i bieżnie wysyłane jako przesyłki nadwymiarowe. Zamawiając wannę lub bieżnię na zamówienie, przed wysyłką potwierdzimy termin realizacji.</p>
      </div>
      <form class="zamf" id="zamowienie">
        <h2>Dane do zamówienia</h2>
        <div class="r2"><label>Imię i nazwisko<input type="text" name="n" autocomplete="name" required></label><label>Telefon<input type="tel" name="t" autocomplete="tel" required></label></div>
        <label>E-mail<input type="email" name="e" autocomplete="email" required></label>
        <label>Ulica i numer<input type="text" name="u" autocomplete="street-address" required></label>
        <div class="r2"><label>Kod pocztowy<input type="text" name="k" autocomplete="postal-code" required></label><label>Miejscowość<input type="text" name="m" autocomplete="address-level2" required></label></div>
        <fieldset><legend>Dostawa</legend>
          <label class="op"><input type="radio" name="dost" checked><span>Kurier: 0 zł, transport gratis<small>Także przesyłki nadwymiarowe i bardzo ciężkie, ubezpieczone.</small></span></label>
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
        <p class="komunikat">To podgląd sklepu: po kliknięciu zobaczysz stronę potwierdzenia, ale zamówienie nigdzie nie zostanie wysłane.</p>
      </form>
    </div>
  </div>
</section>'''
zapisz('koszyk', podstrona('Koszyk | TREG', 'Koszyk sklepu TREG: wanny z hydromasażem Aquaholm i bieżnie elektryczne APVsport.', 'koszyk/', kosz))

# --- potwierdzenie zamowienia (podglad: dane z koszyka w sessionStorage, nic nie jest wysylane)
potw = f'''<section class="kosz-s" aria-labelledby="h1">
  <div class="wrap">
    <nav class="okr" aria-label="Okruszki"><a href="../">TREG</a> / <a href="../koszyk/">Koszyk</a> / Potwierdzenie</nav>
    <h1 id="h1">Dziękujemy, zamówienie przyjęte</h1>
    {kroki(4)}
    <div class="potw">
      <div>
        <h2 class="ok-h">Podsumowanie zamówienia</h2>
        <ul id="lista-p" aria-label="Zamówione produkty" style="list-style:none;margin:16px 0 0;padding:0;border-top:1px solid var(--line)"></ul>
        <dl>
          <dt>Razem za produkty</dt><dd id="p-suma">-</dd>
          <dt>Dostawa</dt><dd>Kurier: 0 zł, transport gratis</dd>
          <dt>Płatność</dt><dd id="p-pl">-</dd>
          <dt>Adres dostawy</dt><dd id="p-adr">-</dd>
        </dl>
        <p class="komunikat">To podgląd sklepu: zamówienie nie zostało nigdzie wysłane. W uruchomionym sklepie w tym miejscu klient zobaczy numer zamówienia.</p>
      </div>
      <aside class="bok" aria-labelledby="h-co">
        <h2 id="h-co">Co dalej?</h2>
        <ol>
          <li>Na podany adres e-mail przyjdzie potwierdzenie zamówienia z listą produktów.</li>
          <li>Przy płatności online od razu przechodzisz do bezpiecznej płatności (BLIK, przelew, karta). Raty 0% i PayPo wybierasz w tym samym miejscu.</li>
          <li>Przy wannie albo bieżni na zamówienie przed wysyłką potwierdzimy termin realizacji.</li>
          <li>Kurier dostarcza paczkę pod wskazany adres. Transport gratis, także przesyłki nadwymiarowe.</li>
        </ol>
        <p style="margin-top:16px">Pytanie do zamówienia? Zadzwoń: <a href="tel:+48503538038"><b>503 538 038</b></a> albo napisz na WhatsAppie.</p>
        <div class="akc"><a class="btn aq" href="../wanny-z-hydromasazem/">Wanny z hydromasażem</a><a class="btn apv" href="../bieznie-elektryczne/">Bieżnie elektryczne</a></div>
      </aside>
    </div>
  </div>
</section>'''
zapisz('zamowienie-przyjete', podstrona('Zamówienie przyjęte | TREG', 'Potwierdzenie zamówienia w sklepie TREG.', 'zamowienie-przyjete/', potw))

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
<ul><li>Kurierem: przedmioty o standardowych wymiarach, paczka do 25 kg.</li><li>Kurierem: przedmioty nadwymiarowe i bardzo ciężkie, czyli wanny i bieżnie.</li><li><b>Transport gratis na wszystkie produkty</b>: koszt wysyłki pokrywamy my, nie doliczamy go do zamówienia.</li>
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
for s in [x for x in STRONY if x not in ("zamowienie-przyjete/", "koszyk/")]:
    if BAZA + s not in sm: sm = sm.replace('</urlset>', f'<url><loc>{BAZA}{s}</loc></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('sklep ok', len(STRONY))
