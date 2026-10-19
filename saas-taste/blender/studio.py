"""Studio photo produit Cycles : cyclo, softboxes, HDRI faible, 85 mm, AgX, OIDN."""
import bpy, math, mathutils, os, sys, time
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets')

def reset(w=1440,h=900,samples=128):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene; sc.render.engine='CYCLES'; c=sc.cycles
    c.device='CPU'; c.samples=samples; c.use_adaptive_sampling=True; c.adaptive_threshold=0.02
    c.use_denoising=True; c.denoiser='OPENIMAGEDENOISE'; c.max_bounces=12; c.transmission_bounces=12; c.glossy_bounces=6
    c.caustics_reflective=False; c.caustics_refractive=False; c.blur_glossy=0.5
    sc.render.resolution_x=w; sc.render.resolution_y=h; sc.render.resolution_percentage=100
    sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
    sc.render.image_settings.file_format='PNG'; sc.render.film_transparent=False
    sc.render.threads_mode='FIXED'; sc.render.threads=4
    return sc

def world(hdr='royal_esplanade_1k.hdr', strength=0.35, rot=0.0):
    w=bpy.data.worlds.new('W'); bpy.context.scene.world=w; w.use_nodes=True; n=w.node_tree.nodes; L=w.node_tree.links
    n.clear(); out=n.new('ShaderNodeOutputWorld'); bg=n.new('ShaderNodeBackground'); env=n.new('ShaderNodeTexEnvironment')
    env.image=bpy.data.images.load(f'{A}/hdr/{hdr}'); mp=n.new('ShaderNodeMapping'); tc=n.new('ShaderNodeTexCoord')
    mp.inputs['Rotation'].default_value[2]=rot
    L.new(tc.outputs['Generated'],mp.inputs['Vector']); L.new(mp.outputs['Vector'],env.inputs['Vector'])
    L.new(env.outputs['Color'],bg.inputs['Color']); bg.inputs['Strength'].default_value=strength; L.new(bg.outputs['Background'],out.inputs['Surface'])
    # le fond HDRI n'est vu que par les reflets, pas par la caméra
    w.cycles_visibility.camera=False if hasattr(w,'cycles_visibility') else None

def mat(name,color,rough=0.85,spec=0.3):
    m=bpy.data.materials.new(name); m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value=(*color,1); p.inputs['Roughness'].default_value=rough
    p.inputs['Specular IOR Level'].default_value=spec; return m

def srgb(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c)

def cyclo(color='#E9E3DC', size=12, curve=1.6):
    """Fond de studio : sol + gorge courbe + mur, d'un seul tenant."""
    import bmesh
    me=bpy.data.meshes.new('cyc'); bm=bmesh.new(); prof=[]
    for i in range(0,21): prof.append((0,-size+i*size/20,0))
    for i in range(1,17): a=i/16*math.pi/2; prof.append((0,curve*math.sin(a),curve-curve*math.cos(a)))
    for i in range(1,11): prof.append((0,curve,curve+i*size/10))
    rows=[]
    for x in (-size,size):
        rows.append([bm.verts.new((x,p[1],p[2])) for p in prof])
    for j in range(len(prof)-1): bm.faces.new((rows[0][j],rows[1][j],rows[1][j+1],rows[0][j+1]))
    bm.to_mesh(me); bm.free(); ob=bpy.data.objects.new('cyc',me); bpy.context.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth=True
    ob.data.materials.append(mat('cyc',srgb(color),0.92,0.15)); return ob

def area(name,loc,target,size,energy,color=(1,1,1),shape='RECTANGLE',sy=None):
    d=bpy.data.lights.new(name,'AREA'); d.energy=energy; d.color=color; d.shape=shape; d.size=size
    if sy: d.size_y=sy
    o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc
    dirv=mathutils.Vector(target)-mathutils.Vector(loc); o.rotation_euler=dirv.to_track_quat('-Z','Y').to_euler(); return o

def lights(r, key=1.0, warm=True):
    """Softbox principale à gauche, fill large à droite, contre-jour haut derrière. r = rayon de l'objet."""
    kc=(1.0,0.96,0.9) if warm else (1,1,1)
    area('key',(-2.2*r*1.6,1.4*r*1.6,2.6*r*1.6),(0,0,r*0.5),3.2*r,900*key*r*r,kc,'RECTANGLE',2.2*r)
    area('fill',(3.0*r*1.6,1.8*r*1.6,1.2*r*1.6),(0,0,r*0.5),4.0*r,180*key*r*r,(0.92,0.95,1.0))
    area('rim',(0.8*r*1.6,-3.2*r*1.6,3.0*r*1.6),(0,0,r*0.6),2.0*r,520*key*r*r,(1,0.97,0.94),'RECTANGLE',0.6*r)

