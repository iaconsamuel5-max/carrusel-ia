import numpy as np,wave,sys
SR=44100;rng=np.random.default_rng(3)
def mk(D):return np.zeros(int(SR*D))
def add(o,s,t):
    i=int(t*SR);e=min(len(o),i+len(s));o[i:e]+=s[:e-i]
def tone(f,d,a=.005,r=.1,v=.3):
    n=int(d*SR);t=np.arange(n)/SR;return v*np.sin(2*np.pi*f*t)*np.minimum(1,t/a)*np.exp(-t/r)
def noise(d,sm=20):
    n=int(d*SR);return np.convolve(rng.standard_normal(n),np.ones(sm)/sm,'same')
def logo(o,t):
    for fq,k in [(659,0),(784,.25),(988,.5)]:add(o,tone(fq,.6,.01,.35,.18)+tone(fq*2,.6,.01,.2,.05),t+k)
def hit(o,t):
    n=int(1.6*SR);tt=np.arange(n)/SR;add(o,.8*np.sin(2*np.pi*(55-25*tt)*tt)*np.exp(-tt/.5),t)
def fin(o,name):
    o[-int(.4*SR):]*=np.linspace(1,0,int(.4*SR));o/=np.abs(o).max()/.85;p=(o*32767).astype(np.int16)
    with wave.open(name,'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(np.stack([p,p],1).tobytes())
s=sys.argv[1]
if s=='radar':
    D=10;o=mk(D);t=np.arange(len(o))/SR;o+=.05*np.sin(2*np.pi*48*t)
    for k in np.arange(.3,8.5,4.49):add(o,tone(1500,1.2,.002,.5,.25)+tone(750,1.2,.002,.4,.1),k)   # sonar ping each sweep
    for k in (1.2,1.8,2.4):add(o,tone(2000,.05,r=.02,v=.15),k)
    add(o,.25*noise(1.5)*np.linspace(0,1,int(1.5*SR))**2,6.5);hit(o,8.0);logo(o,8.3)
elif s=='blueprint':
    D=10;o=mk(D);t=np.arange(len(o))/SR;o+=.04*np.sin(2*np.pi*65*t)
    for k in np.arange(.2,2.2,.09):add(o,.15*rng.standard_normal(400)*np.exp(-np.arange(400)/60),k)  # pencil ticks
    for i,k in enumerate((2.6,3.1,3.6)):add(o,tone(880+i*220,.25,r=.1,v=.2),k)
    add(o,.3*noise(1.2)*np.linspace(0,1,int(1.2*SR))**2,3.2);hit(o,4.4);logo(o,8.0)
else:
    D=8;o=mk(D)
    add(o,.3*noise(.4,8)*np.hanning(int(.4*SR)),0.1)
    for k in (.6,.7):add(o,tone(1200,.08,r=.03,v=.2),k)
    add(o,.35*noise(.35,5)*np.hanning(int(.35*SR)),1.4);hit(o,1.6);add(o,tone(523,.3,v=.25)+tone(659,.3,v=.2),1.62)
    add(o,tone(392,.15,v=.2),2.6);add(o,tone(330,.15,v=.2),2.8);add(o,tone(262,.5,v=.2),3.0)  # sad trombone-ish
    logo(o,6.2)
fin(o,f"{s}.wav")
