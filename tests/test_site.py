import importlib.util, json, os, re, shutil, subprocess, tempfile, unittest
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from unittest.mock import call, patch
ROOT=Path(__file__).resolve().parents[1]
BASE='/trailblazers-website/'
LINK_AUDIT_SPEC=importlib.util.spec_from_file_location('check_external_links',ROOT/'scripts/check_external_links.py')
LINK_AUDIT=importlib.util.module_from_spec(LINK_AUDIT_SPEC);LINK_AUDIT_SPEC.loader.exec_module(LINK_AUDIT)
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[];self.tags=[];self.labels=[];self.inputs=[];self.anchor_depth=0;self.nested_anchors=0;self.images_without_alt=[];self.card_links=[];self.category_jumps=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append(tag)
        if 'id' in attrs:self.ids.add(attrs['id'])
        if attrs.get('data-category-jump'):self.category_jumps.append(attrs['data-category-jump'])
        if tag=='a':
            if self.anchor_depth:self.nested_anchors+=1
            self.anchor_depth+=1
            if 'card-link' in attrs.get('class','').split():self.card_links.append(attrs)
        if tag=='img' and not attrs.get('alt'):self.images_without_alt.append(attrs.get('src'))
        if tag in ('a','link','script','img'):
            target=attrs.get('href') or attrs.get('src')
            if target:self.links.append(target)
        if tag=='label' and 'for' in attrs:self.labels.append(attrs['for'])
        if tag in ('input','select') and 'id' in attrs:self.inputs.append(attrs['id'])
    def handle_endtag(self,tag):
        if tag=='a':self.anchor_depth=max(0,self.anchor_depth-1)

