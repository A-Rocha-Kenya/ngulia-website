from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import subprocess
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import openpyxl
import xlrd


ROOT_DIR = Path(__file__).resolve().parent.parent
PIPELINE_ENV_PATH = ROOT_DIR / ".env.pipeline.local"
CURATED_DATA_DIR = ROOT_DIR / "data"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file(PIPELINE_ENV_PATH)

SOURCE_DATA_DIR = Path(os.getenv("NGULIA_SOURCE_DATA_DIR", str(ROOT_DIR.parent / "data"))).expanduser()

RINGING_PATH = SOURCE_DATA_DIR / "1991-2023 Ngulia Ringing Data MASTER.xlsx"
RECOVERIES_PATH = SOURCE_DATA_DIR / "Data - management and analysis" / "05 Recoveries" / "0709 Ngulia Recoveries and Controls.xls"
REFERENCES_PATH = CURATED_DATA_DIR / "references.bib"
PHOTOS_ROOT = SOURCE_DATA_DIR / "Ngulia_DJP" / "From DJP 2017" / "Selected birds"
OUTPUT_DIR = ROOT_DIR / "public" / "generated"
OUTPUT_PHOTOS_DIR = OUTPUT_DIR / "photos"
OUTPUT_SPECIES_RANGES_DIR = OUTPUT_DIR / "species-ranges"
TAXONOMY_CROSSWALK_PATH = CURATED_DATA_DIR / "ngulia_taxonomy_crosswalk.csv"
RECOVERY_SITE_COORDINATES_PATH = ROOT_DIR / "scripts" / "recovery_site_coordinates.json"
BOTW_GDB_PATH = SOURCE_DATA_DIR / "birdlife" / "BOTW.gdb"

NGULIA_COORDS = {"latitude": -3.0140288001023605, "longitude": 38.211134674309974}
NGULIA_EXCLUSION_BAND_KM = 500
KM_PER_LATITUDE_DEGREE = 111.32
MIGRATION_BOUNDS = {"west": -12.0, "south": -35.0, "east": 78.0, "north": 62.0}
MIGRATION_GRID = {"width": 90, "height": 96}
LAND_POLYGONS = [
    [(-18, 37), (-7, 36), (9, 37), (25, 33), (36, 31), (51, 13), (50, -7), (42, -35), (18, -35), (8, -18), (-6, -6), (-17, 14)],
    [(-12, 39), (6, 42), (16, 46), (30, 42), (42, 38), (55, 34), (78, 30), (78, 62), (-12, 62)],
    [(34, 12), (43, 12), (56, 17), (58, 25), (48, 31), (39, 29), (34, 20)],
    [(57, 5), (78, 6), (78, 31), (61, 31), (55, 24), (58, 14)],
    [(43, -26), (51, -26), (51, -12), (46, -11), (43, -17)],
]
WATER_HOLES = [
    [(-6, 31), (35, 31), (35, 39), (-6, 39)],
    [(27, 40), (42, 40), (42, 48), (27, 48)],
    [(47, 36), (55, 36), (55, 48), (47, 48)],
    [(32, 11), (44, 11), (44, 30), (32, 30)],
    [(47, 24), (57, 24), (57, 31), (47, 31)],
    [(39, -35), (53, -35), (53, 5), (46, 5), (43, -10), (41, -18)],
]

PHOTO_DIRECTORY_ALIASES = {
    "marsh warbler": "Marsh Warbler",
    "thrush nightingale": "Sprosser",
    "common whitethroat": "Whitethroat",
    "barn swallow": "Swallow",
    "river warbler": "River Warbler",
    "irania": "Irania & others",
    "red-backed shrike": "Red-backed Shrike",
    "willow warbler": "Other Warblers",
    "spotted flycatcher": "Afros",
    "common nightingale": "Nightingale",
    "isabelline shrike": "Isabelline Shrike",
    "olive-tree warbler": "Olive-tree Warbler",
    "barred warbler": "Barred Warbler",
    "basra reed warbler": "Basra Reed Warbler",
    "garden warbler": "Other Warblers",
    "upcher's warbler": "Upcher's Warbler",
    "eurasian roller": "Afros",
    "little bittern": "Afros",
}

SPECIES_RANGE_SIMPLIFY_DEGREES = 0.12
SPECIES_RANGE_COORDINATE_PRECISION = 4

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def normalize(value: object) -> str:
    text = str(value or "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).strip().lower()
    return text


SPECIES_RANGE_SEASONAL_TYPES = {
    2: "breeding",
    3: "wintering",
}

def override_key(site: object, province: object, country: object) -> str:
    return f"{normalize(site)}|{normalize(province)}|{normalize(country)}"


def load_recovery_site_coordinates(path: Path) -> dict[str, dict[str, float | str]]:
    if not path.exists():
        raise RuntimeError(f"Missing recovery site coordinates file: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload.get("overrides", payload) if isinstance(payload, dict) else {}
    if not isinstance(raw, dict):
        raise RuntimeError(f"Invalid recovery site coordinates payload in {path}")

    coordinates: dict[str, dict[str, float | str]] = {}
    for key, value in raw.items():
        if not isinstance(value, dict):
            continue
        latitude = value.get("latitude")
        longitude = value.get("longitude")
        if latitude is None or longitude is None:
            continue
        try:
            lat = float(latitude)
            lon = float(longitude)
        except (TypeError, ValueError):
            continue

        coordinates[key] = {
            "latitude": lat,
            "longitude": lon,
            "source": str(value.get("source") or "recovery-site-coordinates"),
        }

    return coordinates


RECOVERY_SITE_COORDINATES = load_recovery_site_coordinates(RECOVERY_SITE_COORDINATES_PATH)


def write_json(filename: str, data: object) -> None:
    (OUTPUT_DIR / filename).write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_json_compact(filename: str, data: object) -> None:
    (OUTPUT_DIR / filename).write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")


def pick_number(value: object) -> int | float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
      if isinstance(value, float) and math.isnan(value):
        return None
      return value
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or "").replace(",", ""))
    if not match:
        return None
    num = float(match.group(0))
    return int(num) if num.is_integer() else num