def load(glb):
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=f'{A}/khr/{glb}')
    obs=[o for o in bpy.data.objects if o not in before]; meshes=[o for o in obs if o.type=='MESH']
    bpy.context.view_layer.update()
    pts=[o.matrix_world@mathutils.Vector(c) for o in meshes for c in o.bound_box]
    mn=mathutils.Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)))
    mx=mathutils.Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
    roots=[o for o in obs if o.parent is None]
    piv=bpy.data.objects.new('piv',None); bpy.context.collection.objects.link(piv)
    for o in roots: o.parent=piv
    c=(mn+mx)/2; piv.location=(-c.x,-c.y,-mn.z)
    bpy.context.view_layer.update()
    size=mx-mn; return piv,size

def camera(size, az=35, el=12, focal=85, fill=0.78, look=0.45, dof=4.0, aspect=1.6):
    cam=bpy.data.cameras.new('cam'); cam.lens=focal; cam.sensor_width=36
    o=bpy.data.objects.new('cam',cam); bpy.context.collection.objects.link(o); bpy.context.scene.camera=o
    tgt=mathutils.Vector((0,0,size.z*look))
    # distance pour que l'objet occupe `fill` de la largeur ou hauteur
    fovx=2*math.atan(18/focal); fovy=2*math.atan(18/aspect/focal)
    rad=max(size.x,size.y)*0.5
    need=max((max(size.x,size.y))/(2*math.tan(fovx/2)*fill),(size.z)/(2*math.tan(fovy/2)*fill))+rad
    a=math.radians(az); e=math.radians(el)
    o.location=tgt+mathutils.Vector((math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)))*need
    o.rotation_euler=(tgt-o.location).to_track_quat('-Z','Y').to_euler()
    if dof: cam.dof.use_dof=True; cam.dof.focus_distance=(tgt-o.location).length; cam.dof.aperture_fstop=dof
    return o

def render(path):
    t=time.time(); bpy.context.scene.render.filepath=path; bpy.ops.render.render(write_still=True)
    print(f'RENDU {os.path.basename(path)} {time.time()-t:.1f}s', flush=True)

def sun(rot_deg=(52,0,-58), strength=4.0, color=(1.0,0.86,0.70), angle=1.2):
    d=bpy.data.lights.new('sun','SUN'); d.energy=strength; d.color=color; d.angle=math.radians(angle)
    o=bpy.data.objects.new('sun',d); bpy.context.collection.objects.link(o); o.rotation_euler=[math.radians(a) for a in rot_deg]
    bpy.context.view_layer.update(); return o

def gobo(center, normal_to, w=3.0, h=3.0, cols=3, rows=2, bar=0.07):
    """Cadre de fenêtre (croisillons) invisible pour la caméra : ne fait que porter des ombres."""
    import bmesh
    me=bpy.data.meshes.new('gobo'); bm=bmesh.new()
    def box(x0,y0,x1,y1):
        v=[bm.verts.new((x,y,0)) for x,y in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))]; bm.faces.new(v)
    big=max(w,h)*3
    box(-big,-big,big,-h/2); box(-big,h/2,big,big); box(-big,-h/2,-w/2,h/2); box(w/2,-h/2,big,h/2)
    for i in range(1,cols): x=-w/2+i*w/cols; box(x-bar/2,-h/2,x+bar/2,h/2)
    for j in range(1,rows): y=-h/2+j*h/rows; box(-w/2,y-bar/2,w/2,y+bar/2)
    bm.to_mesh(me); bm.free(); o=bpy.data.objects.new('gobo',me); bpy.context.collection.objects.link(o)
    o.location=center; dv=mathutils.Vector(normal_to)-mathutils.Vector(center); o.rotation_euler=dv.to_track_quat('Z','Y').to_euler()
    o.visible_camera=False; o.visible_glossy=False; o.visible_diffuse=False; o.visible_transmission=False
    m=mat('gobo',(0.02,0.02,0.02),1,0); o.data.materials.append(m); return o

def sun_dir(to_sun, strength=5.0, color=(1.0,0.87,0.72), angle=0.8):
    """Soleil défini par la direction vers le soleil (x droite caméra-ish, y profondeur, z haut)."""
    d=bpy.data.lights.new('sun','SUN'); d.energy=strength; d.color=color; d.angle=math.radians(angle)
    o=bpy.data.objects.new('sun',d); bpy.context.collection.objects.link(o)
    v=mathutils.Vector(to_sun).normalized(); o.rotation_euler=(-v).to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update(); return o, v

def flat_world(color=(0.9,0.88,0.85), strength=0.35):
    w=bpy.data.worlds.new('W'); bpy.context.scene.world=w; w.use_nodes=True
    bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*color,1); bg.inputs['Strength'].default_value=strength

def fast(samples=24):
    """Réglages d'animation : peu d'échantillons, rebonds courts, clamp, débruitage précis, bruit stable."""
    c=bpy.context.scene.cycles; c.samples=samples; c.adaptive_threshold=0.04
    c.max_bounces=6; c.diffuse_bounces=3; c.glossy_bounces=3; c.transmission_bounces=6; c.volume_bounces=0; c.transparent_max_bounces=8
    c.sample_clamp_indirect=4.0; c.denoising_prefilter='ACCURATE'; c.seed=7; c.use_animated_seed=False
    bpy.context.scene.render.use_persistent_data=True
