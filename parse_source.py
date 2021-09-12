#!/usr/bin/env python3

"""
Convert from the original nested JSON source to a relational format.
"""

import json
from pprint import pprint
import csv
from collections import defaultdict
from pathlib import Path

# Build base path of operation
BASE_PATH = Path(__file__).parent / "original"


def parse_entry(entry):
    """
    Parse a single entry in JSON format, mostly flattening it.
    """

    # Collect info for the root table
    root = {
        "root_id": entry["EGY_ROOT__ID"],
        "root_form": entry["EGY_ROOT__form"],
        "root_meaning_en": entry["EGY_ROOT__meaning_en"],
    }
    if entry["EGY_ROOT__TLA_ROOT"]:
        tla_root = list(entry["EGY_ROOT__TLA_ROOT"].values())[0]
        root["tla_root_id"] = tla_root["TLA_ROOT__ID"]
        root["tla_root_form"] = tla_root["TLA_ROOT__form"]
        root["tla_root_meaning_en"] = tla_root["TLA_ROOT__meaning_en"]
        root["tla_root_meaning_de"] = tla_root["TLA_ROOT__meaning_de"]
    else:
        root["tla_root_id"] = ""
        root["tla_root_form"] = ""
        root["tla_root_meaning_en"] = ""
        root["tla_root_meaning_de"] = ""

    # Collect info for the CCL table
    ccl = []
    for form in entry["CCL__forms"].values():
        ccl.append(form)

    # Collect info for the TLA table
    tla = []
    for form in entry["TLA__forms"].values():
        tla.append(form)

    # Collect matches
    matches = []
    for match in entry["MATCHES"].values():
        matches.append(match)

    return root, ccl, tla, matches


def write_root(root, filename):
    """
    Write the `root` table.
    """

    with open(filename, "w", encoding="utf-8") as handler:
        writer = csv.DictWriter(
            handler,
            delimiter="\t",
            fieldnames=[
                "root_id",
                "root_form",
                "root_meaning_en",
                "tla_root_form",
                "tla_root_id",
                "tla_root_meaning_en",
                "tla_root_meaning_de",
            ],
        )
        writer.writeheader()
        writer.writerows(root)


def write_ccl(ccl, filename):
    """
    Write the `ccl` table.
    """

    with open(filename, "w", encoding="utf-8") as handler:
        writer = csv.DictWriter(
            handler,
            delimiter="\t",
            fieldnames=["CCL__ID", "CCL__form", "CCL__meaning_en"],
        )
        writer.writeheader()
        writer.writerows(ccl)


def write_ccl_match(ccl_match, filename):
    """
    Write the `ccl_match` table.
    """

    with open(filename, "w", encoding="utf-8") as handler:
        handler.write("match_id\tccl_id\n")
        for match_id, ccl_ids in ccl_match.items():
            for ccl_id in ccl_ids:
                handler.write(match_id)
                handler.write("\t")
                handler.write(ccl_id)
                handler.write("\n")


def write_tla(tla, filename):
    """
    Write the `tla` table.
    """

    with open(filename, "w", encoding="utf-8") as handler:
        writer = csv.DictWriter(
            handler,
            delimiter="\t",
            fieldnames=["TLA__ID", "TLA__form", "TLA__meaning_en", "TLA__meaning_de"],
        )
        writer.writeheader()
        writer.writerows(tla)


def write_tla_match(tla_match, filename):
    """
    Write the `tla_match` table.
    """

    with open(filename, "w", encoding="utf-8") as handler:
        handler.write("entry_id\ttla_id\n")
        for entry_id, tla_ids in tla_match.items():
            for tla_id in tla_ids:
                handler.write(entry_id)
                handler.write("\t")
                handler.write(tla_id)
                handler.write("\n")


def write_vycichl(vycichl, filename):
    """
    Write the `vycichl` table.
    """

    # Flatten the Coptic dictionary
    for entry in vycichl:
        coptic = entry.pop("Coptic")
        coptic = {f"Coptic_{k}": v for k, v in coptic.items()}
        entry.update(coptic)

    with open(filename, "w", encoding="utf-8") as handler:
        writer = csv.DictWriter(
            handler,
            delimiter="\t",
            fieldnames=[
                "MATCH",
                "Root",
                "Reconstruction",
                "Gram_number",
                "Gram_gender",
                "Gram_form",
                "Meaning_fr",
                "Pages",
                "Degree_Certainty",
                "Relation_cpt__eg_forms",
                "Coptic_S",
                "Coptic_B",
                "Coptic_A",
                "Coptic_A2",
                "Coptic_P",
                "Coptic_F",
                "Coptic_F0",
                "Coptic_S0",
                "Coptic_O",
                "Coptic_B0",
                "Coptic_A0",
                "Coptic_M",
                "Coptic_L",
                "Coptic_G",
                "Coptic_B_Gr",
                "Coptic_Sf",
                "Coptic_H",
                "Coptic_A20",
                "Coptic_Hf",
            ],
        )
        writer.writeheader()
        writer.writerows(vycichl)


