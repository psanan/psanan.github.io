#!/usr/bin/env python3
"""Define the data format and utilities to read to and from files.

The main data structure is an "entry", simply a
dict with keys KEYS and lists of strings as values."""

import csv

KEYS = ["ch", "de", "en"]
PRIMARY_KEY = KEYS[0]
MAX_ALTERNATES = 4
TSV_COLUMN_KEYS = {
    "ch": [f"CH {i}" for i in range(1, MAX_ALTERNATES)],
    "de": [f"DE {i}" for i in range(1, MAX_ALTERNATES)],
    "en": [f"EN {i}" for i in range(1, MAX_ALTERNATES)],
}


def entries_from_tsv(path):
    """Load entries from a TSV file.

    The file is expected to have columns with strings for each language
    as in TSV_COLUMN_KEYS.

    A primary language is required in each row, and cannot have any duplicates amongst its keys.
    """
    rows = []
    entries = []

    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            rows.append(row)

    primary_keys_canonical = set()
    valid = True
    for row in rows:
        try:
            # Skip entirely empty rows, for convenience
            should_skip = True
            for key in KEYS:
                for column_key in TSV_COLUMN_KEYS[key]:
                    if row[column_key]:
                        should_skip = False
                        break
                if not should_skip:
                    break
            if should_skip:
                continue

            entry = {}
            for key in KEYS:
                entry[key] = []
                for column_key in TSV_COLUMN_KEYS[key]:
                    # Strip for convenience and to skip whitespace-only
                    key_canonical = row[column_key].strip()
                    if row[column_key]:
                        if key == PRIMARY_KEY:
                            if key_canonical in primary_keys_canonical:
                                print(
                                    f"WARNING: duplicate primary canonical key: {key_canonical}"
                                )
                                valid = False
                            primary_keys_canonical.add(key_canonical)
                        entry[key].append(key_canonical)
            if not entry[PRIMARY_KEY]:
                print(
                    f"WARNING: primary key missing in entry: {entry} from row: {row}"
                )
                valid = False
        except:
            print(f"Error processing row: {row}")
            raise
        entries.append(entry)

    if not valid:
        error_message = f"Invalid: {path}"
        raise Exception(error_message)

    return entries


def _empty_row_dict():
    row_dict = {}
    for key in TSV_COLUMN_KEYS:
        for column_key in TSV_COLUMN_KEYS[key]:
            row_dict[column_key] = ""
    return row_dict


def _row_dict_to_string(row_dict):
    sub_strings = []
    for key in TSV_COLUMN_KEYS:
        for column_key in TSV_COLUMN_KEYS[key]:
            sub_strings.append(row_dict[column_key])
    sub_strings.append("\n")
    return "\t".join(sub_strings)


def _header_string():
    sub_strings = []
    for key in TSV_COLUMN_KEYS:
        for column_key in TSV_COLUMN_KEYS[key]:
            sub_strings.append(column_key)
    sub_strings.append("\n")
    return "\t".join(sub_strings)


def tsv_from_entries(entries, path):
    """Save a list of entries back to a TSV file."""
    with open(path, "w") as file:
        file.write(_header_string())
        for entry in entries:
            row_dict = _empty_row_dict()
            for key in KEYS:
                if key in entry:
                    tsv_alternate_index = 0
                    for alternate in entry[key]:
                        if tsv_alternate_index >= MAX_ALTERNATES:
                            raise Exception(
                                f"Only {MAX_ALTERNATES} alternates allowed but {entry} has more"
                            )
                        row_dict[TSV_COLUMN_KEYS[key]
                                 [tsv_alternate_index]] = alternate
                        tsv_alternate_index += 1
            file.write(_row_dict_to_string(row_dict))


def entries_by_primary_key(entries):
    """Requires validated entries list (no duplicates)"""
    entries_by_primary_key = {}
    for entry in entries:
        for entry_primary_key in entry[PRIMARY_KEY]:
            entries_by_primary_key[entry_primary_key] = entry
    return entries_by_primary_key


if __name__ == "__main__":
    test_entries = entries_from_tsv("translations.tsv")
    out_path = "translations_testout.tsv"
    print(f"Dumping to {out_path}")
    tsv_from_entries(test_entries, out_path)
