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

# (miasto, w + miejscownik, dopelniacz, wojewodztwo, wyroznik - zdanie wlasne dla miasta)
M = [
 ('Warszawa','w Warszawie','Warszawy','mazowieckie','W stolicy wiele osób mieszka w nowych apartamentowcach i biega wzdłuż Wisły albo po Polu Mokotowskim. Bieżnia w domu pozwala trenować także zimą i późnym wieczorem, bez dojazdów na siłownię przez zakorkowane miasto.'),
 ('Kraków','w Krakowie','Krakowa','małopolskie','Krakowskie łazienki są bardzo różne: inne w kamienicy na Kazimierzu, inne w nowym bloku na Ruczaju. Dlatego pokazujemy wanny od 170 x 78 cm po narożne 150 x 150 cm, z wymiarami podanymi przy każdym modelu.'),
 ('Wrocław','we Wrocławiu','Wrocławia','dolnośląskie','Wrocław biega nad Odrą i po bulwarach, ale nie każdy wieczór sprzyja wyjściu z domu. Bieżnia APV8000 z ekranem Android pozwala przebiec wirtualną trasę we własnym salonie.'),
 ('Łódź','w Łodzi','Łodzi','łódzkie','W łódzkich loftach w dawnych fabrykach i w przestronnych kamienicach przy Piotrkowskiej często jest miejsce na większą wannę, na przykład prostokątną 180 x 120 cm z wodospadem i podgrzewaczem wody.'),
 ('Poznań','w Poznaniu','Poznania','wielkopolskie','Wokół Malty biega wielu poznaniaków, a po treningu przydaje się ciepła kąpiel z hydromasażem. Kto może poczekać na wannę z terminem realizacji 30 dni, płaci mniej niż za ten sam model od ręki.'),
 ('Gdańsk','w Gdańsku','Gdańska','pomorskie','Nadmorska zima w Gdańsku bywa wilgotna i wietrzna. Wanna z podgrzewaczem wody utrzymuje temperaturę kąpieli, a bieżnia pozwala nie przerywać treningu, gdy na plaży w Brzeźnie wieje zbyt mocno.'),
 ('Szczecin','w Szczecinie','Szczecina','zachodniopomorskie','W szczecińskich kamienicach łazienki bywają wysokie i przestronne, więc dobrze sprawdzają się w nich duże wanny prostokątne i narożne z podświetleniem LED.'),
 ('Lublin','w Lublinie','Lublina','lubelskie','W Lublinie coraz więcej osób urządza w domu miejsce do ćwiczeń. Bieżnie APVsport mają silniki od 3,5 do 6 KM, więc łatwo dobrać model do spaceru, marszu i biegu.'),
 ('Bydgoszcz','w Bydgoszczy','Bydgoszczy','kujawsko-pomorskie','Bydgoszczanie chętnie biegają nad Brdą i w Myślęcinku, a po sezonie przenoszą trening do domu. Bieżnia z pasem 145 x 58 cm daje zapas miejsca także przy szybszym biegu.'),
 ('Białystok','w Białymstoku','Białegostoku','podlaskie','Białystok jest najbliżej naszej siedziby w Bielsku Podlaskim, około 50 km. Klienci z Białegostoku mogą więc łatwo zadzwonić, dopytać o model i ustalić z nami szczegóły dostawy.'),
 ('Katowice','w Katowicach','Katowic','śląskie','W Katowicach, stolicy regionu, wiele osób pracuje do późna w biurowcach wokół Spodka i strefy kultury. Domowa bieżnia oszczędza czas, który zabierałby dojazd na siłownię.'),
 ('Gdynia','w Gdyni','Gdyni','pomorskie','Gdynia słynie z modernistycznych kamienic i nowoczesnych osiedli nad morzem. Białe i czarne wanny Aquaholm z prostą linią pasują do jasnych, minimalistycznych łazienek.'),
 ('Częstochowa','w Częstochowie','Częstochowy','śląskie','W Częstochowie wiele rodzin mieszka w domach jednorodzinnych, gdzie łazienka pozwala na wannę narożną 150 x 150 cm, wygodną także dla dwóch osób.'),
 ('Radom','w Radomiu','Radomia','mazowieckie','Radom leży między Warszawą a Kielcami i dobrze skomunikowanym miastem dojeżdża kurier z dużymi przesyłkami. Wannę lub bieżnię dostarczamy pod wskazany adres w mieście i okolicy.'),
 ('Rzeszów','w Rzeszowie','Rzeszowa','podkarpackie','Rzeszów szybko się rozbudowuje, powstaje tu wiele nowych mieszkań i domów. Przy urządzaniu nowej łazienki warto od razu zaplanować miejsce na wannę z hydromasażem i dostęp do gniazdka.'),
 ('Toruń','w Toruniu','Torunia','kujawsko-pomorskie','Toruń kojarzy się z gotycką starówką nad Wisłą, ale wiele osób mieszka tu w nowych osiedlach na obrzeżach. W takich mieszkaniach dobrze sprawdza się kompaktowa wanna 170 x 80 cm.'),
 ('Sosnowiec','w Sosnowcu','Sosnowca','śląskie','W Sosnowcu i całym Zagłębiu wiele osób mieszka w blokach z łazienkami o typowych wymiarach. Do nich pasują wanny prostokątne 170 x 78 cm i 170 x 80 cm z pełnym wyposażeniem.'),
 ('Kielce','w Kielcach','Kielc','świętokrzyskie','Kielce otaczają Góry Świętokrzyskie, a miłośnicy wędrówek szukają sposobu na trening przez cały rok. Na domowej bieżni mogą trenować kondycję przez cały rok, także zimą.'),
 ('Gliwice','w Gliwicach','Gliwic','śląskie','Gliwice to miasto techniki i politechniki, a tutejsi klienci często pytają o konkretne parametry. Przy każdym modelu podajemy wymiary, moc silnika, wielkość ekranu i wyposażenie.'),
 ('Olsztyn','w Olsztynie','Olsztyna','warmińsko-mazurskie','Olsztyn to miasto jezior, a jego mieszkańcy lubią ruch na świeżym powietrzu. Gdy pogoda nie pozwala na bieg wokół Ukiela, bieżnia w domu pozwala utrzymać formę.'),
 ('Bielsko-Biała','w Bielsku-Białej','Bielska-Białej','śląskie','Bielsko-Biała leży u stóp Beskidów, więc wielu mieszkańców trenuje przed górskimi wyjściami. Bieżnia APV8000 z silnikiem 6 KM nadaje się do długich marszów i biegu.'),
 ('Zabrze','w Zabrzu','Zabrza','śląskie','Zabrze ma silne tradycje górnicze, a po ciężkim dniu najlepiej regeneruje ciepła kąpiel. Dysze obrotowe i podgrzewacz wody w wannach Premium Line pozwalają długo cieszyć się hydromasażem.'),
 ('Bytom','w Bytomiu','Bytomia','śląskie','W Bytomiu, jednym z najstarszych miast Górnego Śląska, wiele osób mieszka w starszych kamienicach. Przed zamówieniem doradzimy, który model zmieści się w łazience o nietypowych wymiarach.'),
 ('Zielona Góra','w Zielonej Górze','Zielonej Góry','lubuskie','Zielona Góra słynie z winiarskich tradycji i spokojnego tempa życia. Wieczorna kąpiel w wannie z podświetleniem LED i muzyką z Bluetooth to dobry sposób na odpoczynek po pracy.'),
 ('Rybnik','w Rybniku','Rybnika','śląskie','Rybniczanie chętnie biegają nad Zalewem Rybnickim, a zimą przenoszą trening pod dach. Bieżnia z ekranem dotykowym pozwala korzystać z aplikacji treningowych, takich jak Kinomap i Zwift.'),
 ('Ruda Śląska','w Rudzie Śląskiej','Rudy Śląskiej','śląskie','Ruda Śląska składa się z kilku dzielnic o różnej zabudowie, od familoków po nowe domy. Niezależnie od łazienki pomożemy dobrać wannę i potwierdzimy jej dostępność przed zamówieniem.'),
 ('Opole','w Opolu','Opola','opolskie','Opole kojarzy się z festiwalem piosenki, a muzyka towarzyszy też kąpieli: wanny Aquaholm mają Bluetooth, więc można słuchać ulubionych utworów prosto z telefonu.'),
 ('Tychy','w Tychach','Tychów','śląskie','W Tychach wiele osób biega nad jeziorem Paprocany. Na chłodniejsze miesiące bieżnia APVsport z pasem 145 x 58 cm daje możliwość kontynuowania treningu w domu.'),
 ('Gorzów Wielkopolski','w Gorzowie Wielkopolskim','Gorzowa Wielkopolskiego','lubuskie','Gorzów Wielkopolski nad Wartą ma wiele osiedli domów jednorodzinnych. Tam często jest miejsce na dużą wannę 180 x 120 cm albo na osobny kąt do ćwiczeń z bieżnią.'),
 ('Elbląg','w Elblągu','Elbląga','warmińsko-mazurskie','Elbląg leży blisko Zalewu Wiślanego, gdzie jesienią i zimą bywa chłodno i wietrznie. Ciepła kąpiel z hydromasażem i trening na bieżni w domu nie zależą od pogody.'),
 ('Dąbrowa Górnicza','w Dąbrowie Górniczej','Dąbrowy Górniczej','śląskie','Dąbrowa Górnicza ma jeziora Pogoria, wokół których trenuje wielu biegaczy. Poza sezonem trening można kontynuować na bieżni z programami i regulacją prędkości.'),
 ('Płock','w Płocku','Płocka','mazowieckie','Płock na skarpie nad Wisłą to miasto, w którym wiele osób pracuje w systemie zmianowym. Bieżnia w domu pozwala ćwiczyć o dowolnej porze, niezależnie od godzin otwarcia siłowni.'),
 ('Wałbrzych','w Wałbrzychu','Wałbrzycha','dolnośląskie','Wałbrzych otaczają Sudety, a okolice zamku Książ przyciągają spacerowiczów i biegaczy. Na bieżni w domu można budować kondycję przed górskimi trasami bez względu na pogodę.'),
 ('Włocławek','we Włocławku','Włocławka','kujawsko-pomorskie','Włocławek nad Wisłą ma wiele domów i mieszkań z łazienkami do odnowienia. Przy remoncie pomożemy wybrać wannę, która zmieści się w łazience, i podamy jej dokładne wymiary.'),
 ('Tarnów','w Tarnowie','Tarnowa','małopolskie','Tarnów nazywany jest polskim biegunem ciepła, ale zimy i tu bywają chłodne. Wanna z podgrzewaczem wody utrzymuje ciepłą kąpiel, a bieżnia pozwala trenować przez cały rok.'),
 ('Chorzów','w Chorzowie','Chorzowa','śląskie','Chorzów ma Park Śląski, jeden z największych parków miejskich w Europie, ulubione miejsce biegaczy. Na deszczowe dni warto mieć w domu bieżnię APVsport.'),
 ('Koszalin','w Koszalinie','Koszalina','zachodniopomorskie','Koszalin leży niedaleko Bałtyku, u stóp Góry Chełmskiej. Gdy nad morzem wieje i pada, trening na bieżni w domu pozwala nie tracić formy.'),
 ('Kalisz','w Kaliszu','Kalisza','wielkopolskie','Kalisz uchodzi za jedno z najstarszych miast w Polsce, z wieloma starszymi kamienicami. Przed zakupem doradzimy, czy wybrana wanna zmieści się w drzwiach i w łazience.'),
 ('Legnica','w Legnicy','Legnicy','dolnośląskie','Legnica leży w Zagłębiu Miedziowym, gdzie wiele osób pracuje fizycznie i ceni dobrą regenerację. Hydromasaż z dyszami obrotowymi pomaga rozluźnić mięśnie po pracy.'),
 ('Grudziądz','w Grudziądzu','Grudziądza','kujawsko-pomorskie','Grudziądz znany jest ze spichrzy nad Wisłą i rosnącej liczby nowych osiedli. W nowych mieszkaniach dobrze sprawdzają się wanny prostokątne 170 cm z podświetleniem LED i pilotem.'),
]
assert len(M) == 40

