#!/usr/bin/env python3
"""Validate researched content; --require-100 is the release milestone gate."""
import argparse, json, re, sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'content/profiles.json').read_text())
pending=json.loads((ROOT/'content/pending.json').read_text()) if (ROOT/'content/pending.json').exists() else []
errors=[]; ids=set(); names=set(); source_count=0
allowed={'id','name','born','died','region','place','era','categories','featured','lesserKnown','summary','biography','achievements','milestones','sources','image','gallery','verification','reviewed'}
def fail(msg): errors.append(msg)
for item in p:
    label=item.get('id','<missing id>')
    if set(item)-allowed or allowed-set(item)-{'gallery'}: fail(f'{label}: schema keys differ from required set')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',label): fail(f'{label}: invalid ID')
    if label in ids: fail(f'{label}: duplicate ID')
    ids.add(label)
    name=item.get('name','').casefold().strip()
    if name in names: fail(f'{label}: duplicate name')
    names.add(name)
    if item.get('verification')!='verified': fail(f'{label}: unpublished record in publishable dataset')
    try: date.fromisoformat(item['reviewed'])
    except (ValueError,KeyError): fail(f'{label}: invalid review date')
    for field in ['born','died']:
        value=item.get(field)
        if value and not re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?',value): fail(f'{label}: invalid {field}')
    if not item.get('categories') or not item.get('region') or not item.get('era') or not item.get('summary'):fail(f'{label}: incomplete metadata')
    words=len(re.findall(r"\b[\w’'-]+\b",item.get('biography','')))
    if not 150<=words<=300:fail(f'{label}: biography {words} words (expected 150–300)')
    if not item.get('achievements') or not item.get('milestones'):fail(f'{label}: accomplishments or milestones missing')
    if len(item.get('sources',[]))<2:fail(f'{label}: fewer than two sources')
    domains=set()
    for source in item.get('sources',[]):
        u=source.get('url','');parsed=urlparse(u)
        if parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.password or 'example.' in parsed.netloc or re.search(r'[\s<>]',u):fail(f'{label}: suspicious URL {u}')
        if not source.get('title'):fail(f'{label}: source missing title')
        domains.add(parsed.netloc)
        source_count+=1
    if len(domains)<2: fail(f'{label}: two independent source domains required')
    gallery=item.get('gallery',[])
    if not isinstance(gallery,list): fail(f'{label}: gallery must be a list'); gallery=[]
    for photo in gallery:
        if not isinstance(photo,dict) or set(photo)!={'url','creator','source','license','attribution','caption','alt'}:
            fail(f'{label}: gallery image metadata incomplete')
            continue
        if any(not isinstance(v,str) or not v.strip() for v in photo.values()):fail(f'{label}: gallery image has blank fields')
        for field in ('url','source'):
            if urlparse(photo[field]).scheme!='https':fail(f'{label}: gallery {field} must be HTTPS')
    image=item.get('image')
    if image is not None:
        for field in ['url','creator','source','license','attribution']:
            if not image.get(field):fail(f'{label}: image missing {field}')
        if image.get('url') and urlparse(image['url']).scheme!='https':fail(f'{label}: image URL must be https')
for item in pending:
    if item.get('verification')!='pending' or not item.get('name') or not item.get('id'):fail('malformed pending candidate')
    if item.get('id') in ids or item.get('name','').casefold().strip() in names:fail(f"pending duplicate: {item.get('name')}")
    ids.add(item['id']);names.add(item['name'].casefold().strip())
parser=argparse.ArgumentParser();parser.add_argument('--require-100',action='store_true');args=parser.parse_args()
if args.require_100 and len(p)<100:fail(f'100-profile milestone unmet: {len(p)} verified; {100-len(p)} more required')
print(f'{len(p)} verified publishable profiles; {len(pending)} pending discovery candidates; {source_count} source citations; {len(errors)} validation errors')
for error in errors:print('ERROR:',error)
sys.exit(bool(errors))