def excel_serial_to_iso(value: object) -> str | None:
    if isinstance(value, (int, float)) and value > 25000:
        base = datetime(1899, 12, 30)
        return (base + timedelta(days=float(value))).date().isoformat()
    return None


def string_date_to_iso(value: object) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None

    match = re.match(r"^(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{2,4})$", text)
    if match:
        day, month, year = match.groups()
        if len(year) == 2:
            year_int = int(year)
            year = f"{1900 + year_int}" if year_int >= 70 else f"{2000 + year_int}"
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", text)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    match = re.match(r"^(\d{4})$", text)
    if match:
        return f"{match.group(1)}-01-01"

    return None


def parse_date(primary: object, fallback: object) -> str | None:
    return excel_serial_to_iso(primary) or string_date_to_iso(fallback)


def parse_year(primary: object, fallback: object) -> int | None:
    iso = parse_date(primary, fallback)
    return int(iso[:4]) if iso else None


def day_of_year(iso_date: str) -> int:
    current = datetime.fromisoformat(iso_date)
    start = datetime(current.year, 1, 1)
    return (current - start).days + 1


def format_month_day(iso_date: str) -> str:
    return iso_date[5:]


def update_phenology(store: dict[int, dict[str, object]], doy: int, label: str, year: int) -> None:
    current = store.get(doy, {"dayOfYear": doy, "label": label, "count": 0, "yearsSet": set()})
    current["count"] += 1
    current["yearsSet"].add(year)
    store[doy] = current


def serialize_phenology(store: dict[int, dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "dayOfYear": value["dayOfYear"],
            "label": value["label"],
            "count": value["count"],
            "effortYears": len(value["yearsSet"]),
        }
        for _, value in sorted(store.items())
    ]


def clean_text(value: object) -> str:
    return str(value or "").strip()


def clean_header(value: object) -> str:
    return clean_text(value).lstrip("\ufeff")


def sanitize_method(value: object) -> str:
    text = clean_text(value)
    if not text:
        return ""
    normalized = normalize(text)
    if (
        normalized == "?"
        or normalized.startswith("controlled")
        or normalized.startswith("found")
        or normalized.startswith("record")
        or normalized.startswith("caught")
    ):
        return ""
    return text


def parse_location(lat_raw: object, lon_raw: object, country_raw: object, site_raw: object = "", province_raw: object = "") -> dict[str, object]:
    key = override_key(site_raw, province_raw, country_raw)
    override = RECOVERY_SITE_COORDINATES.get(key)
    if not override:
        raise RuntimeError(
            "Missing recovery site coordinates for "
            f"site={clean_text(site_raw)!r}, province={clean_text(province_raw)!r}, country={clean_text(country_raw)!r} "
            f"(key: {key}). Add it to {RECOVERY_SITE_COORDINATES_PATH}."
        )

    latitude = override.get("latitude")
    longitude = override.get("longitude")
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        raise RuntimeError(
            f"Invalid recovery site coordinates for key {key} in {RECOVERY_SITE_COORDINATES_PATH}."
        )

    return {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "source": str(override.get("source") or "recovery-site-coordinates"),
    }


def parse_bool_field(value: object, field_name: str, row_label: str) -> bool:
    text = clean_text(value).upper()
    if text in {"TRUE", "T", "1", "YES"}:
        return True
    if text in {"FALSE", "F", "0", "NO"}:
        return False
    raise RuntimeError(f"Invalid boolean {value!r} for {field_name} in taxonomy row {row_label!r}.")


def unique_non_empty(values: list[str]) -> list[str]:
    seen = set()
    items = []
    for value in values:
        text = clean_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        items.append(text)
    return items


def split_crosswalk_ids(value: object) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    return unique_non_empty(re.split(r"\s*;\s*", text))


def build_species_links(avibase_id: str, cornell_species_code: str, birdlife_id: str, kbt_seq: str, abap_ids: list[str]) -> dict[str, object]:
    avibase_short_id = avibase_id.removeprefix("avibase-")
    return {
        "birdsOfTheWorld": f"https://birdsoftheworld.org/bow/species/{cornell_species_code}" if cornell_species_code else "",
        "eBird": f"https://ebird.org/species/{cornell_species_code}" if cornell_species_code else "",
        "birdLifeFactsheet": f"https://datazone.birdlife.org/species/factsheet/{birdlife_id}" if birdlife_id else "",
        "kenyaBirdTrends": f"https://kenyabirdtrends.co.ke/?mode=Species&species={kbt_seq}" if kbt_seq else "",
        "avibase": f"https://avibase.bsc-eoc.org/species.jsp?avibaseid={avibase_short_id}" if avibase_short_id else "",
        "kbm": [{"id": species_id, "url": f"https://kenya.birdmap.africa/species/{species_id}"} for species_id in abap_ids],
        "safring": [{"id": species_id, "url": f"https://safring.ringing.africa/species/{species_id}"} for species_id in abap_ids],
    }


