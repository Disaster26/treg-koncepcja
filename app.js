(function(){
  var d=document,top=d.getElementById('top'),bg=d.getElementById('burger');
  function zamknij(){top.classList.remove('open');bg.setAttribute('aria-expanded','false');bg.setAttribute('aria-label','Otwórz menu')}
  bg.addEventListener('click',function(){var o=top.classList.toggle('open');bg.setAttribute('aria-expanded',o);bg.setAttribute('aria-label',o?'Zamknij menu':'Otwórz menu')});
  d.querySelectorAll('.menu a').forEach(function(a){a.addEventListener('click',zamknij)});

  var hero=d.querySelector('.hero');

  var prz=[].slice.call(d.querySelectorAll('.prz a')),links=[].slice.call(d.querySelectorAll('.menu a[href^="#"]'));
  if('IntersectionObserver' in window){
    /* przelacznik wanny / bieznie: widoczny na telefonie po zejsciu z pierwszego ekranu, podswietla aktualny kierunek */
    if(hero)new IntersectionObserver(function(es){d.body.classList.toggle('zsz',!es[0].isIntersecting)},{threshold:0,rootMargin:'-40% 0px 0px 0px'}).observe(hero);else d.body.classList.add('zsz');
    var ioK=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var k=e.target.getAttribute('data-k');prz.forEach(function(a){a.classList.toggle('on',a.getAttribute('data-k')===k)})}})},{rootMargin:'-45% 0px -50% 0px'});
    d.querySelectorAll('section[id]').forEach(function(s){ioK.observe(s)});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-45% 0px -50% 0px'});
    d.querySelectorAll('section[id]').forEach(function(s){io.observe(s)});
    /* mapa Google dopiero przy przewinieciu */
    var m=d.getElementById('mapa');
    if(m)new IntersectionObserver(function(es,o){if(es[0].isIntersecting){o.disconnect();var f=d.createElement('iframe');f.src=m.dataset.src;f.title='Mapa Google: TREG, ul. 30 Lipca 2, Bielsk Podlaski';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';m.appendChild(f)}},{rootMargin:'300px'}).observe(m);
  }
  /* sekcje bez data-k nie zmieniaja przelacznika */

  /* przeciaganie mysza: pasy kart i galerie w kartach */
  function przeciagaj(el,krok){
    var down=false,sx=0,sl=0,moved=false;
    el.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'||e.button!==0||el.scrollWidth<=el.clientWidth+2)return;e.stopPropagation();down=true;moved=false;sx=e.clientX;sl=el.scrollLeft});
    addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-sx;if(Math.abs(dx)>4){moved=true;el.classList.add('drag');el.style.scrollSnapType='none'}el.scrollLeft=sl-dx});
    addEventListener('pointerup',function(){if(!down)return;down=false;el.classList.remove('drag');if(moved){var w=krok();var cel=Math.round(el.scrollLeft/w)*w;el.style.scrollSnapType='';el.scrollTo({left:cel,behavior:'smooth'})}else el.style.scrollSnapType='';setTimeout(function(){moved=false},0)});
    el.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
    el.addEventListener('dragstart',function(e){e.preventDefault()});
  }
  d.querySelectorAll('[data-tor]').forEach(function(tor){
    function step(){var k=tor.children[0];return k?k.getBoundingClientRect().width+parseFloat(getComputedStyle(tor).columnGap||0):300}
    przeciagaj(tor,step);
    var nav=d.querySelector('[data-nav="'+tor.id+'"]');
    if(nav){var bs=nav.querySelectorAll('button');
      bs.forEach(function(b){b.addEventListener('click',function(){tor.scrollBy({left:step()*(+b.dataset.k),behavior:'smooth'})})});
      function upd(){bs[0].disabled=tor.scrollLeft<4;bs[1].disabled=tor.scrollLeft+tor.clientWidth>=tor.scrollWidth-4}
      bs[0].disabled=true;tor.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);
    }
  });
  d.querySelectorAll('.fl .reszta').forEach(function(r){przeciagaj(r,function(){var k=r.children[0];return k?k.getBoundingClientRect().width+14:300})});
  d.querySelectorAll('.gal').forEach(function(g){
    var gt=g.querySelector('.gt'),kr=g.querySelectorAll('.kr i'),p=g.querySelector('.gp'),n=g.querySelector('.gn');
    function w(){return gt.clientWidth||1}
    var zal=false;function wczytaj(){if(zal)return;zal=true;gt.querySelectorAll('img[data-src]').forEach(function(i){i.src=i.dataset.src;i.removeAttribute('data-src')})}
    ['pointerenter','touchstart','focusin','scroll'].forEach(function(ev){gt.addEventListener(ev,wczytaj,{passive:true,once:true})});
    if(p){p.addEventListener('pointerenter',wczytaj,{once:true});n.addEventListener('pointerenter',wczytaj,{once:true})}
    przeciagaj(gt,w);
    function upd(){var i=Math.round(gt.scrollLeft/w());kr.forEach(function(k,j){k.classList.toggle('on',j===i)});if(p){p.disabled=i<=0;n.disabled=i>=gt.children.length-1}}
    if(p)p.disabled=true;gt.addEventListener('scroll',upd,{passive:true});
    if(p){p.addEventListener('click',function(){wczytaj();gt.scrollBy({left:-w(),behavior:'smooth'})});n.addEventListener('click',function(){wczytaj();gt.scrollBy({left:w(),behavior:'smooth'})})}
  });

  /* koszyk - tylko element wygladu podgladu */
  d.querySelectorAll('[data-kosz]').forEach(function(b){b.addEventListener('click',function(){if(b.classList.contains('ok'))return;b.classList.add('ok');b.textContent='W koszyku'})});

  /* filmy: fasada, odtwarzacz YouTube dopiero po kliknieciu */
  d.querySelectorAll('[data-yt]').forEach(function(b){b.addEventListener('click',function(){
    if(b.querySelector('iframe'))return;var f=d.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.yt+'?autoplay=1&rel=0';f.title=b.getAttribute('aria-label').replace('Odtwórz film: ','');
    f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;b.appendChild(f)})});

  /* lightbox */
  var lb=d.getElementById('lb'),li=lb.querySelector('img'),lp=lb.querySelector('p'),cur=0,last=null,grp=[];
  function opis(b){var a=b.closest('.prod');var h=a&&a.querySelector('h3');return h?h.textContent:''}
  function pokaz(i){cur=(i+grp.length)%grp.length;var b=grp[cur];li.src=b.dataset.lb;var im=b.querySelector('img');li.alt=im?im.alt:'';lp.textContent=opis(b)+(grp.length>1?'  ('+(cur+1)+'/'+grp.length+')':'');lb.querySelector('.p').hidden=lb.querySelector('.n').hidden=grp.length<2}
  d.querySelectorAll('[data-lb]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();last=b;var g=b.closest('[data-grupa]');grp=g?[].slice.call(g.querySelectorAll('[data-lb]')):[b];pokaz(grp.indexOf(b));lb.classList.add('otw');d.body.style.overflow='hidden';lb.querySelector('.x').focus()})});
  function zam(){lb.classList.remove('otw');d.body.style.overflow='';li.removeAttribute('src');if(last)last.focus()}
  lb.querySelector('.x').addEventListener('click',zam);
  lb.querySelector('.p').addEventListener('click',function(){pokaz(cur-1)});
  lb.querySelector('.n').addEventListener('click',function(){pokaz(cur+1)});
  lb.addEventListener('click',function(e){if(e.target===lb)zam()});
  var tx=0;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend',function(e){var dd=e.changedTouches[0].clientX-tx;if(Math.abs(dd)>50&&grp.length>1)pokaz(cur+(dd<0?1:-1))});
  d.addEventListener('keydown',function(e){
    if(e.key==='Escape'){if(lb.classList.contains('otw'))zam();else zamknij()}
    if(!lb.classList.contains('otw')||grp.length<2)return;
    if(e.key==='ArrowRight')pokaz(cur+1);if(e.key==='ArrowLeft')pokaz(cur-1);
  });

  var f=d.getElementById('form'),msg=d.getElementById('msg');
  if(f)f.addEventListener('submit',function(e){e.preventDefault();var ok=true;[].forEach.call(f.querySelectorAll('[required]'),function(i){var v=i.type==='checkbox'?(i.checked?'1':''):i.value.trim();var bad=!v;i.setAttribute('aria-invalid',bad);if(bad&&ok){ok=false;i.focus()}});if(!ok)return;msg.hidden=false;f.reset()});
  var r=d.getElementById('rok');if(r)r.textContent=new Date().getFullYear();
})();
