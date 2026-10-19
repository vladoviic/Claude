"""Rendus de production velvetly.  python prod.py draft|final job1,job2  [--out DIR]"""
import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from room import *
MODE=sys.argv[1]; JOBS=sys.argv[2].split(','); OUT=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','img')
os.makedirs(OUT,exist_ok=True)
RED=dict(hue=0.47,sat=1.3,val=0.6,sheen='#8F1D2E')        # mangue → velours rouge profond
BLUE=dict(hue=0.11,sat=1.1,val=0.62,sheen='#2A46A8')       # mangue → bleu « corporate »
def R(w,h,s):  # résolution/échantillons selon le mode
    if MODE=='draft': return reset(max(160,w//4),max(90,h//4),12)
    return reset(w,h,s)
def jpg(path):
    sc=bpy.context.scene; sc.render.image_settings.file_format='JPEG'; sc.render.image_settings.quality=93; render(path)
def hide(*names):
    for o in bpy.data.objects:
        if any(o.name.startswith(n) for n in names): o.visible_camera=False

def chair_in_room():
    for o in bpy.data.objects:
        if o.name.startswith('root_SheenChair'): return o
def room(chair=RED):
    build(chair_hex=None); hsv('fabric',**chair)

def j_room_eye():   R(2112,1188,96); room(); cam(); jpg(f'{OUT}/room_eye.jpg')
def j_room_top():   R(2112,1188,96); room(); hide('ceil','front'); cam((0.55,-1.9,5.3),(0.3,0.75,0.0),24,8.0); jpg(f'{OUT}/room_top.jpg')
def j_room_phone(): R(1000,1500,96); room(); cam((0.55,-1.55,0.95),(1.35,0.55,0.42),30,4.0); jpg(f'{OUT}/room_phone.jpg')
def j_chair_hero(): R(2112,1188,96); room(); cam((0.42,-1.32,0.30),(1.72,0.33,0.40),38,2.4); jpg(f'{OUT}/chair_hero.jpg')
def j_macro():
    R(2112,1188,96); room()
    ch=chair_in_room(); bpy.context.view_layer.update()
    # boulon du flanc gauche-avant (le plus exposé vers la caméra) : on vise un vrai sommet, pas le centre
    sd=mathutils.Vector((-0.95,-0.35,0.0)).normalized()
    vs=[o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' and any(m and m.name=='metal' for m in o.data.materials) for v in o.data.vertices]
    c=max([p for p in vs if p.z>0.2],key=lambda p:p.dot(sd)); print('METAL',c)
    area('mkey',tuple(c+sd*0.45+mathutils.Vector((-0.2,-0.25,0.35))),tuple(c),0.35,18,(1,0.97,0.93))
    cam(tuple(c+sd*0.34+mathutils.Vector((0.05,-0.06,0.07))),tuple(c+mathutils.Vector((0,0,0.02))),85,2.8); jpg(f'{OUT}/macro.jpg')

def studio_chair(variant, w, h, s, rot):
    R(w,h,s); flat_world((0.95,0.92,0.88),0.45); cyclo('#ECE5DC',12,1.2)
    piv,size=load('SheenChair.glb'); hsv('fabric',**variant)
    root=bpy.data.objects.new('turn',None); bpy.context.collection.objects.link(root); piv.parent=root; root.rotation_euler=(0,0,rot)
    s_,v=sun_dir((-0.7,-0.9,0.8),4.2); c=mathutils.Vector((0,0,0.45)); gobo(tuple(c+v*2.6),tuple(c),1.5,1.8,3,2,0.04)
    area('fill',(2.4,-2.6,1.2),(0,0,0.4),3.0,45,(1,0.98,0.96))
    camera(size,26,8,70,0.62,0.42,4.0); return root
def j_turn():
    """Plateau tournant pour la page produit : 72 images, bleu jusqu'à 47, rouge dès 38 (fondu 918-927)."""
    N=72; span=1.6
    for vname,var,rng_ in (('blue',BLUE,range(0,48)),('red',RED,range(38,72))):
        root=studio_chair(var,1100,800,56,0); sc=bpy.context.scene; sc.render.use_persistent_data=True
        if MODE=='draft': rng_=[rng_[0],rng_[-1]]
        for i in rng_:
            root.rotation_euler=(0,0,-0.55+span*i/(N-1)); os.makedirs(f'{OUT}/turn',exist_ok=True); jpg(f'{OUT}/turn/{vname}_{i:02d}.jpg')
    # masque du fauteuil seul (le thermique du changement de tissu ne touche que lui)
    sc=bpy.context.scene; sc.render.film_transparent=True; sc.cycles.samples=4; sc.cycles.use_denoising=False
    sc.render.resolution_percentage=50; sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'
    for o in bpy.data.objects:
        if o.name.startswith('cyc'): o.is_holdout=True
    for i in (range(36,50) if MODE!='draft' else [36]):
        root.rotation_euler=(0,0,-0.55+span*i/(N-1)); render(f'{OUT}/turn/mask_{i:02d}.png')
def tile(glb, name, fix=None, az=30, el=10, fill=0.6):
    R(600,800,96); flat_world((0.9,0.88,0.85),0.25); cyclo('#2B2826',12,1.0)
    piv,size=load(glb)
    if fix: fix()
    r=max(size)/2; area('key',(-1.6*r*2,-1.2*r*2,2.4*r*2),(0,0,size.z*0.4),2.4*r,700*r*r,(1,0.95,0.9))
    area('rim',(1.4*r*2,1.6*r*2,1.6*r*2),(0,0,size.z*0.5),1.6*r,600*r*r,(0.9,0.95,1.0),'RECTANGLE',0.5*r)
    area('fill',(2.0*r*2,-2.0*r*2,0.8*r*2),(0,0,size.z*0.4),3.0*r,90*r*r)
    camera(size,az,el,55,fill,0.45,5.6,0.75); jpg(f'{OUT}/tile_{name}.jpg')
def j_tiles():
    tile('SheenChair.glb','chair',lambda: hsv('fabric',**RED),32,10,0.62)
    tile('GlamVelvetSofa.glb','sofa',lambda: recolor('GlamVelvetSofa_fabric','#D9CCB6',0.07),24,9,0.8)
    tile('SpecularSilkPouf.glb','pouf',None,20,22,0.7)
    tile('IridescenceLamp.glb','lamp',None,20,6,0.55)
    tile('DiffuseTransmissionPlant.glb','plant',None,30,8,0.6)

# ---------------------------------------------------------------- séquences animées
from bpy_extras.object_utils import world_to_camera_view
import json
def seq_frames(n, step):
    """Images à rendre : une sur `step` (le reste est interpolé), toujours la dernière."""
    fs=list(range(0,n,step)); 
    if fs[-1]!=n-1: fs.append(n-1)
    return fs if MODE!='draft' else [0,n-1]
def place_cam(o,loc,look,lens=None):
    o.location=loc; o.rotation_euler=(mathutils.Vector(look)-mathutils.Vector(loc)).to_track_quat('-Z','Y').to_euler()
    if lens: o.data.lens=lens
def ease(t): return t*t*(3-2*t)
def j_aerial():
    """Plan « drone » (réf 380-417) : orbite descendante autour du fauteuil, parallaxe réelle.
    Exporte aussi la projection écran du tracé, du point et des contours du plan pour la surimpression."""
    N=39; R(1280,720,20); fast(20); room(); hide('ceil','front')
    sc=bpy.context.scene; o=cam((0,0,3),(0,0,0),24,8.0); c=mathutils.Vector((1.72,0.33,0.40))
    def pose(i):
        t=i/(N-1); az=math.radians(-150+34*t); el=math.radians(62-10*t); d=3.5-0.55*t
        loc=c+mathutils.Vector((math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el)))*d
        look=c+mathutils.Vector((-0.55+0.25*t,0.35-0.1*t,-0.3))
        place_cam(o,tuple(loc),tuple(look),24+3*t)
    os.makedirs(f'{OUT}/aerial',exist_ok=True)
    # surimpression : polylignes au sol (tracé, tapis, pouf, canapé, table, plante, fauteuil)
    def circle(cx,cy,r,n=40): return [(cx+r*math.cos(2*math.pi*k/n),cy+r*math.sin(2*math.pi*k/n),0.015) for k in range(n+1)]
    def rect(x0,y0,x1,y1): return [(x0,y0,.015),(x1,y0,.015),(x1,y1,.015),(x0,y1,.015),(x0,y0,.015)]
    route=[(0.0+0.0*k,0,0) for k in range(0)]
    P=[(-0.35,-1.15),(-0.05,-0.55),(0.55,-0.25),(1.05,0.0),(1.45,0.22),(1.70,0.32)]
    for k in range(len(P)-1):
        for s in range(10):
            u=s/10; route.append((P[k][0]*(1-u)+P[k+1][0]*u,P[k][1]*(1-u)+P[k+1][1]*u,0.02))
    route.append((1.72,0.33,0.40))
    def hull(prefix,pad=0.04):
        # emprise réelle du meuble au sol : enveloppe convexe de ses sommets
        from mathutils.geometry import convex_hull_2d
        root=next(o for o in bpy.data.objects if o.name.startswith(prefix)); bpy.context.view_layer.update()
        pts=[(o.matrix_world@v.co) for o in root.children_recursive if o.type=='MESH' for v in o.data.vertices]
        xy=[(p.x,p.y) for p in pts[::max(1,len(pts)//4000)]]; idx=convex_hull_2d(xy); poly=[xy[k] for k in idx]
        cx=sum(p[0] for p in poly)/len(poly); cy=sum(p[1] for p in poly)/len(poly)
        poly=[(cx+(x-cx)*(1+pad),cy+(y-cy)*(1+pad),0.015) for x,y in poly]; return poly+[poly[0]]
    shapes={'route':route,'rug':rect(-1.1,-0.4,1.6,1.5),'pouf':hull('root_SpecularSilkPouf'),'table':circle(-1.55,1.35,0.27),'plant':hull('root_DiffuseTransmissionPlant'),
            'sofa':hull('root_GlamVelvetSofa'),'chair':hull('root_SheenChair')}
    proj=[]
    for i in range(N):
        pose(i); bpy.context.view_layer.update()
        proj.append({k:[[round(v.x,4),round(1-v.y,4)] for v in (world_to_camera_view(sc,o,mathutils.Vector(p)) for p in pts)] for k,pts in shapes.items()})
    json.dump(proj,open(f'{OUT}/aerial/proj.json','w'))
    for i in seq_frames(N,2):
        pose(i); jpg(f'{OUT}/aerial/a_{i:02d}.jpg')

def chair_mask(o, path):
    """Silhouette du fauteuil seul (alpha) : le thermique du plan naît de lui."""
    sc=bpy.context.scene; keep=(sc.render.film_transparent,sc.cycles.samples,sc.cycles.use_denoising,sc.render.resolution_percentage,sc.render.image_settings.file_format,sc.render.image_settings.color_mode)
    ch=chair_in_room(); others=[ob for ob in bpy.data.objects if ob.type=='MESH' and ob not in ch.children_recursive]
    for ob in others: ob.is_holdout=True
    sc.render.film_transparent=True; sc.cycles.samples=8; sc.cycles.use_denoising=False; sc.render.resolution_percentage=50
    sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'; render(path)
    for ob in others: ob.is_holdout=False
    (sc.render.film_transparent,sc.cycles.samples,sc.cycles.use_denoising,sc.render.resolution_percentage,sc.render.image_settings.file_format,sc.render.image_settings.color_mode)=keep

def j_macro_seq():
    """Macro (réf 816-879) : contre-jour, orbite lente sur le pied et les boulons, puis vrai recul (48-58).
    64 images ; 1 sur 2 jusqu'à 47 (interpolées), toutes ensuite (mouvement rapide)."""
    N=64; R(1280,720,20); fast(20); room()
    ch=chair_in_room(); bpy.context.view_layer.update()
    sd=mathutils.Vector((-0.95,-0.35,0.0)).normalized()
    vs=[o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' and any(m and m.name=='metal' for m in o.data.materials) for v in o.data.vertices]
    c=max([p for p in vs if p.z>0.2],key=lambda p:p.dot(sd))
    # contre-jour : le mur derrière le pied s'allume, le pied passe en silhouette avec un liseré sur les boulons
    back=c-sd*1.2+mathutils.Vector((0,0,0.3))
    area('back',tuple(back+mathutils.Vector((0,0,0.6))),tuple(back-sd*0.5),1.6,260,(1,0.98,0.95))
    area('rim',tuple(c-sd*0.5+mathutils.Vector((0.25,0.3,0.35))),tuple(c),0.4,22,(1,1,1))
    o=cam((0,0,1),(0,0,0),85,2.8); mid=ch.matrix_world.translation+mathutils.Vector((0,0,0.38))
    def pose(i):
        if i<48:
            t=ease(i/47); az=math.radians(-12+22*t); R_=mathutils.Matrix.Rotation(az,3,'Z')
            off=R_@(sd*(0.36-0.04*t)+mathutils.Vector((0.05,-0.06,0.07)))
            place_cam(o,tuple(c+off),tuple(c+mathutils.Vector((0,0,0.02))),85)
            o.data.dof.focus_distance=off.length
        else:
            t=ease(min(1,(i-48)/10)); near=c+mathutils.Matrix.Rotation(math.radians(10),3,'Z')@(sd*0.32+mathutils.Vector((0.05,-0.06,0.07)))
            far=mid+mathutils.Vector((-1.25,-1.05,0.25)); loc=near.lerp(far,t); look=(c+mathutils.Vector((0,0,0.02))).lerp(mid,t)
            place_cam(o,tuple(loc),tuple(look),85-45*t); o.data.dof.focus_distance=(look-loc).length; o.data.dof.aperture_fstop=2.8+5*t
    os.makedirs(f'{OUT}/macro',exist_ok=True)
    fs=[i for i in range(0,48,2)]+list(range(48,64)) if MODE!='draft' else [0,40,52,63]
    for i in fs: pose(i); jpg(f'{OUT}/macro/m_{i:02d}.jpg')

def j_done_seq():
    """Order Complete (réf 952-1001) : caméra basse qui avance vers le fauteuil (parallaxe des murs).
    57 images, 1 sur 2 ; masque du fauteuil sur les 14 dernières pour le thermique."""
    N=57; R(1240,830,20); fast(20); room()
    o=cam((0.42,-1.32,0.30),(1.72,0.33,0.40),38,2.4)
    A=mathutils.Vector((0.36,-1.40,0.31)); B=mathutils.Vector((0.86,-0.78,0.36)); L0=mathutils.Vector((1.72,0.33,0.40)); L1=mathutils.Vector((1.73,0.36,0.42))
    def pose(i):
        t=i/(N-1); loc=A.lerp(B,t)+mathutils.Vector((0,0,0.006*math.sin(i*0.5))); look=L0.lerp(L1,t)
        place_cam(o,tuple(loc),tuple(look),38+4*t); o.data.dof.focus_distance=(look-loc).length
    os.makedirs(f'{OUT}/done',exist_ok=True)
    for i in seq_frames(N,2): pose(i); jpg(f'{OUT}/done/d_{i:02d}.jpg')
    for i in (range(43,57) if MODE!='draft' else [50]): pose(i); chair_mask(o,f'{OUT}/done/mask_{i:02d}.png')

def j_land_seq():
    """Landing (réf 234-299, réutilisée au montage) : travelling latéral lent dans le salon. 66 images, 1 sur 2."""
    N=66; R(1240,560,20); fast(20); room()
    o=cam((0.75,-3.7,1.12),(-0.05,1.0,0.72),30,5.6)
    def pose(i):
        t=i/(N-1); loc=(1.25-1.0*t,-3.75+0.2*t,1.10+0.04*t); look=(0.15-0.45*t,1.0,0.70)
        place_cam(o,loc,look,30); o.data.dof.focus_distance=(mathutils.Vector(look)-mathutils.Vector(loc)).length
    os.makedirs(f'{OUT}/land',exist_ok=True)
    for i in seq_frames(N,2): pose(i); jpg(f'{OUT}/land/l_{i:02d}.jpg')

for j in JOBS: globals()['j_'+j]()
