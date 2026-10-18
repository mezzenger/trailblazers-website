import json, os, re, subprocess, unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT=Path(__file__).resolve().parents[1]
BASE='/trailblazers-website/'
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[];self.tags=[];self.labels=[];self.inputs=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append(tag)
        if 'id' in attrs:self.ids.add(attrs['id'])
        if tag in ('a','link','script','img'):
            target=attrs.get('href') or attrs.get('src')
            if target:self.links.append(target)
        if tag=='label' and 'for' in attrs:self.labels.append(attrs['for'])
        if tag in ('input','select') and 'id' in attrs:self.inputs.append(attrs['id'])
class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(['python3','scripts/build.py'],cwd=ROOT,check=True,capture_output=True)
        cls.profiles=json.loads((ROOT/'content/profiles.json').read_text())
    def test_all_profile_routes_and_internal_links(self):
        pages=[ROOT/'dist/index.html',ROOT/'dist/404.html']+list((ROOT/'dist/people').glob('*/index.html'))
        self.assertEqual(len(pages),len(self.profiles)+2)
        for page in pages:
            doc=Document();doc.feed(page.read_text())
            self.assertIn('main',doc.tags)
            self.assertIn('nav',doc.tags)
            self.assertIn('main',doc.ids)
            self.assertTrue(set(doc.labels).issubset(doc.ids))
            for link in doc.links:
                if link.startswith('http') or link.startswith('mailto:'):continue
                parsed=urlsplit(link)
                self.assertTrue(link.startswith(BASE) or link.startswith('#'),f'{page}: {link}')
                if link.startswith('#'):
                    target=page
                else:
                    rel=unquote(parsed.path[len(BASE):]);target=ROOT/'dist'/rel
                    if target.is_dir():target=target/'index.html'
                self.assertTrue(target.exists(),f'{page}: broken {link}')
                if parsed.fragment:
                    target_doc=Document();target_doc.feed(target.read_text())
                    self.assertIn(parsed.fragment,target_doc.ids,f'{page}: broken anchor {link}')
    def test_semantics_and_responsive_rules(self):
        home=(ROOT/'dist/index.html').read_text();css=(ROOT/'dist/styles.css').read_text()
        self.assertIn('class="skip-link"',home)
        self.assertIn('aria-live="polite"',home)
        self.assertIn('@media(max-width:700px)',css)
        self.assertIn('prefers-reduced-motion:reduce',css)
        self.assertIn('type="module"',home)
    def test_combined_search_filters_and_sort(self):
        js='''import fs from 'node:fs'; import {matchesProfile,compareProfiles} from './public/filter-core.mjs';
const p=JSON.parse(fs.readFileSync('content/profiles.json'));
const a=p.filter(x=>matchesProfile(x,{search:'malaria',category:'Medicine & Public Health',era:'20th century',region:'Asia'}));
if(a.length!==1||a[0].id!=='tu-youyou')process.exit(1);
const b=p.filter(x=>matchesProfile(x,{search:'olympic',category:'Sports',era:'20th century',region:'North America'}));
if(b.length!==1||b[0].id!=='wilma-rudolph')process.exit(2);
const c=[...p].sort((x,y)=>compareProfiles(x,y,'born'));
if(c[0].id!=='madam-c-j-walker')process.exit(3);
const d=[...p].sort((x,y)=>compareProfiles(x,y,'period'));
if(d[0].id!=='madam-c-j-walker')process.exit(4);
'''
        subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,check=True)
    def test_validation_and_milestone_gate(self):
        good=subprocess.run(['python3','scripts/validate.py'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(good.returncode,0,good.stdout)
        gate=subprocess.run(['python3','scripts/validate.py','--require-100'],cwd=ROOT,capture_output=True,text=True)
        self.assertNotEqual(gate.returncode,0)
        self.assertIn('100-profile milestone unmet',gate.stdout)
    def test_base_path_override(self):
        env=dict(os.environ,BASE_PATH='/')
        try:
            subprocess.run(['python3','scripts/build.py'],cwd=ROOT,env=env,check=True,capture_output=True)
            home=(ROOT/'dist/index.html').read_text()
            self.assertIn('href="/styles.css"',home)
            self.assertIn('href="/people/',home)
        finally:
            subprocess.run(['python3','scripts/build.py'],cwd=ROOT,check=True,capture_output=True)
if __name__=='__main__':unittest.main()
