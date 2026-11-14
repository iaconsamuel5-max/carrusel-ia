import numpy as np, wave
SR=44100; D=12.0; N=int(SR*D); out=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,t):
    i=int(t*SR); e=min(N,i+len(sig)); out[i:e]+=sig[:e-i]
def env(n,a=0.005,r=0.1):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/r)
def tone(f,d,a=0.005,r=0.1,vol=0.3):
    n=int(d*SR); t=np.arange(n)/SR; return vol*np.sin(2*np.pi*f*t)*env(n,a,r)
# ambient drone
t=np.arange(N)/SR
out+=0.06*np.sin(2*np.pi*55*t)*(0.6+0.4*np.sin(2*np.pi*0.2*t))+0.03*np.sin(2*np.pi*82.5*t)
# opening whoosh
n=int(1.0*SR); w=rng.standard_normal(n); w=np.convolve(w,np.ones(40)/40,'same'); add(0.35*w*np.sin(np.linspace(0,np.pi,n)),0.0)
# typing clicks 0.3-2.5s
for k in np.arange(0.35,2.5,0.07):
    if rng.random()<0.85:
        m=int(0.012*SR); add(0.25*rng.standard_normal(m)*np.exp(-np.arange(m)/(0.002*SR)),k)
add(tone(1320,0.12,r=0.05,vol=0.2),1.05); add(tone(1760,0.15,r=0.06,vol=0.2),2.6)  # OK beeps
# glitch bursts
for g in (2.92,7.92):
    m=int(0.25*SR); s=rng.standard_normal(m)*0.3; s*=(np.sign(np.sin(np.arange(m)/SR*2*np.pi*30))+1)/2; add(s,g)
# HUD power-up sweep at 3.1
n=int(0.8*SR); tt=np.arange(n)/SR; f=200+1200*tt/0.8; add(0.18*np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*tt/0.8),3.1)
# soft sensor ticks
for k in np.arange(3.5,6.2,0.5): add(tone(2400,0.03,r=0.01,vol=0.12),k)
# alarm 6.3-7.9
for k in np.arange(6.3,7.9,0.25): add(tone(880 if int(k*4)%2 else 660,0.2,a=0.01,r=0.15,vol=0.22),k)
# riser into brand hit
n=int(1.8*SR); tt=np.arange(n)/SR; r=rng.standard_normal(n); r=np.convolve(r,np.ones(15)/15,'same')*(tt/1.8)**2*0.4; add(r,8.2)
# sub hit + metallic impact at 10.0
n=int(2.0*SR); tt=np.arange(n)/SR; sub=0.8*np.sin(2*np.pi*(55-25*tt)*tt)*np.exp(-tt/0.6)
met=sum(0.08*np.sin(2*np.pi*fq*tt)*np.exp(-tt/0.5) for fq in (523,1046,1567,2093))
add(sub+met,10.0)
# sonic logo: 3 notes
for i,(fq,k) in enumerate([(659,10.6),(784,10.85),(988,11.1)]): add(tone(fq,0.6,a=0.01,r=0.35,vol=0.18)+tone(fq*2,0.6,a=0.01,r=0.2,vol=0.05),k)
# fade out
out[-int(0.5*SR):]*=np.linspace(1,0,int(0.5*SR))
out/=max(1e-9,np.abs(out).max())/0.85
pcm=(out*32767).astype(np.int16); st=np.stack([pcm,pcm],1)
with wave.open("sonido.wav","wb") as f: f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(st.tobytes())
