import math
def gear(cx,cy,ro,ri,n,hole,stroke,sw=5,fill="none",op=1):
    pts=[]
    for i in range(n*4):
        a=2*math.pi*i/(n*4)
        r= ro if i%4 in (1,2) else ri
        pts.append(f"{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}")
    return (f'<g opacity="{op}"><polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{hole}" fill="none" stroke="{stroke}" stroke-width="{sw}"/></g>')
def bearing(cx,cy,r,stroke,sw=5):
    balls=''.join(f'<circle cx="{cx+r*0.72*math.cos(2*math.pi*i/9):.1f}" cy="{cy+r*0.72*math.sin(2*math.pi*i/9):.1f}" r="{r*0.13:.1f}" fill="{stroke}" opacity=".9"/>' for i in range(9))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.45}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>{balls}')
def wrench(x,y,s,stroke,sw=5,rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" fill="none" stroke="{stroke}" stroke-width="{sw/s:.2f}" stroke-linejoin="round" stroke-linecap="round">'
            '<path d="M-14 -60 a30 30 0 1 0 28 0 l0 22 -14 8 -14 -8 z"/><path d="M-9 -12 L-9 70 a9 9 0 0 0 18 0 L9 -12"/></g>')
# small icons
def ic_sound(c): return f'<svg width="64" height="64" viewBox="0 0 64 64" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 24h10l14-12v40L18 40H8z"/><path d="M42 22c4 5 4 15 0 20M50 14c8 9 8 27 0 36"/></svg>'
def ic_vib(c): return f'<svg width="64" height="64" viewBox="0 0 64 64" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 32h8l6-14 8 28 8-28 8 28 6-14h12"/></svg>'
def ic_temp(c): return f'<svg width="64" height="64" viewBox="0 0 64 64" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M26 10a6 6 0 0 1 12 0v28a12 12 0 1 1-12 0z"/><path d="M32 22v20"/><circle cx="32" cy="48" r="4" fill="{c}"/></svg>'
