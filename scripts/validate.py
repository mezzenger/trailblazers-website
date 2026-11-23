#!/usr/bin/env python3
"""Validate researched content; --require-100 is the release milestone gate."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    'id', 'name', 'born', 'died', 'region', 'place', 'era', 'categories',
    'featured', 'lesserKnown', 'summary', 'biography', 'achievements',
    'milestones', 'sources', 'image', 'verification', 'reviewed',
}
ID = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
IMAGE_FIELDS = ('url', 'creator', 'source', 'license', 'attribution')


def load_collection():
    pending = ROOT / 'content/pending.json'
    return (
        json.loads((ROOT / 'content/profiles.json').read_text(encoding='utf-8')),
        json.loads(pending.read_text(encoding='utf-8')) if pending.exists() else [],
    )


def has_text(value):
    return isinstance(value, str) and bool(value.strip())


def is_date(value, partial=False):
    pattern = r'[0-9]{4}(?:-[0-9]{2}(?:-[0-9]{2})?)?' if partial else r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    if not isinstance(value, str) or not re.fullmatch(pattern, value):
        return False
    expanded = {4: '-01-01', 7: '-01'}.get(len(value), '')
    try:
        date.fromisoformat(value + expanded)
    except ValueError:
        return False
    return True


def https_domain(value):
    if not has_text(value) or re.search(r'[\s<>\\]', value):
        return None
    try:
        url = urlsplit(value)
        host = url.hostname
        port = url.port
    except ValueError:
        return None
    if (url.scheme != 'https' or not host or url.username is not None
            or not re.fullmatch(r'[a-z0-9-]+(?:\.[a-z0-9-]+)+\.?', host)
            or host.rstrip('.').startswith('example.') or port == 0):
        return None
    return host.rstrip('.').removeprefix('www.')

def validate_image(image, label, errors):
    if not isinstance(image, dict) or not all(has_text(image.get(field)) for field in IMAGE_FIELDS):
        errors.append(f'{label}: image needs url, creator, source, license, and attribution')
        return
    if not https_domain(image['url']) or not https_domain(image['source']):
        errors.append(f'{label}: image asset and rights record need HTTPS URLs')
    if ('licenseUrl' in image or image['license'].startswith('CC BY')) and not https_domain(image.get('licenseUrl')):
        errors.append(f'{label}: image license needs an HTTPS URL')
    if not isinstance(image.get('preserveFraming', False), bool):
        errors.append(f'{label}: image preserveFraming must be true or false')
    if 'alt' in image and not has_text(image['alt']):
        errors.append(f'{label}: image alt description must contain text')


def validate_collection(profiles, pending):
    errors = []
    if not isinstance(profiles, list):
        errors.append('profiles.json must contain an array')
    if not isinstance(pending, list):
        errors.append('pending.json must contain an array')
    if errors:
        return errors, 0
    if not profiles:
        errors.append('profiles.json must contain at least one publishable profile')

    ids, names = set(), set()

    def check_identity(item, label):
        identifier = item.get('id')
        name = item.get('name')
        if not isinstance(identifier, str) or not ID.fullmatch(identifier):
            errors.append(f'{label}: invalid ID')
        elif identifier in ids:
            errors.append(f'{label}: duplicate ID')
        else:
            ids.add(identifier)
        if not has_text(name):
            errors.append(f'{label}: missing name')
        elif name.strip().casefold() in names:
            errors.append(f'{label}: duplicate name')
        else:
            names.add(name.strip().casefold())

    source_count = 0
    for index, item in enumerate(profiles, 1):
        if not isinstance(item, dict):
            errors.append(f'profile {index}: expected an object')
            continue
        label = item.get('id') or f'profile {index}'
        check_identity(item, label)
        if item.keys() - {'gallery'} != REQUIRED:
            errors.append(f'{label}: schema keys differ from required set')
        if item.get('verification') != 'verified':
            errors.append(f'{label}: unpublished record in publishable dataset')
        if not is_date(item.get('reviewed')):
            errors.append(f'{label}: invalid review date')
        for field in ('born', 'died'):
            value = item.get(field)
            if value is not None and not is_date(value, partial=True):
                errors.append(f'{label}: invalid {field}')
        for field in ('region', 'place', 'era', 'summary'):
            if not has_text(item.get(field)):
                errors.append(f'{label}: missing {field}')
        for field in ('featured', 'lesserKnown'):
            if not isinstance(item.get(field), bool):
                errors.append(f'{label}: {field} must be true or false')
        for field in ('categories', 'achievements'):
            values = item.get(field)
            if not isinstance(values, list) or not values or not all(map(has_text, values)):
                errors.append(f'{label}: {field} must be a nonempty list of text')
            elif field == 'categories' and len(set(values)) != len(values):
                errors.append(f'{label}: duplicate category')

        biography = item.get('biography')
        words = len(re.findall(r"\b[\w’'-]+\b", biography)) if isinstance(biography, str) else 0
        if not 150 <= words <= 300:
            errors.append(f'{label}: biography {words} words (expected 150–300)')
        milestones = item.get('milestones')
        if not isinstance(milestones, list) or not milestones:
            errors.append(f'{label}: milestones missing')
        elif any(
            not isinstance(m, dict) or type(m.get('year')) is not int
            or not 1 <= m['year'] <= 9999 or not has_text(m.get('label'))
            for m in milestones
        ):
            errors.append(f'{label}: milestones need an integer year and a label')

        sources = item.get('sources')
        domains = set()
        if not isinstance(sources, list) or len(sources) < 2:
            errors.append(f'{label}: fewer than two sources')
        if isinstance(sources, list):
            for source in sources:
                domain = https_domain(source.get('url')) if isinstance(source, dict) else None
                if not domain or not has_text(source.get('title')):
                    errors.append(f'{label}: source needs an HTTPS URL and title')
                else:
                    domains.add(domain)
                    source_count += 1
        if len(domains) < 2:
            errors.append(f'{label}: two independent source domains required')

        image = item.get('image')
        if image is not None:
            validate_image(image, label, errors)
        gallery = item.get('gallery', [])
        if not isinstance(gallery, list):
            errors.append(f'{label}: gallery must be a list of images')
        else:
            for position, photo in enumerate(gallery, 1):
                photo_label = f'{label} gallery photo {position}'
                validate_image(photo, photo_label, errors)
                if isinstance(photo, dict) and not all(has_text(photo.get(key)) for key in ('caption', 'alt')):
                    errors.append(f'{photo_label}: image needs a caption and alt description')

    for index, item in enumerate(pending, 1):
        label = f'pending candidate {index}'
        if not isinstance(item, dict):
            errors.append(f'{label}: expected an object')
            continue
        check_identity(item, label)
        if item.get('verification') != 'pending':
            errors.append(f'{label}: expected pending verification')

    return errors, source_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-100', action='store_true')
    args = parser.parse_args()
    try:
        profiles, pending = load_collection()
    except (OSError, ValueError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    errors, source_count = validate_collection(profiles, pending)
    total = len(profiles) if isinstance(profiles, list) else 0
    pending_count = len(pending) if isinstance(pending, list) else 0
    if args.require_100 and not errors and total < 100:
        errors.append(f'100-profile milestone unmet: {total} verified; {100-total} more required')
    verified = f'{total} verified publishable profiles' if not errors else f'{total} publishable profile records'
    print(f'{verified}; {pending_count} pending discovery candidates; {source_count} source citations; {len(errors)} validation errors')
    for error in errors:
        print('ERROR:', error)
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
