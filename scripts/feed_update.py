#!/usr/bin/env python
"""Generate a feed from HTML files."""

import datetime
import os
import re

import utils

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
SITE_DIRECTORY = os.path.join(THIS_DIR, "..", "site")
FEED_PATH = os.path.join(THIS_DIR, "..", "site", "atom.xml")


def _scrape_html(path):
    with open(path, "r", encoding="utf-8") as html_file:
        publication_date = None
        updated_date = None
        for line in html_file:
            if "publication-date" in line:
                # Very inflexible - just expects YYYY-MM-DD (with zeros)
                match = re.search(r'[^\d]*(\d{4}-\d{2}-\d{2}).*', line)
                if match:
                    publication_date = match.group(1)
            if "updated-date" in line:
                # Very inflexible - just expects YYYY-MM-DD (with zeros)
                match = re.search(r'[^\d]*(\d{4}-\d{2}-\d{2}).*', line)
                if match:
                    updated_date = match.group(1)
            if publication_date is not None and updated_date is not None:
                break
    return publication_date, updated_date


def _feed_header():
    lines = []

    # Truncate to the nearest hour for privacy reasons,
    # and to avoid complications with git status when deploying
    # via a Git-based approach (e.g. Github pages).
    datetime_string = datetime.datetime.now().astimezone().replace(
        minute=0,second=0,microsecond=0).isoformat()

    lines.append('<?xml version="1.0" encoding="utf-8"?>\n')
    lines.append('<feed xmlns="http://www.w3.org/2005/Atom">\n')
    lines.append('<title>patricksanan.org</title>\n')
    lines.append('<link href="https://patricksanan.org/" ref="alternate"/>\n')
    lines.append(
        '<link href="https://patricksanan.org/feeds/all.atom.xml" rel="self"/>\n'
    )
    lines.append(f'<updated>{datetime_string}</updated>\n')
    lines.append('<author><name>Patrick Sanan</name> </author>\n')
    lines.append('<id>https://patricksanan.org</id>\n')
    lines.append(f'<rights>{utils.copyright_string(html=False)}</rights>\n')
    return lines


def _feed_footer():
    return ['</feed>\n']


def _feed_entry(filename, publication_datetime, updated_datetime=None):
    title = filename  # better to scrape file for title
    lines = []
    lines.append('<entry>\n')
    lines.append(f'<title>{title}</title>\n')
    lines.append(f'<link href="https://patricksanan.org/{filename}"/>\n')
    lines.append(
        f'<id>https://patricksanan.org/{filename}</id>\n')  # bad practice!
    lines.append(f'<published>{publication_datetime}</published>\n')
    if updated_datetime is not None:
        lines.append(f'<updated>{updated_datetime}</updated>\n')
    lines.append(f'<summary>https://patricksanan.org/{filename}</summary>\n')
    lines.append(f'<content>https://patricksanan.org/{filename}</content>\n'
                )  # actual content would be better
    lines.append('</entry>\n')
    return lines


def _generate_feed():
    feed_lines = _feed_header()

    # In alphabetical order, but reverse chronological by publication date might be nice
    for filename in sorted(
        [f for f in os.listdir(SITE_DIRECTORY) if f.endswith(".html")]):
        path = os.path.join(SITE_DIRECTORY, filename)
        publication_date, updated_date = _scrape_html(path)
        if not updated_date:
            updated_date = publication_date

        print(f"  {filename} published: {publication_date} updated: {updated_date}")

        if publication_date is not None:
            feed_lines.extend(
                _feed_entry(filename, publication_date, updated_date))
    feed_lines.extend(_feed_footer())
    with open(FEED_PATH, "w", encoding="utf-8") as feed_file:
        feed_file.writelines(feed_lines)


def _main():
    _generate_feed()


if __name__ == "__main__":
    _main()