def write_osing(osing, filename):
    """
    Write the `osing` table.
    """

    # Flatten the Coptic dictionary
    for entry in osing:
        coptic = entry.pop("Coptic")
        coptic = {f"Coptic_{k}": v for k, v in coptic.items()}
        entry.update(coptic)

    with open(filename, "w", encoding="utf-8") as handler:
        writer = csv.DictWriter(
            handler,
            delimiter="\t",
            fieldnames=[
                "MATCH",
                "Form",
                "Root",
                "Nominal_class",
                "Meaning_de",
                "Pages",
                "Coptic_S",
                "Coptic_B",
                "Coptic_A",
                "Coptic_A2",
                "Coptic_Fs",
                "Coptic_F",
                "Coptic_M",
                "Coptic_Sf",
                "Coptic_O",
                "Coptic_H",
                "Coptic_Sa",
                "Coptic_V",
                "Coptic_ManiHPK",
                "Coptic_Mf",
                "Coptic_Sh",
                "Coptic_Bf",
                "Coptic_Copt_undefined",
            ],
        )
        writer.writeheader()
        writer.writerows(osing)


def write_matches(matches, filename):
    """
    Write the `matches` table.
    """

    with open(filename, "w", encoding="utf-8") as handler:
        writer = csv.DictWriter(
            handler,
            delimiter="\t",
            fieldnames=[
                "MATCH__ID",
                "MATCH__form",
                "MATCH__meaning_en",
                "MATCH__gram_number",
                "MATCH__gram_gender",
                "MATCH__pattern",
            ],
        )
        writer.writeheader()
        writer.writerows(matches)


def read_data(input_file):
    """
    Read data from the JSON source and return it as a structured pre-relational dict.
    """

    # Read file and parse data
    with open(input_file, encoding="utf-8") as handler:
        source_json = json.load(handler)

    # Parse entry by entry and update contents
    root, ccl, tla, matches = [], [], [], []
    ccl_match = defaultdict(list)
    tla_match = defaultdict(list)
    for entry, entry_value in source_json.items():
        # Parse entry data
        entry_root, entry_ccl, entry_tla, entry_matches = parse_entry(entry_value)

        # Extend table match_id -> ccl_id, cleaning the data in `ccl`
        for e_ccl in entry_ccl:
            for m in e_ccl["CCL__MATCH__ID"]:
                ccl_match[m].append(e_ccl["CCL__ID"])
            e_ccl.pop("CCL__MATCH__ID")

        # Extend table entry_id -> tla_match
        for tla_entry in entry_tla:
            tla_match[entry].append(tla_entry["TLA__ID"])

        # Extend collectors
        root.append(entry_root)
        ccl += entry_ccl
        tla += entry_tla
        matches += entry_matches

    # Extract Vycichl and Osing
    vycichl = []
    osing = []
    for m in matches:
        if "VYCICHL__1983" in m:
            v = m.pop("VYCICHL__1983")
            v["MATCH"] = m["MATCH__ID"]
            vycichl.append(v)
        if "OSING__1976" in m:
            o = m.pop("OSING__1976")
            o["MATCH"] = m["MATCH__ID"]
            osing.append(o)

    # Build tables for returning data
    return {
        "root": root,
        "ccl": ccl,
        "ccl_match": ccl_match,
        "tla": tla,
        "tla_match": tla_match,
        "vycichl": vycichl,
        "osing": osing,
        "matches": matches,
    }


def write_db(thotbank):
    """
    Write tables as individual tabular files.
    """

    db_root = BASE_PATH / "root.tsv"
    write_root(thotbank["root"], db_root)

    db_ccl = BASE_PATH / "ccl.tsv"
    write_ccl(thotbank["ccl"], db_ccl)

    db_ccl_match = BASE_PATH / "ccl_match.tsv"
    write_ccl_match(thotbank["ccl_match"], db_ccl_match)

    db_tla = BASE_PATH / "tla.tsv"
    write_tla(thotbank["tla"], db_tla)

    db_tla_match = BASE_PATH / "tla_match.tsv"
    write_tla_match(thotbank["tla_match"], db_tla_match)

    db_vycichl = BASE_PATH / "vycichl.tsv"
    write_vycichl(thotbank["vycichl"], db_vycichl)

    db_osing = BASE_PATH / "osing.tsv"
    write_osing(thotbank["osing"], db_osing)

    db_matches = BASE_PATH / "matches.tsv"
    write_matches(thotbank["matches"], db_matches)


def main():
    """
    Entry point for the script.
    """

    input_file = BASE_PATH / "Json_Database_25_3_2020_1.7.json"
    thotbank = read_data(input_file)
    write_db(thotbank)


if __name__ == "__main__":
    main()
