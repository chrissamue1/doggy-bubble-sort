"""Paws & Order: Doggy Bubble Sort -- Streamlit app.
Run:  pip install streamlit  &&  streamlit run app.py
"""
import json
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Paws & Order", page_icon="🐕", layout="wide")

BREEDS = [
    dict(name="Chihuahua", kg=2, fur="#e8c39b", ear="#f4a9a8", style="point"),
    dict(name="Pomeranian", kg=3, fur="#f49a3c", ear="#e07b1f", style="fluff"),
    dict(name="Pug", kg=8, fur="#e0c298", ear="#2f2a28", style="fold"),
    dict(name="French Bulldog", kg=12, fur="#b9bcc4", ear="#f2a7b5", style="bat"),
    dict(name="Corgi", kg=14, fur="#f08a3a", ear="#f6e3cf", style="point"),
    dict(name="Beagle", kg=15, fur="#f6f0e6", ear="#9a5a2a", style="floppy"),
    dict(name="Border Collie", kg=20, fur="#25242a", ear="#25242a", style="fold"),
    dict(name="Golden Retriever", kg=30, fur="#f2c76b", ear="#d9a63f", style="floppy"),
    dict(name="German Shepherd", kg=35, fur="#b8702e", ear="#2b2420", style="point"),
    dict(name="Great Dane", kg=60, fur="#6d7790", ear="#4a5368", style="fold"),
]


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"], .stApp {font-family:'Fredoka','Trebuchet MS',sans-serif !important;}
.stApp{background:linear-gradient(#bfe6ff 0%,#fff3d6 38%,#fff9ee 60%,#8fd47a 100%) fixed;color:#3b2a1d}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:#ffe2b8;border-right:5px solid #8a5a2b;
 background-image:radial-gradient(#f3c98f 2px,transparent 2px);background-size:22px 22px}
[data-testid="stSidebar"] *{color:#3b2a1d}
[data-testid="stSidebar"] .stButton>button{background:#2fa66a;color:#fff !important;border:3px solid #8a5a2b;
 border-radius:14px;font-weight:700;box-shadow:0 4px 0 #8a5a2b}
[data-testid="stSidebar"] .stButton>button:hover{background:#38bd7a}
[data-testid="stSidebar"] .stButton>button p{color:#fff !important}
.sign{display:flex;align-items:center;gap:16px;background:#c98a4b;border:4px solid #8a5a2b;border-radius:22px;
 padding:14px 22px;margin:4px 0 18px;box-shadow:0 6px 0 #8a5a2b;
 background-image:repeating-linear-gradient(90deg,rgba(0,0,0,.06) 0 2px,transparent 2px 46px)}
.sign .big{font-size:46px;line-height:1}
.sign h1{margin:0;padding:0;font-size:2.1rem;color:#fff8e8;text-shadow:0 3px 0 #6b4220;font-weight:700}
.sign p{margin:2px 0 0;color:#ffeccb;font-size:1rem}
.paws{letter-spacing:10px;opacity:.5;font-size:20px;text-align:center;margin-top:12px}
</style>
""", unsafe_allow_html=True)

# ---------- sidebar ----------
st.sidebar.title("🦴 Kennel Controls")
if "seed" not in st.session_state:
    st.session_state.seed = 7
mode = st.sidebar.radio("Theme", ["🏞️ Dog Park (cards)", "🕷️ Spider-Pup (dark 3D)"])
n = st.sidebar.slider("How many dogs?", 4, 10, 8)
order = st.sidebar.radio("Sort order", ["Ascending (small → big)", "Descending (big → small)"])
speed = st.sidebar.slider("Playback speed", 0.5, 3.0, 1.2, 0.1)
sound = st.sidebar.toggle("🔊 Bark sounds", True)
if st.sidebar.button("🎲 Shuffle the pack", use_container_width=True):
    st.session_state.seed += 1

rng = random.Random(st.session_state.seed)
pack = rng.sample(BREEDS, n)
rng.shuffle(pack)
for i, d in enumerate(BREEDS):
    d["id"] = i
pack = [dict(d) for d in pack]

st.sidebar.markdown("---")
st.sidebar.caption("Bubble sort: Worst O(n²) · Best O(n) · Space O(1)")

HTML = r"""
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--grass:#6fbf5a;--grass2:#4f9e43;--sky1:#bfe6ff;--sky2:#fff3d6;--ink:#3b2a1d;--wood:#b9824a;
--wood2:#8a5a2b;--bone:#fffaf0;--sniff:#ffb703;--swap:#ff6b35;--done:#2fa66a;--bg:#fff9ee}
*{box-sizing:border-box}
body{margin:0;font-family:'Fredoka','Trebuchet MS',system-ui,sans-serif;color:var(--ink);background:transparent}
.wrap{border-radius:26px;overflow:hidden;border:3px solid var(--wood2);background:var(--bg);box-shadow:0 8px 0 var(--wood2)}
.top{display:flex;gap:10px;flex-wrap:wrap;padding:12px 16px;background:linear-gradient(#fff,#fff3d6);border-bottom:3px dashed #e5c99a}
.stat{flex:1;min-width:110px;text-align:center;background:#fff;border:2px solid #e5c99a;border-radius:16px;padding:4px 8px}
.stat small{display:block;font-size:11px;opacity:.65}.stat b{font-size:20px}
.yard{position:relative;height:420px;background:linear-gradient(var(--sky1) 0%,var(--sky2) 62%,var(--grass) 62.2%,var(--grass2) 100%);overflow:hidden}
.sun{position:absolute;right:30px;top:18px;width:54px;height:54px;border-radius:50%;background:#ffd23f;box-shadow:0 0 0 10px #ffe9a0aa}
.fence{position:absolute;left:0;right:0;bottom:calc(38% - 6px);height:46px;background:
 repeating-linear-gradient(90deg,var(--wood) 0 22px,transparent 22px 34px);border-top:0;opacity:.55;
 clip-path:polygon(0 100%,0 15%,3% 0,6% 15%,6% 100%)}
.fence{clip-path:none;mask:none;height:38px;background:repeating-linear-gradient(90deg,var(--wood) 0 14px,transparent 14px 40px);opacity:.5}
.track{position:absolute;left:14px;right:14px;top:0;bottom:0}
.card{position:absolute;bottom:62px;border:3px solid #cdbba0;border-radius:16px 16px 10px 10px;background:var(--bone);
 text-align:center;transition:left .55s cubic-bezier(.5,-.3,.3,1.3),background .2s,border-color .2s,height .3s;
 box-shadow:7px 0 0 #e6d6b8, 0 10px 0 -2px rgba(0,0,0,.08);display:flex;flex-direction:column;align-items:center;padding-top:26px}
.card::before{content:'';position:absolute;right:-13px;top:7px;bottom:-1px;width:10px;background:#e6d6b8;
 transform:skewY(-35deg);transform-origin:left top;border-radius:0 6px 6px 0;opacity:.9}
.card .rank{position:absolute;left:6px;top:6px;background:#4a86d6;color:#fff;font-size:11px;font-weight:600;padding:1px 7px;border-radius:10px}
.card .tag{position:absolute;right:6px;top:6px;font-size:10px;font-weight:700;padding:1px 7px;border-radius:10px;display:none}
.card svg{width:84%;max-width:96px;height:auto;margin-top:4px}
.card .nm{font-weight:600;line-height:1.05;margin:2px 4px 0;font-size:clamp(9px,1.25vw,14px)}
.card .kg{margin:5px 0 8px;background:#fff1d6;border:2px solid #e8d2a6;border-radius:12px;padding:0 10px;font-weight:700;font-size:13px}
.card.sniff{border-color:var(--sniff);background:#fff6cf;transform:translateY(-18px)}
.card.sniff svg{transform:rotateY(-14deg) scale(1.1)}
.card svg{filter:drop-shadow(0 6px 4px rgba(60,30,0,.35));transition:transform .3s;transform-style:preserve-3d}
.card.sniff .tag{display:block;background:#fff0b3;color:#a06b00;content:'SNIFF'}
.card.swap{border-color:var(--swap);background:#ffe7d6;animation:hop .55s}
.card.swap .tag{display:block;background:#ffd0b5;color:#b23c0b}
.card.locked{border-color:#e6a800;background:#fff7dc}
.card.locked .tag{display:block;background:#ffe9a0;color:#8a5f00}
.card.locked svg{animation:wag 1.2s ease-in-out infinite}
@keyframes hop{0%{transform:translateY(0)}40%{transform:translateY(-46px) rotate(-3deg)}100%{transform:translateY(0)}}
@keyframes wag{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}
.slot{position:absolute;bottom:40px;font-size:11px;opacity:.75;text-align:center;font-weight:500;color:#1f4d17}
.shadow{position:absolute;bottom:52px;height:12px;border-radius:50%;background:rgba(0,0,0,.18);transition:left .55s}
.paw{position:absolute;font-size:22px;opacity:.0;pointer-events:none}
.log{margin:12px 16px 0;padding:12px 14px;background:#fff;border:3px solid #e5c99a;border-radius:18px;display:flex;gap:12px;align-items:center}
.log .who{background:#ffe2b8;color:#7a4a12;font-weight:700;border-radius:12px;padding:6px 10px;white-space:nowrap}
.log b{display:block}.log span{opacity:.7;font-size:14px}
.bar{height:12px;margin:10px 16px;background:#eadfca;border-radius:8px;overflow:hidden}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#f7931e,#ffcc33);transition:width .3s}
.ctl{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:6px 16px 16px}
button{font:inherit;font-weight:600;color:var(--ink);background:#fff;border:3px solid var(--wood2);border-radius:14px;padding:7px 14px;cursor:pointer;box-shadow:0 4px 0 var(--wood2);transition:transform .08s}
button:active{transform:translateY(3px);box-shadow:0 1px 0 var(--wood2)}
button.go{background:var(--done);color:#fff}
button:focus-visible{outline:3px solid #4a86d6;outline-offset:2px}
.ctl label{font-size:13px;display:flex;gap:6px;align-items:center}
.bone{position:absolute;font-size:26px;animation:fall 2.4s ease-in forwards;pointer-events:none}
@keyframes fall{from{transform:translateY(-40px) rotate(0)}to{transform:translateY(440px) rotate(540deg)}}
@media (prefers-reduced-motion:reduce){.card,.card *{animation:none!important}}
</style>
<div class="wrap">
 <div class="top">
  <div class="stat"><small>Pass</small><b id="s-pass">#1</b></div>
  <div class="stat"><small>Sniffs (comparisons)</small><b id="s-cmp">0</b></div>
  <div class="stat"><small>Zoomies (swaps)</small><b id="s-swp">0</b></div>
  <div class="stat"><small>Good dogs in place</small><b id="s-lock">0</b></div>
  <div class="stat"><small>Step</small><b id="s-step">0</b></div>
 </div>
 <div class="yard" id="yard"><div class="sun"></div><div class="fence"></div><div class="track" id="track"></div></div>
 <div class="log"><div class="who">🐶 Coach Rover</div><div><b id="l1"></b><span id="l2"></span></div></div>
 <div class="bar"><i id="prog"></i></div>
 <div class="ctl">
  <button id="bPlay" class="go">▶ Play sort</button>
  <button id="bPrev">◀ Prev</button><button id="bNext">Next ▶</button><button id="bReset">↺ Reset</button>
  <label>Speed <input type="range" id="spd" min="0.5" max="3" step="0.1"><b id="spdv"></b></label>
 </div>
</div>
<script>
const CFG = __CFG__;
const asc = CFG.asc, dogs = CFG.dogs, N = dogs.length;
const maxKg = Math.max(...dogs.map(d=>d.kg));
let speed = CFG.speed, sound = CFG.sound, playing = false, timer = null, cur = 0;
const rankOf = {}; [...dogs].sort((a,b)=>a.kg-b.kg).forEach((d,i)=>rankOf[d.name]=i+1);

const sh=(h,a)=>{const n=parseInt(h.slice(1),16),r=n>>16,g=n>>8&255,b=n&255;
  const f=v=>Math.max(0,Math.min(255,Math.round(a>0?v+(255-v)*a:v*(1+a))));return `rgb(${f(r)},${f(g)},${f(b)})`;};
function face(d,i){
  const f=d.fur,e=d.ear,dark=['#25242a','#2b2420','#6d7790'].includes(f), mz=dark?'#e8e2d8':'#fff4e4';
  const grad=(id,c)=>`<radialGradient id="${id}${i}" cx=".35" cy=".28" r=".9"><stop offset="0" stop-color="${sh(c,.45)}"/><stop offset=".55" stop-color="${c}"/><stop offset="1" stop-color="${sh(c,-.38)}"/></radialGradient>`;
  let ears='';
  if(d.style==='point') ears=`<polygon points="12,42 22,2 48,26" fill="url(#e${i})"/><polygon points="88,42 78,2 52,26" fill="url(#e${i})"/><polygon points="20,34 24,13 37,25" fill="#f3a3ad"/><polygon points="80,34 76,13 63,25" fill="#f3a3ad"/>`;
  if(d.style==='floppy') ears=`<ellipse cx="13" cy="56" rx="13" ry="27" fill="url(#e${i})" transform="rotate(8 13 56)"/><ellipse cx="87" cy="56" rx="13" ry="27" fill="url(#e${i})" transform="rotate(-8 87 56)"/>`;
  if(d.style==='bat') ears=`<ellipse cx="22" cy="22" rx="13" ry="22" fill="url(#e${i})" transform="rotate(-12 22 22)"/><ellipse cx="78" cy="22" rx="13" ry="22" fill="url(#e${i})" transform="rotate(12 78 22)"/><ellipse cx="22" cy="24" rx="6" ry="14" fill="#f3a3ad" transform="rotate(-12 22 24)"/><ellipse cx="78" cy="24" rx="6" ry="14" fill="#f3a3ad" transform="rotate(12 78 24)"/>`;
  if(d.style==='fold') ears=`<polygon points="14,30 42,18 30,56" fill="url(#e${i})"/><polygon points="86,30 58,18 70,56" fill="url(#e${i})"/>`;
  if(d.style==='fluff') ears=`<circle cx="50" cy="52" r="46" fill="url(#e${i})"/><circle cx="20" cy="18" r="12" fill="url(#e${i})"/><circle cx="80" cy="18" r="12" fill="url(#e${i})"/>`;
  return `<svg viewBox="0 0 100 104"><defs>${grad('h',f)}${grad('e',e)}${grad('m',mz)}
  <radialGradient id="n${i}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6b6b6b"/><stop offset="1" stop-color="#0c0908"/></radialGradient>
  <linearGradient id="c${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa0ff"/><stop offset="1" stop-color="#1f56c4"/></linearGradient></defs>
  <ellipse cx="50" cy="99" rx="34" ry="5" fill="#000" opacity=".22"/>
  ${ears}
  <circle cx="50" cy="56" r="36" fill="url(#h${i})"/>
  <path d="M22 88Q50 108 78 88L74 80Q50 94 26 80Z" fill="url(#c${i})"/><circle cx="50" cy="95" r="5" fill="#ffd23f" stroke="#c99a00" stroke-width="1"/>
  <ellipse cx="38" cy="34" rx="15" ry="8" fill="#fff" opacity=".2" transform="rotate(-25 38 34)"/>
  <ellipse cx="50" cy="69" rx="21" ry="16" fill="url(#m${i})"/>
  <circle cx="37" cy="53" r="6" fill="#1a1210"/><circle cx="63" cy="53" r="6" fill="#1a1210"/>
  <circle cx="39" cy="50.5" r="2.3" fill="#fff"/><circle cx="65" cy="50.5" r="2.3" fill="#fff"/><circle cx="35.5" cy="55.5" r="1.1" fill="#fff" opacity=".8"/><circle cx="61.5" cy="55.5" r="1.1" fill="#fff" opacity=".8"/>
  <circle cx="26" cy="66" r="5" fill="#ff8fa3" opacity=".28"/><circle cx="74" cy="66" r="5" fill="#ff8fa3" opacity=".28"/>
  <ellipse cx="50" cy="63" rx="8" ry="5.8" fill="url(#n${i})"/><ellipse cx="47.5" cy="61" rx="3" ry="1.5" fill="#fff" opacity=".65"/>
  <path d="M50 68v4M40 73q10 8 20 0" stroke="#2a1a14" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <path d="M44 74q6 14 12 0z" fill="#ff6f8e"/><path d="M50 75v6" stroke="#d9486a" stroke-width="1"/></svg>`;
}

// ---- build step list (snapshots) ----
function build(){
  let a=dogs.map((_,i)=>i), steps=[], cmp=0, swp=0, locked=0, pass=1;
  const push=(o)=>steps.push(Object.assign({arr:[...a],cmp,swp,locked,pass,type:'info'},o));
  push({type:'start',t:'Welcome to Paws & Order! The dogs are lined up in the yard.',s:'Press Play or Next to start sniffing.'});
  for(let p=0;p<N-1;p++){
    pass=p+1; let sw=false;
    for(let j=0;j<N-1-p;j++){
      const A=dogs[a[j]],B=dogs[a[j+1]]; cmp++;
      const need = asc? A.kg>B.kg : A.kg<B.kg;
      push({type:'cmp',pair:[j,j+1],t:`Sniff test: ${A.name} (${A.kg}kg) vs ${B.name} (${B.kg}kg).`,
        s: need?'Wrong order → zoomies needed!':'Already in the right order.'});
      if(need){ [a[j],a[j+1]]=[a[j+1],a[j]]; swp++; sw=true;
        push({type:'swap',pair:[j,j+1],t:`Zoomies! ${B.name} and ${A.name} swap spots!`,
          s:`Bubbling ${asc?'heavier':'lighter'} dog ${A.name} to the right.`}); }
    }
    locked++; push({type:'lock',t:`${dogs[a[N-1-p]].name} is locked in place.`,s:'This good dog has found their final spot.'});
    if(!sw){ locked=N; push({type:'lock',t:'No zoomies this pass — the pack is already sorted!',s:'Early exit: this is why the best case is O(n).'}); break; }
  }
  locked=N; push({type:'done',t:'Pack sorted! All good dogs are happily in order!',s:`Completed in ${cmp} sniffs and ${swp} zoomies. Good dogs all around!`});
  return steps;
}
let steps = build();

// ---- DOM ----
const track=document.getElementById('track'), yard=document.getElementById('yard');
const cards=[], shadows=[], slots=[];
dogs.forEach((d,i)=>{
  const c=document.createElement('div'); c.className='card';
  c.innerHTML=`<span class="rank">#${rankOf[d.name]}</span><span class="tag"></span>${face(d,i)}<div class="nm">${d.name}</div><div class="kg">${d.kg} kg</div>`;
  track.appendChild(c); cards.push(c);
  const sh=document.createElement('div'); sh.className='shadow'; track.appendChild(sh); shadows.push(sh);
  const sl=document.createElement('div'); sl.className='slot'; sl.textContent='Spot #'+(i+1); track.appendChild(sl); slots.push(sl);
});
function layout(){
  const W=track.clientWidth, sw=W/N, cw=Math.min(sw*0.8,130);
  dogs.forEach((d,i)=>{
    const h=130+190*Math.sqrt(d.kg/maxKg);
    cards[i].style.width=cw+'px'; cards[i].style.height=h+'px';
  });
  slots.forEach((s,i)=>{s.style.left=(i*sw)+'px';s.style.width=sw+'px'});
  render(true);
}
function actx(){ const ac=bark.ac||(bark.ac=new (window.AudioContext||window.webkitAudioContext)()); if(ac.state==='suspended') ac.resume(); return ac; }
function bark(kg,n=1,delay=0,vol=1){
  if(!sound) return;
  try{
    const ac=actx(), base=520-370*Math.sqrt(kg/60), len=0.09+0.12*Math.sqrt(kg/60);
    for(let k=0;k<n;k++){
      const t=ac.currentTime+delay+k*(len+0.09);
      const out=ac.createGain(); out.gain.setValueAtTime(0.0001,t);
      out.gain.exponentialRampToValueAtTime(0.5*vol,t+0.015); out.gain.exponentialRampToValueAtTime(0.001,t+len+0.05);
      out.connect(ac.destination);
      const o=ac.createOscillator(); o.type='sawtooth';
      o.frequency.setValueAtTime(base*1.5,t); o.frequency.exponentialRampToValueAtTime(base*0.75,t+len);
      [[700,3],[1500,4],[2600,5]].forEach(([fr,q],ix)=>{ const bp=ac.createBiquadFilter(); bp.type='bandpass';
        bp.frequency.value=fr*(1.25-0.5*Math.sqrt(kg/60)); bp.Q.value=q; const g=ac.createGain(); g.gain.value=[1.6,1,.5][ix];
        o.connect(bp); bp.connect(g); g.connect(out); });
      const nb=ac.createBuffer(1,ac.sampleRate*0.15,ac.sampleRate), dta=nb.getChannelData(0);
      for(let q=0;q<dta.length;q++) dta[q]=Math.random()*2-1;
      const ns=ac.createBufferSource(); ns.buffer=nb; const nf=ac.createBiquadFilter(); nf.type='bandpass'; nf.frequency.value=1800; nf.Q.value=.8;
      const ng=ac.createGain(); ng.gain.value=.25; ns.connect(nf); nf.connect(ng); ng.connect(out);
      o.start(t); o.stop(t+len+0.06); ns.start(t); ns.stop(t+len);
    }
  }catch(e){}
}
function render(quiet){
  const st=steps[cur], W=track.clientWidth, sw=W/N, cw=Math.min(sw*0.8,130);
  st.arr.forEach((id,pos)=>{
    const c=cards[id], x=pos*sw+(sw-cw)/2;
    c.style.left=x+'px'; shadows[pos].style.left=(pos*sw+(sw-cw)/2)+'px'; shadows[pos].style.width=cw+'px';
    c.classList.remove('sniff','swap','locked');
    const tag=c.querySelector('.tag');
    if(st.pair&&st.pair.includes(pos)){ c.classList.add(st.type==='swap'?'swap':'sniff'); tag.textContent=st.type==='swap'?'🔀 SWAP':'🐾 SNIFF'; }
    else if(pos>=N-st.locked || st.type==='done'){ c.classList.add('locked'); tag.textContent='🦴 LOCKED'; }
  });
  document.getElementById('s-pass').textContent='#'+st.pass;
  document.getElementById('s-cmp').textContent=st.cmp;
  document.getElementById('s-swp').textContent=st.swp;
  document.getElementById('s-lock').textContent=Math.min(st.locked,N)+' / '+N;
  document.getElementById('s-step').textContent=cur+' / '+(steps.length-1);
  document.getElementById('l1').textContent=st.t; document.getElementById('l2').textContent=st.s;
  const pr=document.getElementById('prog'); pr.style.width=(cur/(steps.length-1)*100)+'%';
  pr.style.background= st.type==='done'?'#e6a800':'';
  if(!quiet){
    if(st.type==='cmp'){ const l=dogs[st.arr[st.pair[0]]], r=dogs[st.arr[st.pair[1]]]; bark(Math.min(l.kg,r.kg),1,0,.45); }
    if(st.type==='swap'){ const l=dogs[st.arr[st.pair[0]]], r=dogs[st.arr[st.pair[1]]]; bark(l.kg,1,0,.9); bark(r.kg,1,.22,.9); }
    if(st.type==='lock'){ bark(dogs[st.arr[N-st.locked]]?.kg||10,1,0,.6); }
    if(st.type==='done'){ bark(60,1,0,1); bark(2,2,.45,.9); bark(14,1,.9,.9); rain(); }
  }
}
function rain(){ for(let i=0;i<16;i++){ const b=document.createElement('div'); b.className='bone'; b.textContent=['🦴','🐾','🎾'][i%3];
  b.style.left=Math.random()*95+'%'; b.style.animationDelay=(Math.random()*.9)+'s'; yard.appendChild(b); setTimeout(()=>b.remove(),3600);} }
function next(){ if(cur<steps.length-1){cur++;render();} else stop(); }
function prev(){ if(cur>0){cur--;render(true);} }
function tick(){ if(!playing) return; if(cur>=steps.length-1){stop();return;} next();
  const d=steps[cur].type==='swap'?750:480; timer=setTimeout(tick,d/speed); }
function play(){ if(cur>=steps.length-1) cur=0; playing=true; document.getElementById('bPlay').textContent='⏸ Pause'; tick(); }
function stop(){ playing=false; clearTimeout(timer); document.getElementById('bPlay').textContent='▶ Play sort'; }
document.getElementById('bPlay').onclick=()=>playing?stop():play();
document.getElementById('bNext').onclick=()=>{stop();next()};
document.getElementById('bPrev').onclick=()=>{stop();prev()};
document.getElementById('bReset').onclick=()=>{stop();cur=0;render(true)};
const spd=document.getElementById('spd'); spd.value=speed; document.getElementById('spdv').textContent=speed.toFixed(1)+'x';
spd.oninput=e=>{speed=+e.target.value;document.getElementById('spdv').textContent=speed.toFixed(1)+'x'};
addEventListener('keydown',e=>{ if(e.code==='Space'){e.preventDefault();playing?stop():play()} if(e.code==='ArrowRight'){stop();next()} if(e.code==='ArrowLeft'){stop();prev()} });
addEventListener('resize',layout); layout();
</script>
"""

SPIDER = r"""
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&display=swap" rel="stylesheet">
<style>
body{margin:0;font-family:'Fredoka',system-ui,sans-serif}
.box{background:#0b1020;border:3px solid #1e293b;border-radius:22px;overflow:hidden;box-shadow:0 8px 0 #1e293b}
canvas{display:block;width:100%}
.ctl{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:10px 14px 14px;background:#0f172a;color:#cbd5e1}
button{font:inherit;font-weight:700;color:#e2e8f0;background:#1e293b;border:2px solid #334155;border-radius:12px;padding:6px 14px;cursor:pointer}
button.go{background:#10b981;border-color:#34d399;color:#04231a}
button:focus-visible{outline:3px solid #22d3ee}
label{font-size:13px;display:flex;gap:6px;align-items:center}
</style>
<div class="box"><canvas id="cv"></canvas>
<div class="ctl"><button id="bPlay" class="go">▶ Play sort</button><button id="bPrev">◀ Prev</button><button id="bNext">Next ▶</button><button id="bReset">↺ Reset</button>
<label>Speed <input type="range" id="spd" min="0.4" max="3.5" step="0.1"><b id="spdv"></b></label></div></div>
<script>
const CFG=__CFG__, dogs=CFG.dogs, asc=CFG.asc, N=dogs.length, maxKg=Math.max(...dogs.map(d=>d.kg));
let speed=CFG.speed, sound=CFG.sound, playing=false, timer=null, cur=0;
const rankOf={}; [...dogs].sort((a,b)=>a.kg-b.kg).forEach((d,i)=>rankOf[d.name]=i+1);
function build(){let a=dogs.map((_,i)=>i),S=[],cmp=0,swp=0,locked=0,pass=1;
 const push=o=>S.push(Object.assign({arr:[...a],cmp,swp,locked,pass,type:'start'},o));
 push({t:'Spider-Pup is ready to swing into action!',s:'Press Play or Next.'});
 for(let p=0;p<N-1;p++){pass=p+1;let sw=false;
  for(let j=0;j<N-1-p;j++){const A=dogs[a[j]],B=dogs[a[j+1]];cmp++;const need=asc?A.kg>B.kg:A.kg<B.kg;
   push({type:'cmp',pair:[j,j+1],t:`compare a[${j}], a[${j+1}]  →  ${A.name} (${A.kg}kg) vs ${B.name} (${B.kg}kg)`,s:need?'Wrong order, swinging them over!':'Already in order.'});
   if(need){[a[j],a[j+1]]=[a[j+1],a[j]];swp++;sw=true;push({type:'swap',pair:[j,j+1],t:`swap a[${j}], a[${j+1}]  →  ${B.name} ⇄ ${A.name}`,s:'Web-slinging swap!'});}}
  locked++;push({type:'lock',t:`${dogs[a[N-1-p]].name} is locked in place.`,s:'Final spot found.'});
  if(!sw){locked=N;push({type:'lock',t:'No swaps this pass, already sorted!',s:'Best case O(n).'});break;}}
 locked=N;push({type:'done',t:'Pack sorted! Spider-Pup saves the day!',s:`${cmp} comparisons, ${swp} swaps.`});return S;}
const steps=build();
function bark(kg,n=1,delay=0,vol=1){if(!sound)return;try{const ac=bark.ac||(bark.ac=new (window.AudioContext||window.webkitAudioContext)());if(ac.state==='suspended')ac.resume();
 const base=520-370*Math.sqrt(kg/60),len=.09+.12*Math.sqrt(kg/60);
 for(let k=0;k<n;k++){const t=ac.currentTime+delay+k*(len+.09),out=ac.createGain();out.gain.setValueAtTime(.0001,t);out.gain.exponentialRampToValueAtTime(.5*vol,t+.015);out.gain.exponentialRampToValueAtTime(.001,t+len+.05);out.connect(ac.destination);
  const o=ac.createOscillator();o.type='sawtooth';o.frequency.setValueAtTime(base*1.5,t);o.frequency.exponentialRampToValueAtTime(base*.75,t+len);
  [[700,3,1.6],[1500,4,1],[2600,5,.5]].forEach(([fr,q,gn])=>{const bp=ac.createBiquadFilter();bp.type='bandpass';bp.frequency.value=fr*(1.25-.5*Math.sqrt(kg/60));bp.Q.value=q;const g=ac.createGain();g.gain.value=gn;o.connect(bp);bp.connect(g);g.connect(out);});
  o.start(t);o.stop(t+len+.06);}}catch(e){}}
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=900,H=700;
function resize(){const dpr=window.devicePixelRatio||1;W=cv.parentNode.clientWidth;H=700;cv.width=W*dpr;cv.height=H*dpr;cv.style.height=H+'px';ctx.setTransform(dpr,0,0,dpr,0,0);}
addEventListener('resize',resize);resize();
const disp=dogs.map(()=>({x:null,lift:0})),pup={x:W/2};
const C={grey:['#475069','#5b6580','#2f364a'],orange:['#ff8a1f','#ffb15c','#c25f00'],cyan:['#22d3ee','#7ae8f7','#0e8fa6'],green:['#10d98a','#5df0b5','#0a9b62']};
function poly(p,c){ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);for(let i=1;i<p.length;i++)ctx.lineTo(p[i][0],p[i][1]);ctx.closePath();ctx.fillStyle=c;ctx.fill();}
function block(id,pos,col,x,lift,glow,rank){
 const d=dogs[id],bw=Math.min(((W-60)/N)*.7,92),dp=bw*.32,gy=455,h=50+215*Math.pow(d.kg/maxKg,.6),y=gy-lift,t=y-h;
 ctx.save();ctx.fillStyle='rgba(0,0,0,.35)';ctx.beginPath();ctx.ellipse(x+bw/2+dp/2,gy+6,bw*.6,8,0,0,7);ctx.fill();
 if(glow){ctx.shadowColor=col[0];ctx.shadowBlur=26;}
 poly([[x+bw,y],[x+bw+dp,y-dp*.6],[x+bw+dp,t-dp*.6],[x+bw,t]],col[2]);
 poly([[x,t],[x+dp,t-dp*.6],[x+bw+dp,t-dp*.6],[x+bw,t]],col[1]);
 poly([[x,y],[x+bw,y],[x+bw,t],[x,t]],col[0]);ctx.restore();
 ctx.textAlign='center';ctx.fillStyle='#0b1020';ctx.font='700 '+Math.max(13,bw*.2)+'px Fredoka,sans-serif';
 ctx.fillText('#'+rank,x+bw/2+dp/2,t-dp*.15);
 const fx=x+bw/2,fy=t+bw*.42,r=bw*.3;ctx.fillStyle=d.fur;ctx.beginPath();ctx.arc(fx,fy,r,0,7);ctx.fill();
 ctx.fillStyle=d.ear;ctx.beginPath();ctx.ellipse(fx-r*.95,fy-r*.5,r*.35,r*.6,0,0,7);ctx.ellipse(fx+r*.95,fy-r*.5,r*.35,r*.6,0,0,7);ctx.fill();
 ctx.fillStyle='#111';ctx.beginPath();ctx.arc(fx-r*.38,fy-r*.1,r*.13,0,7);ctx.arc(fx+r*.38,fy-r*.1,r*.13,0,7);ctx.arc(fx,fy+r*.35,r*.17,0,7);ctx.fill();
 ctx.fillStyle='#fff';ctx.font='700 '+Math.max(10,bw*.16)+'px Fredoka,sans-serif';ctx.fillText(d.name.split(' ').pop(),x+bw/2,fy+r*1.6);
 ctx.fillStyle='rgba(255,255,255,.85)';ctx.font='500 '+Math.max(10,bw*.15)+'px Fredoka,sans-serif';ctx.fillText(d.kg+' kg',x+bw/2,fy+r*2.3);
 return [x+bw/2+dp/2,t-dp*.3];}
function drawPup(px,py){ctx.save();ctx.translate(px,py);ctx.rotate(Math.PI);
 ctx.fillStyle='#d62839';ctx.beginPath();ctx.roundRect(-19,26,38,54,10);ctx.fill();ctx.fillStyle='#1d4ed8';ctx.fillRect(-19,26,8,54);ctx.fillRect(11,26,8,54);
 ctx.fillStyle='#111';ctx.beginPath();ctx.arc(0,50,6,0,7);ctx.fill();ctx.strokeStyle='#111';ctx.lineWidth=1.5;for(let a=0;a<6;a++){ctx.beginPath();ctx.moveTo(0,50);ctx.lineTo(Math.cos(a*1.05)*13,50+Math.sin(a*1.05)*13);ctx.stroke();}
 ctx.strokeStyle='#f2c76b';ctx.lineWidth=9;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-17,38);ctx.lineTo(-34,50);ctx.moveTo(17,38);ctx.lineTo(34,50);ctx.stroke();
 ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(-34,50,6,0,7);ctx.arc(34,50,6,0,7);ctx.fill();
 ctx.fillStyle='#d62839';ctx.beginPath();ctx.ellipse(-25,-14,8,15,.3,0,7);ctx.ellipse(25,-14,8,15,-.3,0,7);ctx.fill();
 ctx.fillStyle='#f2c76b';ctx.beginPath();ctx.arc(0,0,27,0,7);ctx.fill();
 ctx.fillStyle='#d62839';ctx.beginPath();ctx.ellipse(0,-4,26,15,0,0,7);ctx.fill();
 ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(-10,-5,8,5.5,.35,0,7);ctx.ellipse(10,-5,8,5.5,-.35,0,7);ctx.fill();
 ctx.fillStyle='#fff3e0';ctx.beginPath();ctx.ellipse(0,15,13,10,0,0,7);ctx.fill();ctx.fillStyle='#111';ctx.beginPath();ctx.ellipse(0,10,5,3.5,0,0,7);ctx.fill();
 ctx.fillStyle='#ff6f8e';ctx.beginPath();ctx.ellipse(0,24,4,6,0,0,7);ctx.fill();ctx.restore();}
function leash(x1,y1,x2,y2,c,tm){ctx.save();ctx.strokeStyle=c;ctx.shadowColor=c;ctx.shadowBlur=14;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x1,y1);ctx.quadraticCurveTo((x1+x2)/2,(y1+y2)/2+8,x2,y2);ctx.stroke();
 ctx.setLineDash([6,5]);ctx.lineDashOffset=-tm/40;ctx.lineWidth=2;ctx.beginPath();ctx.arc(x2,y2,20,0,7);ctx.stroke();ctx.restore();}
function frame(tm){const st=steps[cur];ctx.clearRect(0,0,W,H);
 const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#0b1020');g.addColorStop(1,'#111a33');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 const sw=(W-60)/N,bw=Math.min(sw*.7,92),pos0=[],act=[];
 st.arr.forEach((id,pos)=>{const D=disp[id],tx=30+pos*sw+(sw-bw)/2-10;if(D.x===null)D.x=tx;D.x+=(tx-D.x)*.16;
  const isA=st.pair&&st.pair.includes(pos),tl=isA?(st.type==='swap'?70:36):0;D.lift+=(tl-D.lift)*.16;});
 const order=st.arr.map((id,pos)=>pos).sort((a,b)=>{const A=st.pair&&st.pair.includes(a)?1:0,B=st.pair&&st.pair.includes(b)?1:0;return A-B;});
 const tops={};
 ctx.fillStyle='#1b2540';ctx.fillRect(0,462,W,3);
 order.forEach(pos=>{const id=st.arr[pos],D=disp[id];let col=C.grey,gl=false;
  if(pos>=N-st.locked||st.type==='done'){col=C.green;gl=true;}
  if(st.pair&&st.pair[0]===pos){col=C.orange;gl=true;} if(st.pair&&st.pair[1]===pos){col=C.cyan;gl=true;}
  tops[pos]=block(id,pos,col,D.x,D.lift,gl,rankOf[dogs[id].name]);});
 let tx=W/2;if(st.pair){tx=(tops[st.pair[0]][0]+tops[st.pair[1]][0])/2;} pup.x+=(tx-pup.x)*.1;
 const py=125;ctx.strokeStyle='#cbd5e1';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(pup.x,0);ctx.lineTo(pup.x,py-80);ctx.stroke();
 if(st.pair){leash(pup.x-34,py-50,tops[st.pair[0]][0],tops[st.pair[0]][1],'#ff8a1f',tm);leash(pup.x+34,py-50,tops[st.pair[1]][0],tops[st.pair[1]][1],'#22d3ee',tm);}
 drawPup(pup.x,py);
 ctx.textAlign='left';ctx.fillStyle='#94a3b8';ctx.font='500 14px Fredoka,sans-serif';
 ctx.fillText(`Pass #${st.pass}   Comparisons ${st.cmp}   Swaps ${st.swp}   Sorted ${Math.min(st.locked,N)}/${N}   Step ${cur}/${steps.length-1}`,16,24);
 ctx.fillStyle='#e2e8f0';ctx.font='700 15px Fredoka,sans-serif';ctx.fillText(st.t,16,48);ctx.fillStyle='#94a3b8';ctx.font='500 13px Fredoka,sans-serif';ctx.fillText(st.s,16,68);
 ctx.fillStyle='#0f172a';ctx.beginPath();ctx.roundRect(16,490,W-32,190,14);ctx.fill();ctx.strokeStyle='#1e293b';ctx.lineWidth=2;ctx.stroke();
 const lines=[['for j in range(0, n - i - 1):',0],['    compare a[j], a[j+1]','cmp'],['    if a[j] '+(asc?'>':'<')+' a[j+1]:',0],['        swap a[j], a[j+1]','swap'],['    # heavier dog bubbles to the right',-1]];
 ctx.font='500 15px ui-monospace,Consolas,monospace';lines.forEach(([tx2,k],i)=>{const y=522+i*30,on=k===st.type;
  if(on){ctx.fillStyle=k==='swap'?'rgba(255,138,31,.2)':'rgba(34,211,238,.18)';ctx.fillRect(22,y-18,W-44,26);}
  ctx.fillStyle=k===-1?'#64748b':on?'#fff':/^( *)(for|if)/.test(tx2)?'#c084fc':'#cbd5e1';ctx.fillText(tx2,34,y);});
 requestAnimationFrame(frame);}
function snd(st){if(st.type==='cmp'){const l=dogs[st.arr[st.pair[0]]],r=dogs[st.arr[st.pair[1]]];bark(Math.min(l.kg,r.kg),1,0,.45);}
 if(st.type==='swap'){bark(dogs[st.arr[st.pair[0]]].kg,1,0,.9);bark(dogs[st.arr[st.pair[1]]].kg,1,.22,.9);}
 if(st.type==='lock')bark(dogs[st.arr[N-st.locked]]?.kg||10,1,0,.6);
 if(st.type==='done'){bark(60,1,0,1);bark(2,2,.45,.9);bark(14,1,.9,.9);}}
function next(){if(cur<steps.length-1){cur++;snd(steps[cur]);}else stop();}
function prev(){if(cur>0)cur--;}
function tick(){if(!playing)return;if(cur>=steps.length-1){stop();return;}next();timer=setTimeout(tick,(steps[cur].type==='swap'?900:560)/speed);}
function play(){if(cur>=steps.length-1)cur=0;playing=true;bPlay.textContent='⏸ Pause';tick();}
function stop(){playing=false;clearTimeout(timer);bPlay.textContent='▶ Play sort';}
bPlay.onclick=()=>playing?stop():play();bNext.onclick=()=>{stop();next()};bPrev.onclick=()=>{stop();prev()};bReset.onclick=()=>{stop();cur=0};
spd.min=.4;spd.max=3.5;spd.value=speed;spdv.textContent=speed.toFixed(1)+'x';spd.oninput=e=>{speed=+e.target.value;spdv.textContent=speed.toFixed(1)+'x'};
addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();playing?stop():play()}if(e.code==='ArrowRight'){stop();next()}if(e.code==='ArrowLeft'){stop();prev()}if(e.key==='r'){stop();cur=0}if(e.key==='m'){sound=!sound}});
requestAnimationFrame(frame);
</script>
"""

cfg = dict(dogs=pack, asc=order.startswith("Asc"), speed=speed, sound=sound)

st.markdown("""
<div class="sign"><div class="big">🐕</div><div>
<h1>Paws & Order: Doggy Bubble Sort</h1>
<p>Coach Rover lines up the pack by weight, from tiny Chihuahua to mighty Great Dane. Space = play/pause, ←/→ = step. Turn your volume up for barks!</p>
</div></div>
""", unsafe_allow_html=True)
page = SPIDER if mode.startswith("🕷") else HTML
components.html(page.replace("__CFG__", json.dumps(cfg)), height=860 if page is HTML else 840, scrolling=True)
st.markdown('<div class="paws">🐾 🐾 🐾 🐾 🐾</div>', unsafe_allow_html=True)