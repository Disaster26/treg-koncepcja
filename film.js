// Filmy: leniwe ladowanie filmow pod pierwszym ekranem, bez ruchu przy prefers-reduced-motion
(function () {
  var rm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wszystkie = [].slice.call(document.querySelectorAll('video'));
  if (rm) wszystkie.forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.controls = true; });
  function wczytaj(v) {
    [].slice.call(v.querySelectorAll('source[data-src]')).forEach(function (s) { s.src = s.getAttribute('data-src'); s.removeAttribute('data-src'); });
    v.load();
    if (!rm) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  }
  var leniwe = [].slice.call(document.querySelectorAll('video[data-leniwy]'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (wpisy) {
      wpisy.forEach(function (w) { if (w.isIntersecting) { io.unobserve(w.target); wczytaj(w.target); } });
    }, { rootMargin: '300px 0px' });
    leniwe.forEach(function (v) { io.observe(v); });
  } else leniwe.forEach(wczytaj);
})();
