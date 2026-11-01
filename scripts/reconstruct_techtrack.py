#!/usr/bin/env python3
"""Reconstruct review-only outlined TechTrack vector assets from immutable SVG PNG references.

Not original designer paths. Uses color-family segmentation and smoothed contours; preserves
original raster source and marks all outputs pending visual approval.
"""
import argparse, base64, hashlib, io, json, re, shutil, sys, xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import cairosvg

BACKGROUNDS={'white':'#FFFFFF','black':'#000000','lemon':'#FFC93D'}
INPUTS={
 'techtrack':{
  'mark':'techtrack-mark-bg-white-v1.svg',
  'stacked':'techtrack-lockup-stacked-bg-white-v1.svg',
  'horizontal':'techtrack-lockup-horizontal-bg-black-v1.svg',
  'wordmark':'techtrack-wordmark-bg-lemon-v1.svg',
 },
 'techtrack-kids':{
  'mark':'techtrack-kids-mark-bg-white-v1.svg',
  'stacked':'techtrack-kids-lockup-stacked-bg-white-v1.svg',
  'horizontal':'techtrack-kids-lockup-horizontal-bg-black-v1.svg',
  'wordmark':'techtrack-kids-wordmark-bg-lemon-v1.svg',
 },
}

def slug_title(b):return 'TechTrack Kids' if b.endswith('kids') else 'TechTrack'
def svg_path(mask, eps=0.7):
    # A small Gaussian filter suppresses PNG edge noise before contour extraction.
    arr=(cv2.GaussianBlur(mask.astype(np.uint8)*255,(3,3),.65)>125).astype('uint8')*255
    contours,hier=cv2.findContours(arr,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    parts=[]
    for c in contours:
        if abs(cv2.contourArea(c))<3.0:continue
        c=cv2.approxPolyDP(c,eps,True)
        if len(c)<3:continue
        pts=c.reshape(-1,2)
        parts.append('M'+' L'.join(f'{x},{y}' for x,y in pts)+' Z')
    return ' '.join(parts)

def categorize(im,bg):
    rgb=np.asarray(im.convert('RGB')).astype(np.int16)
    # Exact background is opaque and uniform in provided files.
    delta=np.max(np.abs(rgb-np.array(bg,dtype=np.int16)),axis=2)
    fg=delta>24
    r,g,b=np.moveaxis(rgb,-1,0)
    masks={}
    masks['light']=fg&(r>160)&(g>160)&(b>160)
    masks['orange']=fg&(r>150)&(r>g*1.17)&(g>43)&(b<160)
    masks['yellow']=fg&(r>130)&(g>95)&(r>b*1.6)&(g>b*1.25)&~masks['orange']
    masks['mint']=fg&(g>112)&(g>r*1.45)&(g>=b*.83)&~masks['light']&~masks['orange']&~masks['yellow']
    masks['teal']=fg&(b>55)&(g>65)&(b<200)&(g<180)&(r<95)&~masks['mint']&~masks['light']
    masks['blue']=fg&(b>118)&(b>r*1.6)&(b>g*1.17)&~masks['teal']&~masks['light']
    used=np.zeros(fg.shape,dtype=bool)
    for k in ('light','orange','yellow','mint','teal','blue'):used |= masks[k]
    masks['ink']=fg&~used
    # De-speckle tiny components; holes stay in paths via even-odd fill.
    for k,m in masks.items():
        count, ids, stats, centers=cv2.connectedComponentsWithStats(m.astype('uint8'),8)
        keep=np.zeros(m.shape,np.uint8)
        for i in range(1,count):
            if stats[i,cv2.CC_STAT_AREA]>=5:keep[ids==i]=1
        masks[k]=keep.astype(bool)
    return masks,rgb,fg

def component_paths(mask, rgb, category, id_prefix):
    count,labels,stats,centers=cv2.connectedComponentsWithStats(mask.astype('uint8'),8)
    pieces=[]; defs=[]
    for i in range(1,count):
        x,y,w,h,area=stats[i]
        if area<10:continue
        m=np.uint8(labels==i)
        d=svg_path(m)
        if not d:continue
        if category in ('light','ink'):
            pieces.append({'category':category,'d':d,'color':None})
            continue
        if category=='yellow':
            pieces.append({'category':category,'d':d,'color':'#FCCA38'})
            continue
        if category=='orange':
            pieces.append({'category':category,'d':d,'color':'#FB693A'})
            continue
        # Real SVG gradients, fitted against local original color samples. Use
        # separate gradients for each connected region so the cap and stems differ.
        axis=0 if w>h*1.15 else 1
        pixel=rgb[labels==i]
        loc=np.argwhere(labels==i)
        idx=loc[:,1] if axis==0 else loc[:,0]
        q=np.quantile(idx,[.10,.32,.55,.78,.90]); colors=[]
        for z in q:
            selection=(abs(idx-z)<max(2,(w if axis==0 else h)*.09))
            sample=pixel[selection]
            if len(sample)<4:sample=pixel
            col=np.median(sample,axis=0).astype(int)
            colors.append('#%02X%02X%02X'%tuple(np.clip(col,0,255)))
        # Keep gradients soft and anchored in the exact source palette.
        gid=f'{id_prefix}_{category}_{i}'
        if axis==0:
            gr=f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
        else:gr=f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        # objectBoundingBox gradient coordinates use percentage; 0/1 valid.
        gr+=''.join(f'<stop offset="{j*25}%" stop-color="{c}"/>' for j,c in enumerate(colors[:5]))+'</linearGradient>'
        defs.append(gr)
        pieces.append({'category':category,'d':d,'color':f'url(#{gid})'})
    return pieces,defs

def decode_reference(source):
    data=source.read_bytes();root=ET.fromstring(data)
    image=root.find('{http://www.w3.org/2000/svg}image')
    if image is None:raise ValueError('No embedded image in original')
    href=image.attrib.get('href') or image.attrib.get('{http://www.w3.org/1999/xlink}href')
    assert href.startswith('data:image/png;base64,')
    raw=base64.b64decode(href.split(',',1)[1]); im=Image.open(io.BytesIO(raw));im.load()
    return im,{'original_file':source.name,'original_sha256':hashlib.sha256(data).hexdigest(),
              'svg_viewBox':root.attrib.get('viewBox'),'svg_dimensions':[root.attrib.get('width'),root.attrib.get('height')],
              'embedded_png_dimensions':list(im.size),'embedded_png_sha256':hashlib.sha256(raw).hexdigest(),
              'embedded_png_mode':im.mode,'background_rgb':list(im.convert('RGB').getpixel((0,0)))}

def extract_geometry(im,id_prefix,brand=None,comp=None):
    rgb=np.asarray(im.convert('RGB')).astype(np.int16)
    bg=rgb[0,0]
    fg=(np.max(np.abs(rgb-bg),axis=2)>28).astype('uint8')
    count,labels,stats,centers=cv2.connectedComponentsWithStats(fg,8)
    mask_info=[]
    for i in range(1,count):
        x,y,w,h,area=map(int,stats[i])
        if area<5:continue
        med=np.median(rgb[labels==i],axis=0)
        mask_info.append((area,i,x,y,w,h,med))
    # Three physically separate primary components of the original T symbol.
    # These are unambiguously distinguishable by their shape and area.
    mark_ids=set()
    if comp != 'wordmark':
        candidates=[x for x in mask_info if x[0]>4000 and
                    (comp=='mark' or (comp=='stacked' and x[3]<im.height*.48) or
                     (comp=='horizontal' and x[2]<im.width*.30))]
        mark_ids={x[1] for x in sorted(candidates,reverse=True)[:3]}
    pieces=[];defs=[]
    for area,i,x,y,w,h,med in mask_info:
        if area<5:continue
        d=svg_path((labels==i).astype('uint8'),eps=.77 if area>300 else .35)
        if not d:continue
        r,g,b=med
        if i in mark_ids:
            if (w/h)>2.6:part='top'
            elif (y<im.height*.35 and (r>g or g>r*1.6)) or (x>im.width*.37 and g>r*1.5):part='right'
            else:part='left'
            # stronger classification by upper/right placement; left hooked stem
            # starts lower than top bar and x is to the left.
            if part!='top':
                candidate_right=sorted([z for z in mask_info if z[1] in mark_ids],key=lambda z:z[2],reverse=True)[0]
                if candidate_right[1]==i:part='right'
                else:part='left'
            if part=='top':
                gid=f'{id_prefix}_cap_{i}'
                defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#02BCFA"/><stop offset="38%" stop-color="#078FFC"/><stop offset="72%" stop-color="#0768F9"/><stop offset="100%" stop-color="#064DBD"/></linearGradient>')
                pieces.append({'category':'symbol','d':d,'color':f'url(#{gid})'})
            elif part=='left':
                gid=f'{id_prefix}_stem_{i}'
                defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#06A8FC"/><stop offset="30%" stop-color="#0364F9"/><stop offset="75%" stop-color="#0767FA"/><stop offset="100%" stop-color="#064CBD"/></linearGradient>')
                pieces.append({'category':'symbol','d':d,'color':f'url(#{gid})'})
            else:
                clip=f'{id_prefix}_right_{i}'
                defs.append(f'<clipPath id="{clip}"><path d="{d}" fill-rule="evenodd"/></clipPath>')
                split=y+h*.43
                # Multi-part component keeps the wing's warm/teal shade distinct
                # from the deeper vertical tail without introducing new geometry.
                if brand.endswith('kids'):
                    wing=('url(#'+id_prefix+'_kids_gold)')
                    defs.append(f'<linearGradient id="{id_prefix}_kids_gold" x1="0" y1="0" x2="1" y2=".3"><stop stop-color="#FBC83B"/><stop offset="80%" stop-color="#FFD668"/><stop offset="100%" stop-color="#F4B82A"/></linearGradient>')
                    # Yellow wing may need orange treatment on lemon (handled below)
                    wing_lemon='#FE8543'
                    tail='#02C6A7'
                else:
                    wing='#02C9AC';wing_lemon=wing;tail='#027A9C'
                # objectBoundingBox gradient in wing has smoother pastel details.
                pieces.append({'category':'right_wing','d':d,'color':wing,'lemon_color':wing_lemon,'clip':clip,'rect':(x,y,w,split-y+2)})
                pieces.append({'category':'right_tail','d':d,'color':tail,'clip':clip,'rect':(x,split,w,y+h-split+2)})
        else:
            if r>150 and r>g*1.25 and g<180:cat='orange';col='#FB693A'
            elif r>150 and g>120 and r>b*1.5:cat='yellow';col='#FCCA38'
            elif g>105 and g>r*1.5 and g>b*.78:cat='mint';col='#02C9AC'
            elif b>150 and b>g*1.3 and b>r*1.3:cat='blue';col='#0464FA'
            else:cat='ink';col=None
            pieces.append({'category':cat,'d':d,'color':col})
    return pieces,defs,{'components':len(mask_info),'mark_components':len(mark_ids)}

def create_svg(brand,comp,im,pieces,defs,bg=None):
    w,h=im.size
    name=slug_title(brand)
    label=f'{name} {comp} / '+(bg or 'transparent')
    bkg= f'<rect width="{w}" height="{h}" fill="{BACKGROUNDS[bg]}"/>' if bg else ''
    shapes=[]
    for p in pieces:
        cat=p['category'];col=p['color']
        if cat in ('light','ink'):
            col= '#F8FAFE' if bg=='black' else '#041B45'
        # source brand palette, Kids orange accents needed on lemon for visibility
        elif brand=='techtrack-kids' and bg=='lemon' and cat=='yellow':col='#FE8543'
        elif brand=='techtrack-kids' and bg=='lemon' and cat=='right_wing':col=p['lemon_color']
        if 'clip' in p:
            x,y,w2,h2=p['rect']
            shapes.append(f'<rect x="{x}" y="{y}" width="{w2}" height="{h2}" fill="{col}" clip-path="url(#{p["clip"]})"/>')
        else:shapes.append(f'<path fill="{col}" fill-rule="evenodd" d="{p["d"]}"/>')
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'role="img" aria-label="{label}" data-provenance="vector-reconstructed-from-raster" data-approval="pending">'
         f'<title>{label} — unapproved vector reconstruction</title><desc>Outlined color-layer reconstruction '
         f'of original uploaded image; not the original designer vector master.</desc><defs>{"".join(defs)}</defs>'
         f'{bkg}{"".join(shapes)}</svg>')
    return svg