def slug(t):
    t = t.replace('ł', 'l').replace('Ł', 'L')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

WSTEP = [
 'Wanny z hydromasażem Aquaholm i bieżnie elektryczne APVsport dostarczamy {w} kurierem, prosto od producenta z Bielska Podlaskiego.',
 'Szukają Państwo wanny z hydromasażem albo bieżni elektrycznej {w}? TREG produkuje i sprzedaje oba rodzaje sprzętu, a dostawę do {d} organizujemy kurierem.',
 'TREG z Bielska Podlaskiego wysyła wanny Aquaholm i bieżnie APVsport do klientów {w} i w całym województwie {woj}.',
 'Do {d} wysyłamy zarówno wanny z hydromasażem Aquaholm, jak i bieżnie elektryczne APVsport, bez pośredników, z własnym serwisem producenta.',
]
DOST = [
 ['Wysyłka kurierem na adres {w}', 'Przewidywany czas dostawy: 1 dzień roboczy od wysyłki', 'Darmowa wysyłka produktów oznaczonych na karcie'],
 ['Dostawa pod wskazany adres {w} i okolicy', 'Duże przesyłki obsługuje kurier od paczek nadwymiarowych', 'Termin modeli na zamówienie ustalamy przed wysyłką'],
 ['Kurier dowozi wanny i bieżnie do {d} i całego województwa {woj}', 'Zwykle 1 dzień roboczy od nadania', 'O dniu dostawy informujemy przed wysyłką'],
]
FAQ = [
 ('Ile trwa dostawa wanny z hydromasażem {w}?', 'Modele dostępne od ręki wysyłamy kurierem, przewidywany czas dostawy to 1 dzień roboczy od wysyłki. Wanny z oznaczeniem „na zamówienie” mają termin realizacji 30 dni i są tańsze od tych samych modeli od ręki.'),
 ('Czy bieżnię APVsport można kupić na raty, mieszkając {w}?', 'Tak. W sklepie są raty 0%, PayPo (zapłata za 30 dni), BLIK, przelew i płatność przy odbiorze. Sposób płatności wybiera się przy zamówieniu, niezależnie od miasta.'),
 ('Kto zajmie się serwisem, jeśli coś się zepsuje?', 'Jesteśmy producentem, więc serwis gwarancyjny i pogwarancyjny prowadzimy sami i mamy własny magazyn części zamiennych. Klienci z {d} mogą zgłosić usterkę telefonicznie, mailem lub na WhatsAppie.'),
 ('Jak dobrać wannę do łazienki {w}?', 'Przy każdym modelu podajemy dokładne wymiary: od 170 x 78 cm po 180 x 120 cm w wannach prostokątnych i 140 x 140 lub 150 x 150 cm w narożnych. Wystarczy przesłać nam wymiary łazienki, a doradzimy model.'),
 ('Którą bieżnię wybrać do domu?', 'Do marszu i spokojnego biegu wystarczy model z silnikiem 4-5 KM. Do szybszego biegu i dla cięższych osób polecamy APV8000 z silnikiem 6 KM i pasem 145 x 58 cm. Chętnie doradzimy {w} przez telefon lub WhatsApp.'),
]

