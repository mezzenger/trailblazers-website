#!/usr/bin/env python3
"""Recreate an audit inventory from the preserved Cocoa-decoded source."""
import json,re
from html import unescape
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'legacy/recovered-original.html').read_text()
items=[]
for category,section in re.findall(r'<section id="([^"]+)">(.*?)</section>',source,re.S):
    for block in re.findall(r'<div class="profile">(.*?)</div>',section,re.S):
        h=re.search(r'<h3>(.*?)</h3>',block,re.S);img=re.search(r'<img src="([^"]+)"',block);a=re.search(r'<a href="([^"]+)"',block)
        ps=re.findall(r'<p(?: class="[^"]+")?>(.*?)</p>',block,re.S)
        if not h:continue
        items.append({'name':unescape(h.group(1)),'legacyCategory':category,'legacyBiographyHtml':ps[0] if ps else '', 'legacyImageUrl':img.group(1) if img else None,'legacySourceUrl':a.group(1) if a else None,'legacyAttributionHtml':ps[-1] if len(ps)>1 else None,'migrationStatus':'rewritten and reviewed; image withheld pending rights review'})
(root/'legacy/migration-inventory.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
print(f'Preserved {len(items)} original profiles across {len(set(x["legacyCategory"] for x in items))} categories')