def export_svg(svg,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(svg,encoding='utf8')
    root=ET.fromstring(svg)
    assert not list(root.iter('{http://www.w3.org/2000/svg}image'))
    assert 'data:image/' not in svg and 'base64,' not in svg
    assert root.attrib['viewBox']

def image_png(svg,out_path,width,transparent,background=None):
    vb=ET.fromstring(svg).get('viewBox').split()
    w,h=map(float,vb[-2:]);height=round(width*h/w)
    data=cairosvg.svg2png(bytestring=svg.encode(),output_width=width,output_height=height)
    image=Image.open(io.BytesIO(data)).convert('RGBA')
    if transparent:
        a=np.asarray(image.getchannel('A')); assert a.min()==0 and a.max()==255
    else:
        assert background is not None
        import PIL.ImageColor
        matte=Image.new('RGBA',image.size,PIL.ImageColor.getrgb(background)+(255,))
        matte.alpha_composite(image)
        image=matte
        a=np.asarray(image.getchannel('A'));assert a.min()==255
    out_path.parent.mkdir(parents=True,exist_ok=True)
    image.save(out_path,optimize=True)
    return [width,height]

def build(root, do_png=True):
    results={}; samples=[]
    for brand,inp in INPUTS.items():
        target=root/'brands'/brand;source=(target/'source')
        info={};inv={}
        for comp,filename in inp.items():
            im,metadata=decode_reference(source/filename)
            pieces,defs,counts=extract_geometry(im,f'{brand.replace("-","_")}_{comp}',brand,comp)
            metadata.update({'component_pixel_counts':counts,'vector_path_count':len(pieces),
                             'geometry_method':'color-family segmentation / smoothed original silhouette contours; gradient stops fitted to raster samples'})
            info[comp]=metadata
            master=create_svg(brand,comp,im,pieces,defs,None)
            export_svg(master,target/'vector'/comp/f'{brand}-{comp}-master.svg')
            inv[comp]={}
            for bg in BACKGROUNDS:
                art=create_svg(brand,comp,im,pieces,defs,bg)
                name=f'{brand}-{comp}-{bg}-v1.svg'
                export_svg(art,target/'logos'/'svg'/name)
                inv[comp][bg]={'svg':f'logos/svg/{name}','dimensions':list(im.size),'png':[]}
                if do_png:
                    sizes=[512,1024,2048,4096] if comp=='mark' else [1024,2048,4096]
                    for width in sizes:
                        out=target/'logos'/'png'/f'{brand}-{comp}-{bg}-{width}w-v1.png'
                        dims=list(Image.open(out).size) if out.exists() else image_png(art,out,width,False,BACKGROUNDS[bg])
                        inv[comp][bg]['png'].append({'path':str(out.relative_to(target)),'dimensions':dims,'alpha':False})
            if do_png:
                sizes=[512,1024,2048,4096] if comp=='mark' else [1024,2048,4096]
                for width in sizes:
                    out=target/'logos'/'png'/f'{brand}-{comp}-transparent-{width}w-v1.png'
                    image_png(master,out,width,True) if not out.exists() else None
        manifest={'name':slug_title(brand),'slug':brand,'status':'draft','approval':'pending',
                  'provenance':'vector-reconstructed-from-raster','original_sources_preserved':True,
                  'palette':{'white':'#FFFFFF','black':'#000000','lemon':'#FFC93D','navy':'#041B45',
                             'blue':'#0464FA','cyan':'#03A6FC','teal':'#02C9AC','kids_orange':'#FB693A','kids_yellow':'#FCCA38'},
                  'tagline':'Learn. Play. Create.' if brand.endswith('kids') else 'Skills Today. Opportunities Tomorrow.',
                  'sources':info,'assets':inv,'limitations':['Reference raster has quantization/antialiasing; exact original curves cannot be recovered.',
                    'Gradient regions inferred from colour samples; source illustration requires designer sign-off.',
                    'Letterforms are traced outlines, not a substitute font or original designer typography.']}
        # Audit every original uploaded source, including variants not selected for tracing.
        all_src={}
        for sp in sorted(source.glob('*.svg')):
            try:
                _, rec=decode_reference(sp)
                all_src[sp.name]=rec
            except ValueError:continue
        manifest['source_inventory']=all_src
        (target/'brand.json').write_text(json.dumps(manifest,indent=2)+'\n')
        results[brand]=all_src
        (target/'brand.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (root/'reconstruction-audit.json').write_text(json.dumps(results,indent=2)+'\n')
    return results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path('.'));ap.add_argument('--no-png',action='store_true');ns=ap.parse_args()
    print(json.dumps({b:{k:v['svg_viewBox'] for k,v in d.items()} for b,d in build(ns.root,not ns.no_png).items()},indent=2))