def load_taxonomy_crosswalk(path: Path) -> dict[str, object]:
    if not path.exists():
        raise RuntimeError(f"Missing taxonomy crosswalk file: {path}")

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames:
            reader.fieldnames = [clean_header(name) for name in reader.fieldnames]
        rows = list(reader)
        headers = reader.fieldnames or []

    required_columns = {
        "raw_label",
        "ngulia_english",
        "ngulia_latin",
        "latin_abbreviation",
        "ngulia_abbreviation",
        "avilist_scientific_name",
        "avilist_english_name",
        "birdlife_id",
        "avibase_id",
        "include_processing",
        "include_recovery",
    }
    missing_columns = sorted(required_columns - set(headers))
    if missing_columns:
        raise RuntimeError(f"Missing required taxonomy columns in {path}: {', '.join(missing_columns)}")

    parsed_rows: list[dict[str, object]] = []
    rows_by_raw_label: dict[str, dict[str, object]] = {}
    rows_by_code: dict[str, dict[str, object]] = {}
    rows_by_avibase: dict[str, list[dict[str, object]]] = defaultdict(list)
    errors: list[str] = []

    for row in rows:
        raw_label = clean_text(row.get("raw_label"))
        if not raw_label:
            errors.append("Encountered taxonomy row with blank raw_label.")
            continue

        include_processing = parse_bool_field(row.get("include_processing"), "include_processing", raw_label)
        include_recovery = parse_bool_field(row.get("include_recovery"), "include_recovery", raw_label)

        parsed = {
            clean_header(key): clean_text(value)
            for key, value in row.items()
        }
        parsed["include_processing"] = include_processing
        parsed["include_recovery"] = include_recovery

        if raw_label in rows_by_raw_label:
            errors.append(f"Duplicate raw_label in taxonomy crosswalk: {raw_label!r}")
            continue
        rows_by_raw_label[raw_label] = parsed

        latin_abbreviation = parsed["latin_abbreviation"]
        if latin_abbreviation:
            existing = rows_by_code.get(latin_abbreviation)
            if existing and existing["avibase_id"] != parsed["avibase_id"]:
                errors.append(
                    f"Duplicate latin_abbreviation mapped to different avibase_id values: {latin_abbreviation!r}"
                )
            elif not existing:
                rows_by_code[latin_abbreviation] = parsed

        if include_recovery and not include_processing:
            errors.append(f"Taxonomy row {raw_label!r} has include_recovery=TRUE but include_processing=FALSE.")

        if include_processing or include_recovery:
            if not parsed["avibase_id"]:
                errors.append(f"Taxonomy row {raw_label!r} is included but has blank avibase_id.")
            if not parsed["avilist_english_name"]:
                errors.append(f"Taxonomy row {raw_label!r} is included but has blank avilist_english_name.")
            if not parsed["avilist_scientific_name"]:
                errors.append(f"Taxonomy row {raw_label!r} is included but has blank avilist_scientific_name.")
        if include_recovery and not parsed["birdlife_id"]:
            errors.append(f"Taxonomy row {raw_label!r} has include_recovery=TRUE but blank birdlife_id.")

        if parsed["avibase_id"]:
            rows_by_avibase[parsed["avibase_id"]].append(parsed)
        parsed_rows.append(parsed)

    species_by_id: dict[str, dict[str, object]] = {}
    for avibase_id, grouped_rows in sorted(rows_by_avibase.items()):
        included_rows = [row for row in grouped_rows if row["include_processing"]]
        if not included_rows:
            continue

        display_names = unique_non_empty([row["avilist_english_name"] for row in included_rows])
        scientific_names = unique_non_empty([row["avilist_scientific_name"] for row in included_rows])
        birdlife_ids = unique_non_empty([row["birdlife_id"] for row in included_rows])
        cornell_species_codes = unique_non_empty([row["cornell_species_code"] for row in included_rows])
        kbt_seqs = unique_non_empty([row["kbt_seq"] for row in included_rows])
        abap_ids = unique_non_empty(
            [species_id for row in included_rows for species_id in split_crosswalk_ids(row["abap_ids"])]
        )
        latin_abbreviations = unique_non_empty([row["latin_abbreviation"] for row in included_rows])
        ngulia_abbreviations = unique_non_empty([row["ngulia_abbreviation"] for row in included_rows])

        if len(display_names) != 1:
            errors.append(f"Avibase group {avibase_id!r} has inconsistent avilist_english_name values.")
            continue
        if len(scientific_names) != 1:
            errors.append(f"Avibase group {avibase_id!r} has inconsistent avilist_scientific_name values.")
            continue
        if len(birdlife_ids) > 1:
            errors.append(f"Avibase group {avibase_id!r} has inconsistent birdlife_id values.")
            continue
        if len(cornell_species_codes) > 1:
            errors.append(f"Avibase group {avibase_id!r} has inconsistent cornell_species_code values.")
            continue
        if len(kbt_seqs) > 1:
            errors.append(f"Avibase group {avibase_id!r} has inconsistent kbt_seq values.")
            continue

        species_by_id[avibase_id] = {
            "id": avibase_id,
            "name": display_names[0],
            "latin": scientific_names[0],
            "code": latin_abbreviations[0] if len(latin_abbreviations) == 1 else "; ".join(latin_abbreviations),
            "nguliaCode": ngulia_abbreviations[0] if len(ngulia_abbreviations) == 1 else "; ".join(ngulia_abbreviations),
            "birdlifeId": birdlife_ids[0] if birdlife_ids else "",
            "cornellSpeciesCode": cornell_species_codes[0] if cornell_species_codes else "",
            "kbtSeq": kbt_seqs[0] if kbt_seqs else "",
            "abapIds": abap_ids,
            "includeRecovery": any(row["include_recovery"] for row in included_rows),
            "rawLabels": [row["raw_label"] for row in included_rows],
            "photoLabels": unique_non_empty(
                [
                    *(row["raw_label"] for row in included_rows),
                    *(row["ngulia_english"] for row in included_rows),
                    *(row["avilist_english_name"] for row in included_rows),
                ]
            ),
            "links": build_species_links(
                avibase_id,
                cornell_species_codes[0] if cornell_species_codes else "",
                birdlife_ids[0] if birdlife_ids else "",
                kbt_seqs[0] if kbt_seqs else "",
                abap_ids,
            ),
        }

    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise RuntimeError(f"Invalid taxonomy crosswalk at {path}:\n{joined}")

    return {
        "rows": parsed_rows,
        "rows_by_raw_label": rows_by_raw_label,
        "rows_by_code": rows_by_code,
        "species_by_id": species_by_id,
    }