def rot(lst, k):
    k %= len(lst); return lst[k:] + lst[:k]

WA = 'https://wa.me/48660489335'
FW = ['w9014','w9011','w8008','w8008c','w9001']
FB = ['futura','premium','top']
strony = []
for i, (m, w, dop, woj, wyr) in enumerate(M):
    sl = 'wanny-z-hydromasazem-' + slug(m)
    f = dict(w=w, d=dop, woj=woj, m=m)
    tytul = f'Wanny z hydromasażem i bieżnie elektryczne {m} | TREG'
    opis = f'Wanny z hydromasażem Aquaholm i bieżnie elektryczne APVsport z dostawą {w}. Raty 0%, PayPo, BLIK, serwis producenta. Tel. 503 538 038.'
    wst = WSTEP[i % 4].format(**f)
    dl = DOST[i % 3]
    faq = [FAQ[(i + j) % 5] for j in range(3)]
    faqh = ''.join(f'<details><summary>{H.escape(q.format(**f))}</summary><p>{H.escape(a.format(**f))}</p></details>' for q, a in faq)
    ld = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ','.join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q.format(**f).replace('"', '\\"'), a.format(**f).replace('"', '\\"').replace('„', '').replace('”', '')) for q, a in faq) + ']}')
    tw = '\n'.join(rot(WANNY, i)); tb = '\n'.join(rot(BIEZNIE, i * 2))
    strona = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{H.escape(tytul)}</title>
