#!/usr/bin/env python3
"""Check Wikimedia Commons file identity and license claims; fail closed on uncertainty.

Runs on a network-enabled machine. Does not equate a Commons page with permission
to reuse an image: human review of attribution and jurisdiction remains required.
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'commons-provenance-report.json'
API = 'https://commons.wikimedia.org/w/api.php'
HEADERS = {'User-Agent': 'TrailblazersMuseumProvenanceAudit/1.0 (github.com/mezzenger/trailblazers-website)'}


def plain(value):
    value = re.sub(r'<[^>]+>', ' ', html.unescape(value or ''))
    return ' '.join(value.split())


def license_family(value):
    value = (value or '').lower()
    if re.search(r'\bcc\s*by[- ]sa\b|attribution-sharealike', value):
        return 'by-sa'
    if re.search(r'\bcc\s*by\b|attribution\s+\d', value):
        return 'by'
    if 'cc0' in value or 'public domain' in value or 'pd-' in value:
        return 'pd'
    if 'gfdl' in value:
        return 'gfdl'
    return None


def commons_title(source):
    u = urllib.parse.urlsplit(source)
    if u.scheme != 'https' or u.netloc != 'commons.wikimedia.org':
        return None
    prefix = '/wiki/File:'
    if not u.path.startswith(prefix):
        return None
    return 'File:' + urllib.parse.unquote(u.path[len(prefix):]).replace('_', ' ')


def fetch_batch(titles):
    params = urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'formatversion': 2,
        'redirects': 1, 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|mime',
        'titles': '|'.join(titles)
    })
    request = urllib.request.Request(API + '?' + params, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def main():
    profiles = json.loads((ROOT / 'content/profiles.json').read_text())
    items = []
    for person in profiles:
        for kind, images in (
            ('portrait', [person['image']] if person.get('image') else []),
            ('gallery', person.get('gallery', []))
        ):
            for image in images:
                items.append({'profile': person['id'], 'kind': kind, **image})
    by_title = {}
    for item in items:
        title = commons_title(item['source'])
        item['commons_title'] = title
        if title:
            by_title.setdefault(title, []).append(item)

    errors = []
    records = []
    for offset in range(0, len(by_title), 20):
        titles = list(by_title)[offset:offset + 20]
        try:
            data = fetch_batch(titles)
        except Exception as exc:
            errors.append(f'Commons API unavailable for batch {offset // 20 + 1}: {type(exc).__name__}: {exc}')
            continue
        pages = {p['title'].replace('_', ' '): p for p in data.get('query', {}).get('pages', [])}
        normalized = {p['title'].replace('_', ' ').casefold(): p for p in pages.values()}
        for title in titles:
            page = normalized.get(title.casefold())
            for item in by_title[title]:
                problems = []
                if not page or page.get('missing') or not page.get('imageinfo'):
                    problems.append('file missing or no image information')
                    meta = {}
                    actual_url = None
                else:
                    info = page['imageinfo'][0]
                    meta = {k: plain(v.get('value', '')) for k, v in info.get('extmetadata', {}).items()}
                    actual_url = info.get('url')
                    expected = license_family(item['license'])
                    actual = license_family(meta.get('LicenseShortName', '') + ' ' + meta.get('UsageTerms', ''))
                    if not actual:
                        problems.append('Commons has no classifiable reuse license')
                    elif expected != actual:
                        problems.append(f'license family mismatch: claimed {expected}, Commons {actual}')
                    if meta.get('Restrictions'):
                        problems.append('Commons reuse restrictions require review')
                    if not actual_url or info.get('mime', '').split('/')[0] != 'image':
                        problems.append('Commons image asset absent or not an image')
                record = {
                    'profile': item['profile'], 'kind': item['kind'],
                    'source': item['source'], 'asset': item['url'],
                    'commonsTitle': page.get('title') if page else title,
                    'creatorClaim': item['creator'], 'licenseClaim': item['license'],
                    'commonsCreator': meta.get('Artist', '') or meta.get('Attribution', ''),
                    'commonsLicense': meta.get('LicenseShortName', ''),
                    'commonsUsageTerms': meta.get('UsageTerms', ''),
                    'commonsAsset': actual_url,
                    'problems': problems,
                }
                records.append(record)
                for problem in problems:
                    errors.append(f"{item['profile']} {item['kind']}: {problem}: {title}")

    for item in items:
        if not item['commons_title']:
            errors.append(f"{item['profile']} {item['kind']}: source not a Commons File page (requires separate review)")
    if len(records) != len([i for i in items if i['commons_title']]):
        errors.append('Incomplete Commons metadata coverage')

    report = {
        'checkedAt': datetime.now(timezone.utc).isoformat(),
        'imageCount': len(items), 'checkedCommonsRecords': len(records),
        'errors': errors, 'records': records,
        'note': 'Metadata comparison only; manual file identity, rights, attribution, changes, and territories still require human review.'
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(f"Commons provenance: {len(records)}/{len(items)} image records queried; {len(errors)} issues")
    for issue in errors:
        print('REVIEW:', issue)
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