def publication_embed_url(url: str) -> str:
    params = "rel=0&modestbranding=1&controls=0&iv_load_policy=3"
    if "youtu.be/" in url:
        video_id = url.rstrip("/").split("/")[-1].split("?")[0]
        return f"https://www.youtube-nocookie.com/embed/{video_id}?{params}"

    match = re.search(r"(?:youtube\.com/watch\?v=|youtube\.com/embed/)([^&?/]+)", url)
    return f"https://www.youtube-nocookie.com/embed/{match.group(1)}?{params}" if match else ""


def publication_is_open_access(url: str) -> bool:
    if not url:
        return False

    url_lower = url.lower()
    return url_lower.endswith(".pdf") or any(host in url_lower for host in ["ajol.info", "ringing.africa", "researchgate.net"])


def parse_reference_entries(text: str) -> list[dict[str, str | bool]]:
    matches = re.findall(r"@(\w+)\{([^,]+),([\s\S]*?)\n\}", text)
    entries = []
    seen = set()

    for entry_type, key, body in matches:
        def field(name: str) -> str:
            match = re.search(rf"{name}\s*=\s*\{{([\s\S]*?)\}}", body, re.I)
            return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""

        url = field("url")
        doi = field("doi")

        entry = {
            "entryType": entry_type,
            "key": key,
            "title": field("title"),
            "authors": field("author"),
            "journal": field("journal"),
            "year": field("year"),
            "volume": field("volume"),
            "issue": field("issue"),
            "pages": field("pages"),
            "url": url,
            "doi": doi,
            "abstract": field("abstract"),
            "isPdf": url.lower().endswith(".pdf"),
            "openAccess": publication_is_open_access(url),
        }
        if not entry["title"]:
            continue

        identifier = f"{entry['title']}|{entry['year']}"
        if identifier in seen:
            continue
        seen.add(identifier)
        entries.append(entry)

    entries.sort(key=lambda item: int(item["year"] or 0), reverse=True)
    return entries


def walk_image_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    files = []
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            files.append(path)
    return sorted(files)


def find_photo_for_species(species_name: str) -> Path | None:
    alias = PHOTO_DIRECTORY_ALIASES.get(normalize(species_name))
    if not alias:
        return None
    files = walk_image_files(PHOTOS_ROOT / alias)
    return files[0] if files else None


def copy_photo_for_species_candidates(species_labels: list[str], species_id: str) -> str | None:
    source_path = None
    for label in species_labels:
        source_path = find_photo_for_species(label)
        if source_path:
            break
    if not source_path:
        return None

    target_name = f"{species_id}{source_path.suffix.lower()}"
    target_path = OUTPUT_PHOTOS_DIR / target_name
    shutil.copyfile(source_path, target_path)
    return f"./generated/photos/{target_name}"


def build_ringing_data(taxonomy: dict[str, object]) -> tuple[list[dict[str, object]], dict[str, object]]:
    workbook = openpyxl.load_workbook(RINGING_PATH, read_only=True, data_only=True)
    ring_sheet = workbook["RingData"]
    ring_rows = list(ring_sheet.iter_rows(values_only=True))
    ring_headers = [str(item or "") for item in ring_rows[0]]

    yearly: dict[int, dict[str, object]] = {}
    phenology: dict[int, dict[str, object]] = {}
    species_map: dict[str, dict[str, object]] = {}
    total_birds = 0

    for row in ring_rows[1:]:
        record = dict(zip(ring_headers, row))
        raw_label = clean_text(record.get("Name"))
        if not raw_label:
            continue

        taxonomy_row = taxonomy["rows_by_raw_label"].get(raw_label)
        if not taxonomy_row:
            raise RuntimeError(
                f"Missing taxonomy row for RingData.Name {raw_label!r} in {TAXONOMY_CROSSWALK_PATH}."
            )
        if not taxonomy_row["include_processing"]:
            continue

        species_id = taxonomy_row["avibase_id"]
        species_meta = taxonomy["species_by_id"].get(species_id)
        if not species_meta:
            raise RuntimeError(f"Missing grouped taxonomy metadata for avibase_id {species_id!r}.")

        year = parse_year(record.get("Date_Full"), record.get("Date"))
        if not year or year < 1991 or year > 2023:
            continue

        iso_date = parse_date(record.get("Date_Full"), record.get("Date"))
        total_birds += 1

        if year not in yearly:
            yearly[year] = {"year": year, "totalRings": 0, "speciesSet": set()}
        yearly[year]["totalRings"] += 1
        yearly[year]["speciesSet"].add(species_id)

        if species_id not in species_map:
            species_map[species_id] = {
                "id": species_meta["id"],
                "name": species_meta["name"],
                "latin": species_meta["latin"],
                "code": species_meta["code"],
                "nguliaCode": species_meta["nguliaCode"],
                "birdlifeId": species_meta["birdlifeId"],
                "cornellSpeciesCode": species_meta["cornellSpeciesCode"],
                "kbtSeq": species_meta["kbtSeq"],
                "abapIds": list(species_meta["abapIds"]),
                "includeRecovery": species_meta["includeRecovery"],
                "rawLabels": list(species_meta["rawLabels"]),
                "photoLabels": list(species_meta["photoLabels"]),
                "links": species_meta["links"],
                "total": 0,
                "annual": defaultdict(int),
                "phenology": {},
                "photo": None,
            }

        species = species_map[species_id]
        species["total"] += 1
        species["annual"][year] += 1

        if iso_date:
            doy = day_of_year(iso_date)
            label = format_month_day(iso_date)
            update_phenology(species["phenology"], doy, label, year)
            update_phenology(phenology, doy, label, year)

    species_list = []
    for species in sorted(species_map.values(), key=lambda item: item["total"], reverse=True):
        species_list.append(
            {
                **species,
                "photo": copy_photo_for_species_candidates(species["photoLabels"], species["id"]),
                "annual": [{"year": year, "count": count} for year, count in sorted(species["annual"].items())],
                "phenology": serialize_phenology(species["phenology"]),
            }
        )

    yearly_series = [
        {"year": entry["year"], "totalRings": entry["totalRings"], "totalSpecies": len(entry["speciesSet"])}
        for _, entry in sorted(yearly.items())
    ]
    years = [item["year"] for item in yearly_series]

    dashboard = {
        "summary": {
            "totalBirds": total_birds,
            "totalSpecies": len(species_list),
            "yearStart": years[0],
            "yearEnd": years[-1],
        },
        "yearly": yearly_series,
        "phenology": serialize_phenology(phenology),
        "topSpecies": [
            {
                "id": species["id"],
                "name": species["name"],
                "latin": species["latin"],
                "code": species["code"],
                "links": species["links"],
                "total": species["total"],
                "photo": species["photo"],
            }
            for species in species_list[:15]
        ],
        "speciesExplorer": species_list,
    }

    return species_list, dashboard


