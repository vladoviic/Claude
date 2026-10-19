"""Intérieur photoréaliste : pièce enduite, fenêtre atelier, soleil, mobilier Khronos/Wayfair."""
import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from studio import *

def pmat(name,hexcol,rough=0.8,noise=0.05,bump=0.08,scale=6.0,spec=0.3):
    """Matériau mat avec variation de teinte et léger relief (enduit, béton, travertin)."""
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; N=nt.nodes; L=nt.links; p=N['Principled BSDF']
    tx=N.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value=scale; tx.inputs['Detail'].default_value=8; tx.inputs['Roughness'].default_value=0.6
    c=srgb(hexcol); mr=N.new('ShaderNodeMix'); mr.data_type='RGBA'; mr.inputs['A'].default_value=(*[x*(1-noise) for x in c],1); mr.inputs['B'].default_value=(*[min(1,x*(1+noise)) for x in c],1)
    L.new(tx.outputs['Fac'],mr.inputs['Factor']); L.new(mr.outputs['Result'],p.inputs['Base Color'])
    b=N.new('ShaderNodeBump'); b.inputs['Strength'].default_value=bump; L.new(tx.outputs['Fac'],b.inputs['Height']); L.new(b.outputs['Normal'],p.inputs['Normal'])
    p.inputs['Roughness'].default_value=rough; p.inputs['Specular IOR Level'].default_value=spec; return m

def box(name,loc,dim,m,bevel=0):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=(dim[0]/2,dim[1]/2,dim[2]/2)
    bpy.ops.object.transform_apply(scale=True)
    if bevel: md=o.modifiers.new('b','BEVEL'); md.width=bevel; md.segments=4
    o.data.materials.append(m); return o

def place(glb,loc,rotz=0,scale=1):
    piv,size=load(glb); piv.location=(piv.location.x+loc[0],piv.location.y+loc[1],piv.location.z+loc[2])
    # rotation autour du centre posé : pivot intermédiaire
    root=bpy.data.objects.new('root_'+glb,None); bpy.context.collection.objects.link(root); root.location=loc
    piv.location=(piv.location.x-loc[0],piv.location.y-loc[1],piv.location.z-loc[2]); piv.parent=root
    root.rotation_euler=(0,0,math.radians(rotz)); root.scale=(scale,)*3; bpy.context.view_layer.update(); return root,size

def recolor(prefix,hexcol,keep_tex=0.25):
    """Remplace la couleur de base des matériaux dont le nom commence par prefix (garde un peu de la texture)."""
    for m in bpy.data.materials:
        if not m.name.startswith(prefix) or not m.use_nodes: continue
        nt=m.node_tree; p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'); inp=p.inputs['Base Color']
        src=inp.links[0].from_socket if inp.links else None
        mix=nt.nodes.new('ShaderNodeMix'); mix.data_type='RGBA'; mix.blend_type='MULTIPLY' if src else 'MIX'
        col=srgb(hexcol)
        if src:
            hs=nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(src,hs.inputs['Color'])
            # luminance de la texture (pour garder le froissé du velours) × nouvelle teinte
            mp=nt.nodes.new('ShaderNodeMapRange'); nt.links.new(hs.outputs['Val'],mp.inputs['Value'])
            mp.inputs['From Min'].default_value=0.0; mp.inputs['From Max'].default_value=0.25; mp.inputs['To Min'].default_value=1-keep_tex; mp.inputs['To Max'].default_value=1+keep_tex
            mix.inputs['Factor'].default_value=1.0; nt.links.new(mp.outputs['Result'],mix.inputs['A']); mix.inputs['B'].default_value=(*col,1)
        else: mix.inputs['Factor'].default_value=1.0; mix.inputs['A'].default_value=(1,1,1,1); mix.inputs['B'].default_value=(*col,1)
        nt.links.new(mix.outputs['Result'],inp)
        if 'Sheen Tint' in p.inputs and p.inputs['Sheen Weight'].default_value>0: p.inputs['Sheen Tint'].default_value=(*[min(1,c*1.4+0.15) for c in col],1)

def art(loc,w,h):
    """Tableau abstrait aux couleurs irisées du film, cadre chêne fin."""
    m=bpy.data.materials.new('art'); m.use_nodes=True; nt=m.node_tree; N=nt.nodes; L=nt.links; p=N['Principled BSDF']
    wv=N.new('ShaderNodeTexWave'); wv.wave_type='BANDS'; wv.inputs['Scale'].default_value=1.1; wv.inputs['Distortion'].default_value=7; wv.inputs['Detail'].default_value=3
    cr=N.new('ShaderNodeValToRGB'); e=cr.color_ramp; e.elements[0].color=(*srgb('#F6C9D3'),1); e.elements[1].color=(*srgb('#BFE6F2'),1)
    for pos,hx in [(0.33,'#FFD9B8'),(0.62,'#D8CCF4'),(0.85,'#FF8FA3')]: el=e.elements.new(pos); el.color=(*srgb(hx),1)
    L.new(wv.outputs['Fac'],cr.inputs['Fac']); L.new(cr.outputs['Color'],p.inputs['Base Color']); p.inputs['Roughness'].default_value=0.9
    pl=box('art',loc,(w,0.02,h),m); fr=pmat('oak','#8A6A4A',0.6,0.08,0.02,40)
    t=0.025
    for dx,dz,ww,hh in [(0,h/2,w+2*t,t),(0,-h/2,w+2*t,t),(-w/2,0,t,h),(w/2,0,t,h)]: box('fr',(loc[0]+dx,loc[1]-0.005,loc[2]+dz),(ww,0.035,hh),fr)

