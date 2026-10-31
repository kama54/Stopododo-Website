(()=>{
  'use strict';
  const control=document.getElementById('dimming-level');
  const shade=document.getElementById('demo-overlay');
  const value=document.getElementById('dimming-value');
  if(control&&shade&&value){
    const update=()=>{const x=Math.min(80,Math.max(0,Number(control.value)||0));shade.style.opacity=String(x/100);value.textContent=x+'%'};
    control.addEventListener('input',update); update();
  }

  const video=document.getElementById('promo-video');
  const status=document.getElementById('video-status');
  if(video){
    // The text and triangle beside the promotional film are real, keyboard accessible controls.
    document.querySelectorAll('[data-play-video]').forEach(button=>{
      button.addEventListener('click',()=>{
        video.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'});
        if(status){status.hidden=true;status.textContent='';}
        // Explicit play in the user's click handler: compatible with mobile autoplay restrictions.
        const result=video.play();
        if(result&&typeof result.catch==='function')result.catch(()=>{
          video.focus({preventScroll:true});
          if(status){status.hidden=false;status.textContent=video.getAttribute('data-play-error')||'Please start the video using the player controls.';}
        });
      });
    });
  }
  document.querySelectorAll('.mobile-nav nav a').forEach(a=>a.addEventListener('click',()=>{const menu=a.closest('details');if(menu)menu.open=false}));
  document.addEventListener('click',e=>{document.querySelectorAll('details.language[open],details.mobile-nav[open]').forEach(d=>{if(!d.contains(e.target))d.open=false})});
})();