@cache
def read_document(page):
    doc = Document()
    doc.feed(page.read_text(encoding='utf-8'))
    return doc

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ['python3', 'scripts/build.py'],
            cwd=ROOT, capture_output=True, text=True,
        )
        if result.returncode:
            raise AssertionError(
                f'Museum build failed (exit {result.returncode})\\n'
                f'stdout:\\n{result.stdout}\\n'
                f'stderr:\\n{result.stderr}'
            )
        cls.profiles=json.loads((ROOT/'content/profiles.json').read_text())
    def test_all_profile_routes_and_internal_links(self):
        pages=[ROOT/'dist/index.html',ROOT/'dist/404.html']+list((ROOT/'dist/people').glob('*/index.html'))
        self.assertEqual(len(pages),len(self.profiles)+2)
        for page in pages:
            doc=read_document(page)
            self.assertIn('main',doc.tags)
            self.assertEqual(doc.nested_anchors,0,f'{page}: nested anchors')
            self.assertEqual(doc.images_without_alt,[],f'{page}: image missing alt')
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
                    target_doc=read_document(target)
                    self.assertIn(parsed.fragment,target_doc.ids,f'{page}: broken anchor {link}')
    def test_semantics_and_responsive_rules(self):
        home=(ROOT/'dist/index.html').read_text();css=(ROOT/'dist/styles.css').read_text()
        self.assertIn('class="skip-link"',home)
        self.assertIn('aria-live="polite"',home)
        self.assertIn('@media(max-width:700px)',css)
        self.assertIn('prefers-reduced-motion:reduce',css)
        self.assertIn('type="module"',home)
        profile=(ROOT/'dist/people'/self.profiles[0]['id']/'index.html').read_text()
        self.assertIn('<h2 class="eyebrow">Milestones</h2>',profile)
        self.assertIn('<h2 class="eyebrow">Sources &amp; further reading</h2>',profile)
    def test_card_link_accessible_name_comes_from_visible_content(self):
        doc=Document();doc.feed((ROOT/'dist/index.html').read_text())
        self.assertTrue(doc.card_links)
        for link in doc.card_links:
            self.assertNotIn('aria-label',link,'card links must derive their name from visible text')
    def test_category_discovery_covers_the_dataset(self):
        doc=Document();doc.feed((ROOT/'dist/index.html').read_text())
        categories={category for profile in self.profiles for category in profile['categories']}
        self.assertEqual(set(doc.category_jumps),categories)
        self.assertEqual(len(doc.category_jumps),len(categories))
    def test_link_audit_distinguishes_dead_links_from_access_restrictions(self):
        self.assertEqual(LINK_AUDIT.classify_status(200),'reachable')
        self.assertEqual(LINK_AUDIT.classify_status(404),'broken')
        self.assertEqual(LINK_AUDIT.classify_status(410),'broken')
        self.assertEqual(LINK_AUDIT.classify_status(403),'restricted')
        self.assertEqual(LINK_AUDIT.classify_status(429),'restricted')
        self.assertEqual(LINK_AUDIT.classify_status(500),'unavailable')
        url = 'https://museum.org/portrait'
        with patch.object(LINK_AUDIT, 'request_url', side_effect=[
            (404, url, 'Not found'), (None, url, 'TimeoutError'),
        ]):
            self.assertEqual(LINK_AUDIT.check_url(url)['classification'], 'unavailable')
        with patch.object(LINK_AUDIT, 'request_url', side_effect=[
            (410, url, 'Gone'), (410, url, 'Gone'),
        ]):
            self.assertEqual(LINK_AUDIT.check_url(url)['classification'], 'broken')
        with patch.object(LINK_AUDIT, 'request_url', side_effect=[
            (405, url, 'Method not allowed'), (416, url, 'Range not satisfiable'), (200, url, None),
        ]) as request:
            self.assertEqual(LINK_AUDIT.check_url(url)['classification'], 'reachable')
            self.assertEqual(request.call_args_list, [
                call(url, 'HEAD'), call(url, 'GET', ranged=True), call(url, 'GET'),
            ])
    def test_accent_text_contrast_in_both_themes(self):
        css=(ROOT/'public/styles.css').read_text()
        light,dark=css.split(':root[data-theme=dark]',1)
        dark=dark.split('}',1)[0]
        def color(block,name):
            return re.search(rf'--{name}:#([0-9a-f]{{6}})',block).group(1)
        def luminance(value):
            rgb=[int(value[i:i+2],16)/255 for i in (0,2,4)]
            linear=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in rgb]
            return sum(x*y for x,y in zip(linear,(0.2126,0.7152,0.0722)))
        for theme,backgrounds in ((light,('paper','ivory','card')),(dark,('paper','ivory','card'))):
            accent=luminance(color(theme,'accent-text'))
            for name in backgrounds:
                background=luminance(color(theme,name))
                ratio=(max(accent,background)+0.05)/(min(accent,background)+0.05)
                self.assertGreaterEqual(ratio,4.5,f'{name} accent text contrast {ratio:.2f}')
    def test_combined_search_filters_and_sort(self):
        js='''import fs from 'node:fs'; import {matchesProfile,compareProfiles} from './public/filter-core.mjs';
const p=JSON.parse(fs.readFileSync('content/profiles.json'));
const a=p.filter(x=>matchesProfile(x,{search:'malaria',category:'Medicine & Public Health',era:'20th century',region:'Asia'}));
if(a.length!==1||a[0].id!=='tu-youyou')process.exit(1);
const b=p.filter(x=>matchesProfile(x,{search:'relay bronze',category:'Sports',era:'20th century',region:'North America'}));
if(b.length!==1||b[0].id!=='wilma-rudolph')process.exit(2);
const added=p.filter(x=>matchesProfile(x,{search:'parity violation',category:'Science & Innovation',era:'20th century',region:'Asia'}));
if(added.length!==1||added[0].id!=='chien-shiung-wu')process.exit(5);
const accent=p.filter(x=>matchesProfile(x,{search:'kariko',category:'Science & Innovation',era:'21st century',region:'Europe'}));
if(accent.length!==1||accent[0].id!=='katalin-karik')process.exit(6);
const c=[...p].sort((x,y)=>compareProfiles(x,y,'born'));
if(c.some((x,i)=>i>0&&compareProfiles(c[i-1],x,'born')>0))process.exit(3);
const d=[...p].sort((x,y)=>compareProfiles(x,y,'period'));
if(d.some((x,i)=>i>0&&compareProfiles(d[i-1],x,'period')>0))process.exit(4);
const earlier={name:'Z',milestones:[{year:2020},{year:999}]};
const later={name:'A',milestones:[{year:1000}]};
if(compareProfiles(earlier,later,'period')>=0)throw Error('period must use the earliest milestone numerically');
'''
        subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,check=True)
    def test_homepage_script_applies_search_filters_with_unknown_birth_dates(self):
        js='''import fs from 'node:fs';
const people=JSON.parse(fs.readFileSync('content/profiles.json'));
const cards=people.map(person=>({dataset:{profile:JSON.stringify(person)},hidden:false}));
function control(value='') {return {value,addEventListener(type,fn){this[type]=fn},focus(){this.focused=true}}}
const search=control(),category=control(),era=control(),region=control(),sort=control('name');
const count={textContent:''},empty={hidden:true},clear=control();
const grid={querySelectorAll(){return cards},replaceChildren(...items){this.children=items}};
const theme=control();
theme.setAttribute=function(key,value){this[key]=value};
const fallback={hidden:true},credit={hidden:false};
const image=control();
image.parentElement={querySelector(key){return key==='.credit'?credit:fallback}};
const elements={'#search':search,'#category':category,'#era':era,'#region':region,'#sort':sort,'#card-grid':grid,'#result-count':count,'#empty-state':empty,'#clear-filters':clear,'.theme-toggle':theme};
globalThis.document={documentElement:{dataset:{}},querySelector(key){return elements[key]??null},querySelectorAll(key){return key==='.portrait-frame img'?[image]:[]}};
globalThis.localStorage={getItem(){throw Error('storage blocked')},setItem(){throw Error('storage blocked')}};
await import('./public/app.js');
if(count.textContent!==`Showing ${people.length} people`)throw Error('initial collection did not render');
theme.click();
if(document.documentElement.dataset.theme!=='dark'||theme['aria-pressed']!=='true')throw Error('theme needs to work without storage');
image.error();
if(!image.hidden||!credit.hidden||fallback.hidden)throw Error('broken portrait must show its placeholder');
search.value='kariko';category.value='Science & Innovation';era.value='21st century';region.value='Europe';search.input();
if(cards.filter(card=>!card.hidden).map(card=>JSON.parse(card.dataset.profile).id).join()!=='katalin-karik')throw Error('combined filters failed');
search.value='no matching biography';search.input();
if(!cards.every(card=>card.hidden)||empty.hidden)throw Error('empty state failed');
clear.click();
if(cards.some(card=>card.hidden)||!empty.hidden||!search.focused)throw Error('clear filters failed');
sort.value='born';sort.change();
const last=grid.children.slice(-3).map(card=>JSON.parse(card.dataset.profile).born);
if(!last.every(value=>value===null))throw Error('unknown birth dates should sort last');
'''
        subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,check=True)
    def test_validation_and_milestone_gate(self):
        good=subprocess.run(['python3','scripts/validate.py'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(good.returncode,0,good.stdout)
        gate=subprocess.run(['python3','scripts/validate.py','--require-100'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(gate.returncode,0,gate.stdout)
        self.assertIn(f'{len(self.profiles)} verified publishable profiles',gate.stdout)
        with tempfile.TemporaryDirectory() as temporary:
            fixture=Path(temporary)
            (fixture/'scripts').mkdir();(fixture/'content').mkdir()
            shutil.copy(ROOT/'scripts/validate.py',fixture/'scripts/validate.py')
            (fixture/'content/profiles.json').write_text(json.dumps(self.profiles[:99]))
            (fixture/'content/pending.json').write_text('[]')
            short=subprocess.run(['python3','scripts/validate.py','--require-100'],cwd=fixture,capture_output=True,text=True)
            self.assertNotEqual(short.returncode,0,short.stdout)
            self.assertIn('100-profile milestone unmet: 99 verified; 1 more required',short.stdout)
            shutil.copy(ROOT/'scripts/build.py', fixture/'scripts/build.py')
            (fixture/'dist').mkdir()
            old_output = fixture/'dist/index.html'
            old_output.write_text('previous build')
            invalid = dict(self.profiles[0], born='2000-02-30', milestones=[{'year':'2000','label':'Text'}],
                           image={'url':'https://museum.org/a','source':'http://museum.org/rights',
                                  'creator':'Name','license':'Public domain','attribution':'Name'})
            (fixture/'content/profiles.json').write_text(json.dumps([invalid]))
            broken = subprocess.run(['python3','scripts/build.py'],cwd=fixture,capture_output=True,text=True)
            self.assertNotEqual(broken.returncode, 0)
            for message in ('invalid born', 'integer year', 'rights record need HTTPS'):
                self.assertIn(message, broken.stderr)
            self.assertEqual(old_output.read_text(), 'previous build')
    def test_profile_gallery_and_pending_visibility(self):
        profile = next(person for person in self.profiles if person['id'] == 'sara-seager')
        profile_page = ROOT/'dist/people/sara-seager/index.html'
        document = read_document(profile_page)
        body = profile_page.read_text(encoding='utf-8')
        self.assertIn('class="story-gallery"', body)
        audit_links = LINK_AUDIT.collect_urls()
        for image in [profile['image'], *profile['gallery']]:
            self.assertIn(image['url'], document.links)
            self.assertIn(image['source'], document.links)
            self.assertIn(image['source'], audit_links)
        home_links = read_document(ROOT/'dist/index.html').links
        for candidate in json.loads((ROOT/'content/pending.json').read_text()):
            self.assertNotIn(f"{BASE}people/{candidate['id']}/", home_links)
            self.assertFalse((ROOT/'dist/people'/candidate['id']).exists())

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