def build(chair_hex='#D7263D', sofa_hex='#D9CCB6', sun_to=(-1.0,-0.30,0.62), sun_strength=7.0):
    flat_world((0.86,0.91,1.0),2.2); bpy.context.scene.view_settings.exposure=0.3
    wall=pmat('wall','#E7DED2',0.92,0.035,0.06,3.5); floor=pmat('floor','#C4B9AC',0.55,0.06,0.03,1.8,0.45)
    box('floor',(0.45,-1.7,-0.05),(6.5,7.8,0.1),floor); box('ceil',(0.45,-1.7,2.85),(6.5,7.8,0.1),wall)
    box('ground',(-8,0,-0.6),(10,20,0.1),pmat('ground','#B9B2A6',0.9,0.05,0.02,2))
    box('back',(0.45,2.08,1.4),(6.5,0.16,2.9),wall); box('front',(0.45,-5.5,1.4),(6.5,0.16,2.9),wall); box('right',(3.6,0,1.4),(0.16,12,2.9),wall)
    # mur gauche percé d'une grande fenêtre (y -0.6..1.6, z 0.45..2.45)
    X=-2.7; y0,y1,z0,z1=-0.7,1.7,0.42,2.48
    box('lw1',(X,(y1+2.1)/2+0.02,1.4),(0.16,2.1-y1+0.04,2.9),wall); box('lw2',(X,(y0-6)/2,1.4),(0.16,6+y0,2.9),wall)
    box('lw3',(X,(y0+y1)/2,z0/2),(0.16,y1-y0,z0),wall); box('lw4',(X,(y0+y1)/2,(z1+2.9)/2),(0.16,y1-y0,2.9-z1),wall)
    steel=mat('steel',srgb('#1C1B1A'),0.45,0.5)
    for k in range(0,5): yy=y0+k*(y1-y0)/4; box('mv',(X,yy,(z0+z1)/2),(0.06,0.035,z1-z0),steel)
    for k in range(0,4): zz=z0+k*(z1-z0)/3; box('mh',(X,(y0+y1)/2,zz),(0.06,y1-y0,0.035),steel)
    s,v=sun_dir(sun_to,sun_strength,(1.0,0.86,0.70),0.6)
    # portail de ciel sur la fenêtre pour guider l'échantillonnage
    lp=area('portal',(X+0.05,(y0+y1)/2,(z0+z1)/2),(X+1,(y0+y1)/2,(z0+z1)/2),1,0); lp.data.cycles.is_portal=True; lp.data.shape='RECTANGLE'; lp.data.size=y1-y0; lp.data.size_y=z1-z0
    # tapis laine
    rug=pmat('rug','#D3C6B3',1.0,0.08,0.25,60,0.1); box('rug',(0.25,0.55,0.006),(2.7,1.9,0.012),rug,0.006)
    # table d'appoint travertin
    trav=pmat('trav','#D8C8B0',0.6,0.12,0.12,9,0.4)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.24,depth=0.52,location=(-1.55,1.35,0.26),vertices=96); t=bpy.context.object; t.data.materials.append(trav)
    bpy.ops.object.shade_smooth(); md=t.modifiers.new('b','BEVEL'); md.width=0.01; md.segments=3
    place('GlamVelvetSofa.glb',(0.05,1.42,0),0); recolor('GlamVelvetSofa_fabric',sofa_hex,0.07)
    place('SheenChair.glb',(1.75,0.35,0),-38)
    if chair_hex: recolor('fabric',chair_hex,0.2)
    place('SpecularSilkPouf.glb',(0.15,0.35,0.012),15)
    place('GlassVaseFlowers.glb',(0.05,0.36,0.212),20)
    place('DiffuseTransmissionTeacup.glb',(0.33,0.22,0.212),0)
    place('DiffuseTransmissionPlant.glb',(-2.1,1.55,0),30,1.35)
    place('IridescenceLamp.glb',(-1.55,1.35,0.52),0)
    art((0.05,1.995,1.62),1.05,0.72)

def cam(loc=(0.75,-3.7,1.12), look=(-0.05,1.0,0.72), lens=30, fstop=5.6, focus=None):
    c=bpy.data.cameras.new('cam'); c.lens=lens; c.sensor_width=36; o=bpy.data.objects.new('cam',c); bpy.context.collection.objects.link(o)
    bpy.context.scene.camera=o; o.location=loc; o.rotation_euler=(mathutils.Vector(look)-mathutils.Vector(loc)).to_track_quat('-Z','Y').to_euler()
    c.dof.use_dof=True; c.dof.focus_distance=focus or (mathutils.Vector(look)-mathutils.Vector(loc)).length; c.dof.aperture_fstop=fstop; return o

def hsv(prefix, hue=0.5, sat=1.0, val=1.0, sheen=None):
    """Décale la teinte de la texture d'origine (garde le froissé du velours)."""
    for m in bpy.data.materials:
        if not m.name.startswith(prefix) or not m.use_nodes: continue
        nt=m.node_tree; p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'); inp=p.inputs['Base Color']
        if not inp.links: continue
        src=inp.links[0].from_socket; h=nt.nodes.new('ShaderNodeHueSaturation')
        h.inputs['Hue'].default_value=hue; h.inputs['Saturation'].default_value=sat; h.inputs['Value'].default_value=val
        nt.links.new(src,h.inputs['Color']); nt.links.new(h.outputs['Color'],inp)
        if sheen and p.inputs['Sheen Weight'].default_value>0:
            sl=p.inputs['Sheen Tint']
            for l in list(sl.links): nt.links.remove(l)
            sl.default_value=(*srgb(sheen),1)
