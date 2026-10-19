#!/usr/bin/env python3
"""Audit external citations and portrait resources without conflating blocks with dead links."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'external-link-report.json'
TIMEOUT = 15


def classify_status(status):
    if 200 <= status < 400:
        return 'reachable'
    if status in (404, 410):
        return 'broken'
    if status in (401, 403, 407, 429):
        return 'restricted'
    return 'unavailable'


def request_url(url, method):
    headers = {'User-Agent': 'TrailblazersOfHistory-LinkReview/1.0 (+https://github.com/mezzenger/trailblazers-website)',
               'Range': 'bytes=0-0'}
    try:
        request = Request(url, headers=headers, method=method)
        with urlopen(request, timeout=TIMEOUT) as response:
            if method == 'GET':
                response.read(1)
            return response.status, response.geturl(), None
    except HTTPError as error:
        return error.code, error.geturl(), str(error.reason)
    except (URLError, TimeoutError, OSError, ValueError) as error:
        return None, url, type(error).__name__


def check_url(url):
    status, final_url, detail = request_url(url, 'HEAD')
    if status in (400, 403, 404, 405, 410, 501):
        retry_status, retry_url, retry_detail = request_url(url, 'GET')
        if retry_status is not None or status == 405:
            status, final_url, detail = retry_status, retry_url, retry_detail
    return {
        'url': url,
        'finalUrl': final_url,
        'statusCode': status,
        'classification': classify_status(status) if status is not None else 'unavailable',
        'detail': detail,
    }


def collect_urls():
    profiles = json.loads((ROOT / 'content/profiles.json').read_text())
    links = {}
    def add(url, reference):
        links.setdefault(url, []).append(reference)
    for profile in profiles:
        for source in profile['sources']:
            add(source['url'], {'profile': profile['id'], 'kind': 'citation', 'title': source['title']})
        image = profile.get('image')
        if image:
            add(image['url'], {'profile': profile['id'], 'kind': 'portrait-asset', 'title': image['creator']})
            add(image['source'], {'profile': profile['id'], 'kind': 'portrait-rights-record', 'title': image['license']})
        for index, gallery_image in enumerate(profile.get('gallery', [])):
            add(gallery_image['url'], {'profile': profile['id'], 'kind': 'gallery-asset', 'title': gallery_image['caption']})
            add(gallery_image['source'], {'profile': profile['id'], 'kind': 'gallery-rights-record', 'title': gallery_image['license']})
    return links


def main():
    links = collect_urls()
    results = {}
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(check_url, url): url for url in links}
        for future in as_completed(futures):
            result = future.result()
            result['references'] = links[result['url']]
            results[result['url']] = result
    ordered = [results[url] for url in sorted(results)]
    counts = {name: sum(row['classification'] == name for row in ordered)
              for name in ('reachable', 'broken', 'restricted', 'unavailable')}
    report = {
        'checkedAt': datetime.now(timezone.utc).isoformat(),
        'uniqueUrls': len(ordered),
        'counts': counts,
        'results': ordered,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"External link audit: {len(ordered)} unique URLs — " + ', '.join(f'{key}: {value}' for key, value in counts.items()))
    for result in ordered:
        if result['classification'] != 'reachable':
            print(f"{result['classification'].upper()}: {result['statusCode'] or 'no response'} {result['url']}")
    return 1 if counts['broken'] else 0


if __name__ == '__main__':
    sys.exit(main())
