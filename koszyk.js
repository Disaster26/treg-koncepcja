/* koszyk sklepu (podglad): localStorage, licznik w naglowku, strona /koszyk/ z formularzem zamowienia */
(function(){
  var d=document,KL='treg-koszyk',PAS={id:20530,nazwa:'Pas piersiowy do pomiaru tętna',cena:125};
  var skrypt=d.currentScript&&d.currentScript.src,BAZA=skrypt?skrypt.replace(/koszyk\.js.*$/,''):'/';
  function czytaj(){try{var k=JSON.parse(localStorage.getItem(KL)||'[]');return Array.isArray(k)?k:[]}catch(e){return []}}
  function zapisz(k){try{localStorage.setItem(KL,JSON.stringify(k))}catch(e){}licznik(k)}
  function zl(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,' ')+' zł'}
  function abs(u){try{return new URL(u,location.href).href}catch(e){return u}}
  function licznik(k){var n=0;(k||czytaj()).forEach(function(p){n+=p.il});
    d.querySelectorAll('[data-licznik]').forEach(function(e){e.textContent=n;e.hidden=!n});
    d.querySelectorAll('.kosz').forEach(function(a){a.setAttribute('aria-label','Koszyk, produktów: '+n)})}
  function dodaj(p,il){var k=czytaj(),j=-1;k.forEach(function(x,i){if(x.id==p.id)j=i});
    if(j>=0)k[j].il+=il;else{p.il=il;k.push(p)}zapisz(k)}
  var tost;
  function pokaz(nazwa){
    if(!tost){tost=d.createElement('div');tost.className='tost';tost.setAttribute('role','status');d.body.appendChild(tost);
      var st=d.createElement('style');st.textContent='.tost{position:fixed;left:50%;bottom:22px;z-index:90;transform:translate(-50%,140%);width:min(560px,calc(100vw - 24px));background:#1e2124;color:#fff;padding:16px 18px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;box-shadow:0 14px 40px rgba(0,0,0,.3);transition:transform .25s}.tost.on{transform:translate(-50%,0)}.tost p{flex:1 1 100%;margin:0;font-weight:600;line-height:1.35}.tost a,.tost button{font:700 .98rem Archivo,Arial,sans-serif;min-height:46px;padding:0 18px;display:inline-flex;align-items:center;border:0;cursor:pointer;text-decoration:none}.tost a{background:#d7140f;color:#fff}.tost button{background:transparent;color:#fff;border:2px solid #5b636b}@media (prefers-reduced-motion:reduce){.tost{transition:none}}';d.head.appendChild(st)}
    tost.innerHTML='';var p=d.createElement('p');p.textContent='Dodano do koszyka: '+nazwa;tost.appendChild(p);
    var a=d.createElement('a');a.href=BAZA+'koszyk/';a.textContent='Przejdź do koszyka';tost.appendChild(a);
    var b=d.createElement('button');b.type='button';b.textContent='Kupuj dalej';b.onclick=function(){tost.classList.remove('on')};tost.appendChild(b);
    requestAnimationFrame(function(){tost.classList.add('on')});clearTimeout(tost._t);tost._t=setTimeout(function(){tost.classList.remove('on')},7000)}
  d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-kosz]');if(!b||!b.dataset.id)return;e.preventDefault();
    var il=1,pole=b.closest('.kup')&&d.getElementById('il');if(pole)il=Math.max(1,parseInt(pole.value,10)||1);
    dodaj({id:+b.dataset.id,nazwa:b.dataset.nazwa,cena:+b.dataset.cena,url:abs(b.dataset.url||location.href),img:abs(b.dataset.img||'')},il);
    var op=d.getElementById('pas');if(op&&op.checked&&b.closest('.kup')){dodaj({id:PAS.id,nazwa:PAS.nazwa,cena:PAS.cena,url:BAZA+'pas-piersiowy-do-pomiaru-tetna/',img:BAZA+'img/p/20530-1-600.webp'},1)}
    pokaz(b.dataset.nazwa)});
  licznik();
  window.addEventListener('storage',function(e){if(e.key===KL){licznik();rysuj()}});

  /* strona koszyka */
  var lista=d.getElementById('lista'),suma=d.getElementById('suma'),pusty=d.getElementById('pusty'),zam=d.getElementById('zamowienie');
  function rysuj(){if(!lista)return;var k=czytaj(),s=0;lista.innerHTML='';
    k.forEach(function(p,i){s+=p.cena*p.il;var li=d.createElement('li');li.className='poz';
      li.innerHTML='<a class="fz" href=""><img alt="" width="120" height="96" loading="lazy"></a><div class="op"><a class="nz" href=""></a><span class="cj"></span></div><div class="ilosc"><button type="button" data-z="-1" aria-label="Mniej">-</button><input type="number" min="1" aria-label="Ilość"><button type="button" data-z="1" aria-label="Więcej">+</button></div><b class="wr"></b><button type="button" class="us" aria-label="Usuń z koszyka">Usuń</button>';
      li.querySelector('.fz').href=p.url;li.querySelector('img').src=p.img;li.querySelector('.nz').href=p.url;li.querySelector('.nz').textContent=p.nazwa;
      li.querySelector('.cj').textContent=zl(p.cena)+' / szt.';li.querySelector('input').value=p.il;li.querySelector('.wr').textContent=zl(p.cena*p.il);
      li.querySelectorAll('[data-z]').forEach(function(z){z.onclick=function(){var k2=czytaj();k2[i].il=Math.max(1,k2[i].il+(+z.dataset.z));zapisz(k2);rysuj()}});
      li.querySelector('input').onchange=function(){var k2=czytaj();k2[i].il=Math.max(1,parseInt(this.value,10)||1);zapisz(k2);rysuj()};
      li.querySelector('.us').onclick=function(){var k2=czytaj();k2.splice(i,1);zapisz(k2);rysuj()};
      lista.appendChild(li)});
    suma.textContent=zl(s);pusty.hidden=!!k.length;d.querySelectorAll('[data-pelny]').forEach(function(e){e.hidden=!k.length})}
  rysuj();
  if(zam)zam.addEventListener('submit',function(e){e.preventDefault();var m=d.getElementById('komunikat');m.hidden=false;m.focus()});
})();
