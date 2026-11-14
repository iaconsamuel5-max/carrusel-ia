import numpy as np, wave
SR=44100
rng=np.random.default_rng(11)
def nf(n): return 440*2**((n-69)/12)  # midi->Hz
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def add(o,s,i):
    e=min(len(o),i+len(s)); 
    if i<len(o): o[i:e]+=s[:e-i]
def kick(): n=int(.35*SR);t=np.arange(n)/SR;f=45+90*np.exp(-t*30);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.18)
def snare(): n=int(.25*SR);t=np.arange(n)/SR;nz=rng.standard_normal(n);nz=nz-np.convolve(nz,np.ones(6)/6,'same');return .6*nz*np.exp(-t/.08)+.4*np.sin(2*np.pi*185*t)*np.exp(-t/.05)
def clap():
    n=int(.2*SR);nz=rng.standard_normal(n);nz=nz-np.convolve(nz,np.ones(4)/4,'same');e=np.zeros(n)
    for k in (0,.01,.02): e+=env(n,0.001,.03)*0+0
    t=np.arange(n)/SR;e=np.exp(-t/.06);[e.__setitem__(slice(int(k*SR),int(k*SR)+30),1) for k in (0,.012,.024)];return .7*nz*e
def hat(op=False): n=int((.12 if op else .04)*SR);nz=rng.standard_normal(n);nz=np.diff(np.concatenate([[0],nz]));return .25*nz*env(n,.001,.05 if op else .012)
def clank(): n=int(.4*SR);t=np.arange(n)/SR;return sum(.15*np.sin(2*np.pi*f*t) for f in (310,743,1187,1903))*np.exp(-t/.12)
def saw(f,d,harm=12): n=int(d*SR);t=np.arange(n)/SR;return sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,harm))
def square(f,d,harm=9): n=int(d*SR);t=np.arange(n)/SR;return sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,harm,2))
def pluck(f,d,bright=6): n=int(d*SR);t=np.arange(n)/SR;return sum(np.sin(2*np.pi*f*k*t)*np.exp(-t*k*2.5)/k for k in range(1,bright))*np.exp(-t/.4)
STYLES={
 'synthwave':dict(bpm=112,prog=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])],kit='synth'),
 'industrial':dict(bpm=100,prog=[(50,[50,53,57]),(50,[50,53,57]),(46,[46,50,53]),(48,[48,52,55])],kit='ind'),
 'funky':dict(bpm=120,prog=[(48,[60,64,67]),(45,[57,60,64]),(53,[53,57,60]),(55,[55,59,62])],kit='funk'),
 'corporate':dict(bpm=104,prog=[(48,[60,64,67,71]),(45,[57,60,64,67]),(41,[53,57,60,64]),(43,[55,59,62,65])],kit='corp'),
 'romantic':dict(bpm=84,prog=[(53,[65,69,72,76]),(57,[64,69,72,76]),(50,[62,65,69,72]),(55,[62,67,71,74])],kit='soft'),
}
def track(D,style):
    S=STYLES[style];bpm=S['bpm'];b=60/bpm;N=int(D*SR);dr=np.zeros(N);mus=np.zeros(N);kenv=np.zeros(N)
    nb=int(D/b)+1
    for i in range(nb):
        t=i*b;idx=int(t*SR);bar=(i//4)%4;root,ch=S['prog'][bar];kit=S['kit']
        # drums
        if kit!='soft' or i%2==0:
            k=kick()*(0.6 if kit=='soft' else 1);add(dr,k,idx);add(kenv,np.exp(-np.arange(int(.25*SR))/SR/.08),idx)
        if i%4 in (1,3):
            add(dr,(clap() if kit=='funk' else snare())*(0.4 if kit=='soft' else 0.8),idx)
        for h in range(2):
            add(dr,hat(op=(h==1 and kit in('synth','funk'))),idx+int(h*b/2*SR))
        if kit=='ind' and i%2==1: add(dr,clank(),idx+int(b/2*SR))
        # bass 8ths
        for h in range(2):
            bf=nf(root-12 if kit!='soft' else root-12)
            if kit=='funk' and h==1: bf*=2
            s=saw(bf,b/2*0.9,8)*env(int(b/2*0.9*SR),.005,.2 if kit!='soft' else .5)
            s=np.convolve(s,np.ones(12)/12,'same');add(mus,.35*s,idx+int(h*b/2*SR))
        # arp / plucks 16ths
        if kit in('synth','ind'):
            for q in range(4):
                n=ch[(i*4+q)%len(ch)]+12;add(mus,.12*square(nf(n),b/4*0.9)*env(int(b/4*.9*SR),.002,.08),idx+int(q*b/4*SR))
        elif kit in('corp','soft'):
            if i%2==0:
                for j,n in enumerate(ch):add(mus,.12*pluck(nf(n),b*2),idx+int(j*0.03*SR))
        elif kit=='funk':
            for q in (0,3):
                for n in ch:add(mus,.08*pluck(nf(n+12),b/2,4),idx+int(q*b/4*SR))
        # pad on bar start
        if i%4==0:
            d=b*4;n=int(d*SR);tt=np.arange(n)/SR;pad=sum(np.sin(2*np.pi*nf(m)*tt)+.5*np.sin(2*np.pi*nf(m)*1.003*tt) for m in ch)
            pad*=np.minimum(1,tt/.4)*np.minimum(1,(d-tt)/.4);add(mus,(.05 if kit!='soft' else .09)*pad,idx)
    duck=1-0.55*np.clip(kenv,0,1)
    out=dr*0.55+mus*duck
    return out/np.abs(out).max()
def read(p):
    with wave.open(p) as f: a=np.frombuffer(f.readframes(f.getnframes()),np.int16).reshape(-1,f.getnchannels())[:,0]/32767
    return a
def write(p,a):
    a=a/np.abs(a).max()*.9;pcm=(a*32767).astype(np.int16)
    with wave.open(p,'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(np.stack([pcm,pcm],1).tobytes())
def mix(D,style,sfx=None,music_vol=.55,sfx_vol=.85,fade_in=.3):
    m=track(D,style);N=len(m)
    m[:int(fade_in*SR)]*=np.linspace(0,1,int(fade_in*SR));m[-int(.8*SR):]*=np.linspace(1,0,int(.8*SR))
    o=music_vol*m
    if sfx is not None:
        s=np.zeros(N);s[:min(N,len(sfx))]=sfx[:N];o=o+sfx_vol*s
    return o