def build_recoveries(taxonomy: dict[str, object]) -> dict[str, object]:
    workbook = xlrd.open_workbook(RECOVERIES_PATH)
    sheet = workbook.sheet_by_index(0)
    rows = [sheet.row_values(i) for i in range(sheet.nrows)]
    recoveries = []
    section_status = ""

    for row in rows:
        section_label = normalize(row[0])
        if section_label == "ringed at ngulia":
            section_status = "ringed"
            continue
        if section_label == "controlled at ngulia":
            section_status = "controlled"
            continue

        code = clean_text(row[0])
        if code == "SPECIES" or not re.match(r"^[A-Z]{5,7}$", code):
            continue

        taxonomy_row = taxonomy["rows_by_code"].get(code)
        if not taxonomy_row:
            raise RuntimeError(
                f"Missing taxonomy row for recovery species code {code!r} in {TAXONOMY_CROSSWALK_PATH}."
            )
        if not taxonomy_row["include_recovery"]:
            continue

        species_id = taxonomy_row["avibase_id"]
        species_meta = taxonomy["species_by_id"].get(species_id)
        if not species_meta:
            raise RuntimeError(f"Missing grouped taxonomy metadata for avibase_id {species_id!r}.")

        species_name = species_meta["name"]
        ring_site = clean_text(row[4])
        recover_site = clean_text(row[15])

        inferred_status = section_status
        if not inferred_status:
            ring_is_ngulia = "ngulia" in normalize(ring_site)
            recover_is_ngulia = "ngulia" in normalize(recover_site)
            if ring_is_ngulia and not recover_is_ngulia:
                inferred_status = "ringed"
            elif recover_is_ngulia and not ring_is_ngulia:
                inferred_status = "controlled"
            else:
                inferred_status = "ringed"

        if inferred_status == "ringed":
            location_site = clean_text(row[15])
            location_province = clean_text(row[16])
            location_country = clean_text(row[17])
            coords = parse_location(row[18], row[19], location_country, location_site, location_province)
        else:
            location_site = clean_text(row[4])
            location_province = clean_text(row[5])
            location_country = clean_text(row[6])
            coords = parse_location(row[7], row[8], location_country, location_site, location_province)

        recoveries.append(
            {
                "id": f"recovery-{len(recoveries) + 1}",
                "status": inferred_status,
                "speciesId": species_id,
                "speciesCode": code,
                "speciesName": species_name,
                "speciesLatin": species_meta["latin"],
                "ringDate": string_date_to_iso(row[3]) or clean_text(row[3]),
                "ringSite": ring_site,
                "ringProvince": clean_text(row[5]),
                "ringCountry": clean_text(row[6]),
                "method": sanitize_method(row[13]),
                "recoverDate": string_date_to_iso(row[14]) or clean_text(row[14]),
                "recoverySite": recover_site,
                "recoveryProvince": clean_text(row[16]),
                "recoveryCountry": clean_text(row[17]),
                "recoverSite": location_site,
                "recoverProvince": location_province,
                "recoverCountry": location_country,
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "coordinateSource": coords["source"],
                "durationDays": pick_number(row[24]),
                "distanceKm": pick_number(row[25]),
            }
        )

    countries = sorted({row["recoverCountry"] for row in recoveries if row["recoverCountry"]})
    farthest = max(recoveries, key=lambda row: row["distanceKm"] or 0, default=None)

    by_species: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in recoveries:
        by_species[row["speciesId"]].append(row)

    return {
        "summary": {
            "totalRecoveries": len(recoveries),
            "totalCountries": len(countries),
            "countries": countries,
            "farthestRecovery": {
                "speciesName": farthest["speciesName"],
                "country": farthest["recoverCountry"],
                "distanceKm": farthest["distanceKm"],
            }
            if farthest
            else None,
        },
        "items": recoveries,
        "bySpeciesId": {species_id: by_species[species_id] for species_id in sorted(by_species)},
    }


