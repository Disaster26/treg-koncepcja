/* Czat WhatsApp: okienko na stronie, wiadomosc wysylana w WhatsAppie na numer sklepu (wa.me). Bez zewnetrznych skryptow. */
(function(){
  var d=document,s=d.currentScript,NR=(s&&s.dataset.nr)||'48660489335',FIRMA=(s&&s.dataset.firma)||'Sklep',KOL=(s&&s.dataset.kolor)||'#1e2124';
  var css='.wa-b{position:fixed;right:18px;bottom:18px;z-index:90;transition:transform .2s,bottom .25s;width:62px;height:62px;border-radius:50%;border:0;background:#25d366;color:#fff;display:grid;place-items:center;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.22);transition:transform .2s}'+
  '.wa-b:hover{transform:scale(1.06)}.wa-b:focus-visible{outline:3px solid #0b6b34;outline-offset:3px}.wa-b svg{width:34px;height:34px}'+
  '.wa-b .wa-t{position:absolute;right:74px;top:50%;transform:translateY(-50%);white-space:nowrap;background:#fff;color:#1e2124;font:600 15px/1.2 Archivo,Arial,sans-serif;padding:10px 14px;border-radius:10px;box-shadow:0 6px 20px rgba(0,0,0,.16)}'+
  '.wa-p{position:fixed;right:18px;bottom:92px;z-index:91;width:min(370px,calc(100vw - 24px));background:#fff;border-radius:16px;box-shadow:0 18px 50px rgba(0,0,0,.28);overflow:hidden;display:none;font:16px/1.45 Archivo,Arial,sans-serif;color:#1e2124}'+
  '.wa-p.otw{display:block}.wa-h{background:'+KOL+';color:#fff;padding:16px 52px 16px 18px;position:relative}.wa-h b{display:block;font-size:18px}.wa-h span{font-size:14px;opacity:.85}'+
  '.wa-x{position:absolute;right:10px;top:12px;width:36px;height:36px;border:0;background:transparent;color:#fff;font-size:26px;line-height:1;cursor:pointer}'+
  '.wa-c{background:#efeae2;padding:16px}.wa-m{background:#fff;border-radius:0 12px 12px 12px;padding:12px 14px;max-width:92%;box-shadow:0 1px 1px rgba(0,0,0,.08)}'+
  '.wa-q{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.wa-q button{border:1px solid #25d366;background:#fff;color:#0b6b34;border-radius:18px;padding:7px 12px;font:600 14px Archivo,Arial,sans-serif;cursor:pointer}.wa-q button:hover{background:#e7f8ee}'+
  '.wa-f{display:flex;gap:8px;padding:12px;border-top:1px solid #e3e6ea}.wa-f textarea{flex:1;resize:none;height:52px;border:1px solid #cfd6dd;border-radius:10px;padding:10px 12px;font:16px/1.3 Archivo,Arial,sans-serif;color:#1e2124}'+
  '.wa-f button{border:0;border-radius:10px;background:#25d366;color:#fff;font:700 15px Archivo,Arial,sans-serif;padding:0 16px;cursor:pointer;min-width:96px}.wa-f button:hover{background:#1ebe5a}'+
  '.wa-i{font-size:13px;color:#5a6570;padding:0 14px 12px}'+
  '@media (max-width:760px){.wa-b{right:14px;bottom:14px;width:58px;height:58px}.wa-b .wa-t{display:none}.wa-p{right:12px;bottom:84px}.mob.widac~.wa-b{bottom:84px}.mob.widac~.wa-p{bottom:152px}}'+
  '@media (prefers-reduced-motion:reduce){.wa-b{transition:none}}';
  var st=d.createElement('style');st.textContent=css;d.head.appendChild(st);
  var ik='<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6.3-.6v-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.1 1.1-1.1 2.7s1.2 3.2 1.3 3.4c.2.2 2.3 3.5 5.6 4.9 2.7 1.1 3.3.9 3.9.8.6-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>';
  var b=d.createElement('button');b.type='button';b.className='wa-b';b.setAttribute('aria-label','Czat WhatsApp: napisz do nas');b.setAttribute('aria-expanded','false');b.setAttribute('aria-controls','wa-p');
  b.innerHTML=ik+'<span class="wa-t" aria-hidden="true">Napisz na WhatsAppie</span>';
  var p=d.createElement('div');p.className='wa-p';p.id='wa-p';p.setAttribute('role','dialog');p.setAttribute('aria-label','Czat WhatsApp');
  p.innerHTML='<div class="wa-h"><b>'+FIRMA+'</b><span>Odpowiadamy na WhatsAppie w dni robocze</span><button type="button" class="wa-x" aria-label="Zamknij czat">×</button></div>'+
    '<div class="wa-c"><div class="wa-m">Dzień dobry! W czym możemy pomóc? Napisz pytanie, a rozmowa otworzy się w WhatsAppie.</div>'+
    '<div class="wa-q"><button type="button">Pytanie o wannę</button><button type="button">Pytanie o bieżnię</button><button type="button">Termin dostawy</button></div></div>'+
    '<form class="wa-f"><label class="wa-l" style="position:absolute;left:-9999px" for="wa-t">Wiadomość</label><textarea id="wa-t" placeholder="Napisz wiadomość"></textarea><button type="submit">Wyślij</button></form>'+
    '<p class="wa-i">Wiadomość wyślesz z własnego WhatsAppa na numer 660 489 335.</p>';
  d.body.appendChild(p);d.body.appendChild(b);
  if(d.getElementById('mob'))d.body.classList.add('wa-mob');
  var t=p.querySelector('textarea');
  function otw(o){p.classList.toggle('otw',o);b.setAttribute('aria-expanded',o);if(o)setTimeout(function(){t.focus()},50);else b.focus()}
  b.addEventListener('click',function(){otw(!p.classList.contains('otw'))});
  p.querySelector('.wa-x').addEventListener('click',function(){otw(false)});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&p.classList.contains('otw'))otw(false)});
  p.querySelectorAll('.wa-q button').forEach(function(q){q.addEventListener('click',function(){t.value=q.textContent+': ';t.focus()})});
  p.querySelector('form').addEventListener('submit',function(e){e.preventDefault();var m=t.value.trim()||'Dzień dobry, mam pytanie.';
    window.open('https://wa.me/'+NR+'?text='+encodeURIComponent(m+'\n\n(ze strony: '+location.href.split('#')[0]+')'),'_blank','noopener')});
})();