<meta name="description" content="{H.escape(opis)}">
<link rel="canonical" href="{BAZA}{sl}/">
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
    <p class="okr"><a href="../">TREG</a> / {H.escape(m)}</p>
    <h1 id="h1">Wanny z hydromasażem i bieżnie elektryczne: {H.escape(m)}</h1>
    <p class="lead">{H.escape(wst)}</p>
    <p class="lead">{H.escape(wyr)}</p>
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
        <h2 id="h-wanny"><span class="kw aq"></span>Wanny z hydromasażem {H.escape(w)}</h2>
        <p class="lead">Seria Premium Line: prostokątne i narożne, białe i czarne, z podgrzewaczem wody, Bluetooth i podświetleniem LED.</p>
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
        <h2 id="h-bieznie"><span class="kw apv"></span>Bieżnie elektryczne {H.escape(w)}</h2>
        <p class="lead">Bieżnie APVsport do marszu i biegu, od modeli z ekranem LCD po APV8000 z ekranem dotykowym Android.</p>
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
    <div class="sg"><div><h2 id="h-dostawa">Dostawa do {H.escape(dop)}, płatności i serwis</h2></div></div>
    <div class="info4">
      <div><h3><span class="kw aq"></span>Dostawa</h3><ul>{''.join(f'<li>{H.escape(x.format(**f))}</li>' for x in dl)}</ul></div>
      <div><h3><span class="kw apv"></span>Płatności</h3><ul><li>Raty 0%</li><li>PayPo: zapłać za 30 dni</li><li>BLIK i przelew</li><li>Płatność przy odbiorze</li></ul></div>
      <div><h3><span class="kw aq"></span>Serwis producenta</h3><ul><li>Serwis gwarancyjny i pogwarancyjny</li><li>Własny magazyn części zamiennych</li><li>Zgłoszenie telefonicznie, mailem lub na WhatsAppie</li></ul></div>
      <div><h3><span class="kw apv"></span>Doradztwo</h3><ul><li>Pomożemy dobrać wannę do wymiarów łazienki</li><li>Doradzimy bieżnię do marszu lub biegu</li><li>Potwierdzimy dostępność przed zamówieniem</li></ul></div>
    </div>
  </div>
</section>

<section class="sek szary" id="pytania" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="sg"><div><h2 id="h-faq">Najczęstsze pytania klientów {H.escape(w)}</h2></div></div>
    <div class="faq">{faqh}</div>
  </div>
</section>

<section class="sek" id="kontakt" aria-labelledby="h-kontakt">
  <div class="wrap">
    <h2 id="h-kontakt">Zadzwoń albo napisz</h2>
    <p class="lead" style="max-width:62ch;color:var(--mut);margin-top:14px">Doradzimy przy wyborze wanny lub bieżni i potwierdzimy termin dostawy {H.escape(w)}. Poniedziałek-piątek 9:00-18:00.</p>
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
    import os
    os.makedirs(sl, exist_ok=True)
    open(f'{sl}/index.html', 'w', encoding='utf-8').write(strona)
    strony.append(sl)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + f'<url><loc>{BAZA}</loc></url>\n' + ''.join(f'<url><loc>{BAZA}{s}/</loc></url>\n' for s in strony) + '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('miasta:', len(strony), strony[:3])
