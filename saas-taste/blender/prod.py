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
for j in JOBS: globals()['j_'+j]()