def load_species_range_checklist_by_id() -> dict[str, dict[str, str]]:
    if not BOTW_GDB_PATH.exists():
        return {}

    try:
        result = subprocess.run(
            [
                "ogr2ogr",
                "-f",
                "CSV",
                "/vsistdout/",
                str(BOTW_GDB_PATH),
                "Checklist_v8_txt",
                "-select",
                "SISID,CommonName,ScientificName",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("ogr2ogr is required to build BirdLife species ranges.") from exc

    by_id: dict[str, dict[str, str]] = {}
    for row in csv.DictReader(result.stdout.splitlines()):
        birdlife_id = clean_text(row.get("SISID"))
        if not birdlife_id:
            continue
        by_id[birdlife_id] = {
            "birdlifeId": birdlife_id,
            "commonName": clean_text(row.get("CommonName")),
            "scientificName": clean_text(row.get("ScientificName")),
        }

    return by_id


def export_species_range_features(birdlife_ids: list[str]) -> dict[str, list[dict[str, object]]]:
    if not birdlife_ids or not BOTW_GDB_PATH.exists():
        return {}

    temp_path = Path("/tmp/ngulia-species-ranges.geojson")
    if temp_path.exists():
        temp_path.unlink()

    sql_ids = ", ".join(str(int(birdlife_id)) for birdlife_id in birdlife_ids)
    sql = (
        "SELECT sisid, sci_name, seasonal "
        "FROM All_Species "
        f"WHERE seasonal IN (2,3) AND sisid IN ({sql_ids})"
    )

    try:
        subprocess.run(
            [
                "ogr2ogr",
                "--config",
                "OGR_ORGANIZE_POLYGONS",
                "ONLY_CCW",
                "-f",
                "GeoJSON",
                str(temp_path),
                str(BOTW_GDB_PATH),
                "-dialect",
                "OGRSQL",
                "-sql",
                sql,
                "-simplify",
                str(SPECIES_RANGE_SIMPLIFY_DEGREES),
                "-lco",
                f"COORDINATE_PRECISION={SPECIES_RANGE_COORDINATE_PRECISION}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("ogr2ogr is required to build BirdLife species ranges.") from exc

    payload = json.loads(temp_path.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)

    for feature in payload.get("features", []):
        properties = feature.get("properties") or {}
        birdlife_id = clean_text(properties.get("sisid"))
        scientific_name = clean_text(properties.get("sci_name"))
        seasonal_code = properties.get("seasonal")
        range_type = SPECIES_RANGE_SEASONAL_TYPES.get(seasonal_code)
        if not birdlife_id or not scientific_name or not range_type:
            continue

        grouped[birdlife_id].append(
            {
                "type": "Feature",
                "properties": {
                    "birdlifeId": birdlife_id,
                    "scientificName": scientific_name,
                    "rangeType": range_type,
                },
                "geometry": feature.get("geometry"),
            }
        )

    return grouped


def build_species_ranges(species_list: list[dict[str, object]]) -> dict[str, object]:
    if OUTPUT_SPECIES_RANGES_DIR.exists():
        shutil.rmtree(OUTPUT_SPECIES_RANGES_DIR)
    ensure_dir(OUTPUT_SPECIES_RANGES_DIR)

    checklist_by_id = load_species_range_checklist_by_id()
    index_by_id: dict[str, dict[str, object]] = {}
    matched_species: list[dict[str, object]] = []

    for species in species_list:
        species_id = str(species["id"])
        index_entry: dict[str, object] = {
            "id": species_id,
            "name": species["name"],
            "latin": species.get("latin", ""),
            "birdlifeId": species.get("birdlifeId", ""),
            "available": False,
        }
        index_by_id[species_id] = index_entry

        if not species.get("includeRecovery"):
            index_entry["missingReason"] = "not-included-in-recovery"
            continue

        birdlife_id = clean_text(species.get("birdlifeId"))
        checklist_match = checklist_by_id.get(birdlife_id)
        if not checklist_match:
            raise RuntimeError(
                f"Missing BirdLife checklist match for avibase_id {species_id!r} "
                f"(species {species['name']!r}, birdlife_id {birdlife_id!r})."
            )

        matched_species.append(
            {
                "id": species_id,
                "name": species["name"],
                "latin": species.get("latin", ""),
                "birdlifeId": birdlife_id,
                "birdlifeScientificName": checklist_match["scientificName"],
                "birdlifeCommonName": checklist_match["commonName"],
            }
        )
        index_entry.update(
            {
                "birdlifeScientificName": checklist_match["scientificName"],
                "birdlifeCommonName": checklist_match["commonName"],
            }
        )

    features_by_birdlife_id = export_species_range_features(sorted({species["birdlifeId"] for species in matched_species}))
    available_species = 0

    for species in matched_species:
        features = features_by_birdlife_id.get(species["birdlifeId"], [])
        if not features:
            raise RuntimeError(
                f"No BirdLife breeding/wintering range for avibase_id {species['id']!r} "
                f"(species {species['name']!r}, birdlife_id {species['birdlifeId']!r})."
            )

        range_types = sorted({feature["properties"]["rangeType"] for feature in features})
        payload = {
            "type": "FeatureCollection",
            "features": [
                {
                    **feature,
                    "properties": {
                        **feature["properties"],
                        "speciesId": species["id"],
                        "speciesName": species["name"],
                        "speciesLatin": species["latin"],
                    },
                }
                for feature in features
            ],
        }
        write_json_compact(f"species-ranges/{species['id']}.geojson", payload)

        index_by_id[species["id"]].update(
            {
                "available": True,
                "path": f"species-ranges/{species['id']}.geojson",
                "rangeTypes": range_types,
                "featureCount": len(features),
            }
        )
        available_species += 1

    return {
        "metadata": {
            "source": "BirdLife International and Handbook of the Birds of the World",
            "crs": "EPSG:4326",
            "simplifyDegrees": SPECIES_RANGE_SIMPLIFY_DEGREES,
            "seasonalTypes": SPECIES_RANGE_SEASONAL_TYPES,
        },
        "summary": {
            "totalSpecies": len(species_list),
            "matchedSpecies": len(matched_species),
            "availableSpecies": available_species,
        },
        "species": index_by_id,
    }


def species_group(species_name: object) -> str:
    name = normalize(species_name)
    if "warbler" in name or "whitethroat" in name:
        return "warblers"
    if "nightingale" in name or "irania" in name:
        return "nightingales"
    if "swallow" in name or "roller" in name or "nightjar" in name:
        return "aerial migrants"
    return "other migrants"


def recovery_season(value: object) -> str:
    text = str(value or "")
    match = re.match(r"^\d{4}-(\d{2})-\d{2}$", text)
    if not match:
        return "undated"
    month = int(match.group(1))
    if month in {3, 4, 5, 6}:
        return "spring recoveries"
    if month in {8, 9, 10, 11, 12}:
        return "autumn recoveries"
    return "other seasons"


def point_in_polygon(lng: float, lat: float, polygon: list[tuple[float, float]]) -> bool:
    inside = False
    j = len(polygon) - 1
    for i, point in enumerate(polygon):
        xi, yi = point
        xj, yj = polygon[j]
        if ((yi > lat) != (yj > lat)) and (lng < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def is_land(lng: float, lat: float) -> bool:
    return any(point_in_polygon(lng, lat, polygon) for polygon in LAND_POLYGONS) and not any(point_in_polygon(lng, lat, polygon) for polygon in WATER_HOLES)


def grid_centers() -> list[dict[str, float | int | bool]]:
    bounds = MIGRATION_BOUNDS
    width = MIGRATION_GRID["width"]
    height = MIGRATION_GRID["height"]
    dx = (bounds["east"] - bounds["west"]) / width
    dy = (bounds["north"] - bounds["south"]) / height

    return [
        {
            "index": y * width + x,
            "longitude": bounds["west"] + (x + 0.5) * dx,
            "latitude": bounds["south"] + (y + 0.5) * dy,
            "land": is_land(bounds["west"] + (x + 0.5) * dx, bounds["south"] + (y + 0.5) * dy),
        }
        for y in range(height)
        for x in range(width)
    ]


def normalize_surface(values: list[float]) -> list[float]:
    total = sum(values)
    if total <= 0:
        return [0 for _ in values]
    return [round(value / total, 9) for value in values]


def gaussian_surface(points: list[dict[str, float]], cells: list[dict[str, float | int | bool]], sigma_lng: float, sigma_lat: float, min_lat: float | None = None, max_lat: float | None = None) -> list[float]:
    values = []

    for cell in cells:
        if not cell["land"] or (min_lat is not None and cell["latitude"] <= min_lat) or (max_lat is not None and cell["latitude"] > max_lat):
            values.append(0)
            continue

        density = 0.0
        for point in points:
            density += math.exp(-0.5 * (((cell["longitude"] - point["longitude"]) / sigma_lng) ** 2 + ((cell["latitude"] - point["latitude"]) / sigma_lat) ** 2))
        values.append(density)

    return normalize_surface(values)


def corridor_surface(cells: list[dict[str, float | int | bool]]) -> list[float]:
    values = []

    for cell in cells:
        if not cell["land"]:
            values.append(0)
            continue

        corridor_lng = NGULIA_COORDS["longitude"] + 0.12 * (cell["latitude"] - NGULIA_COORDS["latitude"])
        lateral = math.exp(-0.5 * ((cell["longitude"] - corridor_lng) / 8.5) ** 2)
        north_south = 0.35 + 0.65 * math.exp(-0.5 * ((cell["longitude"] - NGULIA_COORDS["longitude"]) / 18.0) ** 2)
        values.append(lateral * north_south)

    return normalize_surface(values)


def recovery_points(items: list[dict[str, object]]) -> list[dict[str, float]]:
    return [{"latitude": item["latitude"], "longitude": item["longitude"]} for item in items if is_land(item["longitude"], item["latitude"])]


def outside_ngulia_latitude_band(item: dict[str, object]) -> bool:
    latitude_band = NGULIA_EXCLUSION_BAND_KM / KM_PER_LATITUDE_DEGREE
    return abs(item["latitude"] - NGULIA_COORDS["latitude"]) > latitude_band


def landing_cell_is_land(cell: dict[str, float | int | bool]) -> bool:
    if not cell["land"]:
        return False

    # Use a stricter east-coast cutoff for southern arrival cells so the coarse
    # prototype mask cannot place endpoints over the Indian Ocean.
    if cell["latitude"] < NGULIA_COORDS["latitude"] and cell["longitude"] > 37.5:
        return False

    return True


def build_migration_probabilities(recoveries: dict[str, object]) -> dict[str, object]:
    cells = grid_centers()
    landing_cells = [{**cell, "land": landing_cell_is_land(cell)} for cell in cells]
    items = [
        item
        for item in recoveries["items"]
        if item["coordinateSource"] != "unknown" and -35 <= item["latitude"] <= 62 and -12 <= item["longitude"] <= 78
    ]
    northern_items = [item for item in items if item["latitude"] > NGULIA_COORDS["latitude"] and outside_ngulia_latitude_band(item)]
    southern_items = [item for item in items if item["latitude"] < NGULIA_COORDS["latitude"] and outside_ngulia_latitude_band(item)]
    fallback_departure_points = recovery_points(northern_items) or [{"latitude": 42.0, "longitude": 42.0}]
    fallback_landing_points = recovery_points(southern_items) or [{"latitude": -15.0, "longitude": 35.0}]

    return {
        "metadata": {
            "description": "Browser-sampled migration probability grids for the Ngulia home-page deck.gl prototype.",
            "crs": "EPSG:4326",
            "site": {"name": "Ngulia", "latitude": NGULIA_COORDS["latitude"], "longitude": NGULIA_COORDS["longitude"]},
            "normalization": "Each values array sums to one and can be sampled as a discrete probability distribution.",
            "source": "Departure densities are smoothed from recoveries north of Ngulia; landing densities are smoothed from recoveries south of Ngulia.",
            "landMask": "Coarse in-script land polygons with broad water holes for rapid prototype iteration.",
            "exclusionBandKm": NGULIA_EXCLUSION_BAND_KM,
        },
        "bounds": MIGRATION_BOUNDS,
        "grid": MIGRATION_GRID,
        "landMask": [cell["land"] for cell in cells],
        "departure": {
            "label": "Northern departure probability",
            "recordCount": len(northern_items),
            "values": gaussian_surface(fallback_departure_points, cells, sigma_lng=5.2, sigma_lat=4.5, min_lat=NGULIA_COORDS["latitude"]),
        },
        "landing": {
            "label": "Southern landing probability",
            "recordCount": len(southern_items),
            "values": gaussian_surface(fallback_landing_points, landing_cells, sigma_lng=5.2, sigma_lat=4.5, max_lat=NGULIA_COORDS["latitude"]),
        },
        "movementSuitability": {
            "label": "Broad north-south corridor prior",
            "values": corridor_surface(cells),
        },
    }


def build_publications() -> dict[str, object]:
    entries = parse_reference_entries(REFERENCES_PATH.read_text(encoding="utf-8"))
    main_review = next((entry for entry in entries if re.search(r"overview and update", entry["title"], re.I)), None)

    highlights = []
    if main_review:
        highlights.append(
            {
                "displayTitle": "Main review",
                "title": main_review["title"],
                "authors": main_review["authors"],
                "year": main_review["year"],
                "journal": main_review["journal"],
                "volume": main_review["volume"],
                "issue": main_review["issue"],
                "pages": main_review["pages"],
                "doi": main_review["doi"],
                "url": main_review["url"]
                or "https://www.researchgate.net/publication/320858776_The_study_and_ringing_of_Palaearctic_birds_at_Ngulia_Lodge_Tsavo_West_National_Park_Kenya_1969-2012_An_overview_and_update",
                "kind": "Main review",
                "description": "The central Ngulia review paper, highlighted here because it brings together the long-term ringing record, species patterns, recoveries, and broader scientific value of the project in a single reference source up to 2012.",
                "openAccess": True,
                "isPdf": False,
                "embedUrl": "",
            }
        )

    highlights.append(
        {
            "displayTitle": "David Pearson presentation",
            "title": "David Pearson presentation",
            "authors": "David Pearson",
            "year": "",
            "journal": "YouTube presentation",
            "volume": "",
            "issue": "",
            "pages": "",
            "doi": "",
            "url": "https://youtu.be/3o5bN61VKLc",
            "kind": "Presentation",
            "description": "A long-form talk by David Pearson on the discovery of the Ngulia phenomenon, how the fieldwork developed, and what the ringing records have revealed.",
            "openAccess": True,
            "isPdf": False,
            "embedUrl": publication_embed_url("https://youtu.be/3o5bN61VKLc"),
        }
    )

    return {"highlights": highlights, "entries": entries}


def merge_species_extras(species_explorer: list[dict[str, object]], recoveries_by_species_id: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    merged = []
    for species in species_explorer:
        merged.append({**species, "recoveries": recoveries_by_species_id.get(species["id"], [])})
    return merged


def main() -> None:
    ensure_dir(OUTPUT_DIR)
    ensure_dir(OUTPUT_PHOTOS_DIR)
    ensure_dir(OUTPUT_SPECIES_RANGES_DIR)

    taxonomy = load_taxonomy_crosswalk(TAXONOMY_CROSSWALK_PATH)
    species_list, dashboard = build_ringing_data(taxonomy)
    recoveries = build_recoveries(taxonomy)
    migration_probabilities = build_migration_probabilities(recoveries)
    publications = build_publications()
    species_ranges = build_species_ranges(species_list)

    dashboard["summary"]["totalRecoveries"] = recoveries["summary"]["totalRecoveries"]
    dashboard["summary"]["recoveryCountries"] = recoveries["summary"]["totalCountries"]
    dashboard["speciesExplorer"] = merge_species_extras(species_list, recoveries["bySpeciesId"])

    write_json("dashboard.json", dashboard)
    write_json("recoveries.json", recoveries)
    write_json("species-ranges-index.json", species_ranges)
    write_json_compact("migration-probabilities.json", migration_probabilities)
    write_json("publications.json", publications)

    print(
        json.dumps(
            {
                "dashboardSpecies": len(dashboard["speciesExplorer"]),
                "recoveries": recoveries["summary"]["totalRecoveries"],
                "speciesRanges": species_ranges["summary"]["availableSpecies"],
                "migrationGridCells": MIGRATION_GRID["width"] * MIGRATION_GRID["height"],
                "publications": len(publications["entries"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
