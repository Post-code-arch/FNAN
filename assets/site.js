/* FNAN — comportements communs */
(function(){
  var d=document, root=d.documentElement;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* En-tête : fond au défilement, menu mobile */
  var hdr=d.getElementById('hdr'), burger=d.getElementById('burger');
  function onScroll(){hdr.classList.toggle('scrolled',scrollY>40)}
  addEventListener('scroll',onScroll,{passive:true}); onScroll();
  burger.addEventListener('click',function(){
    var o=!hdr.classList.contains('open'); hdr.classList.toggle('open',o); burger.setAttribute('aria-expanded',o);
    d.body.style.overflow=o?'hidden':'';
  });
  [].forEach.call(d.querySelectorAll('.nav a'),function(a){a.addEventListener('click',function(){hdr.classList.remove('open');burger.setAttribute('aria-expanded',false);d.body.style.overflow=''})});

  /* Apparition au défilement */
  root.classList.add('js');
  var items=[].slice.call(d.querySelectorAll('.rv'));
  if('IntersectionObserver' in window && !reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    items.forEach(function(el){io.observe(el)});
  }else items.forEach(function(el){el.classList.add('in')});

  /* Hero */
  var hero=d.getElementById('hero'); if(!hero)return;
  var layers=d.getElementById('layers');
  if(layers){
    [].forEach.call(layers.querySelectorAll('a'),function(a){
      var set=function(){layers.dataset.active=a.dataset.layer}, clr=function(){delete layers.dataset.active};
      a.addEventListener('mouseenter',set);a.addEventListener('focus',set);a.addEventListener('mouseleave',clr);a.addEventListener('blur',clr);
    });
  }
  /* Vidéo du KV : si assets/kv.mp4 existe, elle prend le relais de l'image */
  var v=d.getElementById('kv-video');
  if(v&&!reduce){
    v.addEventListener('canplay',function(){v.classList.add('on');v.play&&v.play().catch(function(){})},{once:true});
    v.load();
  }
  if(reduce)return;
  var kv=hero.querySelector('.kv-box'), ticking=false;
  function frame(){
    ticking=false;
    var p=Math.min(1,Math.max(0,scrollY/(hero.offsetHeight*.85)));
    hero.style.setProperty('--p',p.toFixed(3));
    hero.style.setProperty('--sc',(1+p*.14).toFixed(3));
    hero.style.setProperty('--sy',(p*70).toFixed(1)+'px');
  }
  addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(frame)}},{passive:true});
  frame();
  /* Parallaxe discrète au curseur */
  if(matchMedia('(hover:hover)').matches){
    addEventListener('pointermove',function(e){
      hero.style.setProperty('--px',((e.clientX/innerWidth-.5)*-14).toFixed(1)+'px');
      hero.style.setProperty('--py',((e.clientY/innerHeight-.5)*-10).toFixed(1)+'px');
    },{passive:true});
  }
})();
