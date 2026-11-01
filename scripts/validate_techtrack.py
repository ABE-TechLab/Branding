#!/usr/bin/env python3
"""Quality gates for draft TechTrack SVG/PNG reconstruction; not brand approval."""
from pathlib import Path
from PIL import Image
import hashlib, json, re, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
checks=0
for brand in ['techtrack','techtrack-kids']:
    b=ROOT/'brands'/brand; m=json.loads((b/'brand.json').read_text())
    assert m['approval']=='pending' and m['provenance']=='vector-reconstructed-from-raster'
    for filename,rec in m['source_inventory'].items():
        source=b/'source'/filename
        assert source.exists() and hashlib.sha256(source.read_bytes()).hexdigest()==rec['original_sha256'],source
        checks+=1
    for comp in ['mark','stacked','horizontal','wordmark']:
        base=b/'vector'/comp/f'{brand}-{comp}-master.svg'
        assert base.exists()
        for path in [base]+[b/'logos'/'svg'/f'{brand}-{comp}-{bg}-v1.svg' for bg in ['white','black','lemon']]:
            s=path.read_text()
            r=ET.fromstring(s)
            assert r.attrib.get('data-provenance')=='vector-reconstructed-from-raster'
            assert r.attrib.get('data-approval')=='pending'
            assert len(list(r.iter('{http://www.w3.org/2000/svg}path')))>0
            assert '<image' not in s and 'base64' not in s and 'data:image/' not in s
            assert not re.search(r'<(?:script|foreignObject|iframe)\b|onload=',s,re.I)
            assert r.attrib['viewBox'].split()[-2:]==[str(x) for x in m['sources'][comp]['embedded_png_dimensions']]
            checks+=1
        for bg in ['white','black','lemon','transparent']:
            widths=([512,1024,2048,4096] if comp=='mark' else [1024,2048,4096])
            for w in widths:
                p=b/'logos'/'png'/f'{brand}-{comp}-{bg}-{w}w-v1.png'
                assert p.exists(),p
                im=Image.open(p)
                assert im.format=='PNG' and im.width==w,p
                ow,oh=m['sources'][comp]['embedded_png_dimensions']
                assert abs(im.height-(w*oh/ow))<=.51,p
                a=im.convert('RGBA').getchannel('A')
                assert a.getextrema()==((0,255) if bg=='transparent' else (255,255)),(p,a.getextrema())
                checks+=1
print(f'PASS: {checks} source, vector XML, export dimensions, opacity and provenance checks')
print('NOTE: visual similarity and original-designer approval remain pending.')
