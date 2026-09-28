"""Build website resources from the latest Zenodo dataset or a local Zenodo export."""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "public" / "generated"
SOURCE_DIR = ROOT_DIR / "data" / "zenodo"
DATA_FILES = ["taxonomy.csv", "daily_counts.csv", "daily_coverage.csv", "ring_events.csv", "recoveries.csv", "README.md", "DATA_DICTIONARY.md"]
NGULIA = {"latitude": -3.0140288001023605, "longitude": 38.211134674309974}
BOUNDS = {"west": -12, "south": -35, "east": 78, "north": 62}
GRID = {"width": 90, "height": 96}
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


def load_env_file(path: Path) -> None:
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            text = line.strip()
            if text and not text.startswith("#") and "=" in text:
                key, value = text.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def read_json_url(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def write_json(data: object, path: Path, compact: bool = False) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, allow_nan=False, indent=None if compact else 2) + "\n", encoding="utf-8")


def read_csv(name: str) -> list[dict]:
    with (SOURCE_DIR / name).open(encoding="utf-8-sig", newline="") as stream:
        return [{key: value.strip() for key, value in row.items()} for row in csv.DictReader(stream)]


# Keep a complete local copy of the dataset, separate from the public website assets.
def acquire_source(local_dir: str | None, record_id: str | None) -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    if local_dir:
        for name in DATA_FILES:
            shutil.copyfile(Path(local_dir).expanduser() / name, SOURCE_DIR / name)
        write_json({"source": "local-export", "path": str(Path(local_dir).expanduser().resolve())}, SOURCE_DIR / "source.json")
    else:
        if not record_id:
            raise RuntimeError("Set NGULIA_ZENODO_RECORD_ID to the published record ID, or use --source-dir with a local Zenodo export.")
        record = read_json_url(f"https://zenodo.org/api/records/{record_id}")
        record = read_json_url(record["links"]["latest"])
        files = {entry["key"]: entry for entry in record["files"]}
        for name in DATA_FILES:
            print(f"Downloading {name}", flush=True)
            with urllib.request.urlopen(files[name]["links"]["self"], timeout=120) as response, (SOURCE_DIR / name).open("wb") as stream:
                shutil.copyfileobj(response, stream)
        write_json({"source": "zenodo", "record_id": record["id"], "doi": record["doi"], "url": record["links"]["self_html"]}, SOURCE_DIR / "source.json")
    print(f"Dataset copy: {SOURCE_DIR}", flush=True)


def species_metadata(row: dict) -> dict:
    species_id = row["avibase_id"]
    code, birdlife, kbt = row["species_code"], row["birdlife_id"], row["kbt_seq"]
    abap = [value.strip() for value in row["abap_ids"].split(";") if value.strip()]
    return {
        "id": species_id, "afringNumber": row["afring_numbers"],
        "name": row["common_name"], "latin": row["scientific_name"],
        "code": row["ngulia_latin_abbr"] or code, "nguliaCode": row["ngulia_numbers"],
        "birdlifeId": birdlife, "cornellSpeciesCode": code, "kbtSeq": kbt,
        "abapIds": abap, "includeRecovery": bool(birdlife), "rawLabels": [row["common_name"]],
        "links": {
            "birdsOfTheWorld": f"https://birdsoftheworld.org/bow/species/{code}" if code else "",
            "eBird": f"https://ebird.org/species/{code}" if code else "",
            "birdLifeFactsheet": row["birdlife_url"],
            "kenyaBirdTrends": f"https://kenyabirdtrends.co.ke/?mode=Species&species={kbt}" if kbt else "",
            "avibase": f"https://avibase.bsc-eoc.org/species.jsp?avibaseid={species_id.removeprefix('avibase-')}",
            "kbm": [{"id": value, "url": f"https://kenya.birdmap.africa/species/{value}"} for value in abap],
            "safring": [{"id": value, "url": f"https://safring.ringing.africa/species/{value}"} for value in abap],
        },
    }


def date_precision(value: str) -> str:
    if not value:
        return "unknown"
    if "/" in value:
        return "range"
    return {4: "year", 7: "month", 10: "day"}[len(value)]


def distance_km(latitude: float, longitude: float) -> int:
    lat1, lat2 = math.radians(NGULIA["latitude"]), math.radians(latitude)
    dlat, dlng = lat2 - lat1, math.radians(longitude - NGULIA["longitude"])
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return round(6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


# Recovery dates retain the precision provided by Zenodo; no date imputation.
def build_recoveries(rows: list[dict], taxonomy: dict) -> dict:
    items = []
    for index, row in enumerate(rows, 1):
        species = taxonomy[row["avibase_id"]]
        from_ngulia = row["direction"] == "from_ngulia"
        lat = float(row["other_latitude"]) if row["other_latitude"] else None
        lng = float(row["other_longitude"]) if row["other_longitude"] else None
        ring_date, encounter_date = row["ringing_date"], row["encounter_date_edtf"]
        duration = None
        if date_precision(ring_date) == date_precision(encounter_date) == "day":
            duration = (date.fromisoformat(encounter_date) - date.fromisoformat(ring_date)).days
        items.append({
            "id": f"NGREC-{index:04d}", "status": "ringed" if from_ngulia else "controlled",
            "direction": row["direction"], "encounterType": row["encounter_type"],
            "speciesId": species["id"], "speciesCode": species["code"],
            "speciesName": species["name"], "speciesLatin": species["latin"],
            "ringScheme": row["ring_scheme"], "ringNumber": row["ring_number"],
            "ringDate": ring_date or None, "ringDatePrecision": date_precision(ring_date),
            "ringSite": "Ngulia" if from_ngulia else row["other_site"] or None,
            "ringProvince": "Tsavo West National Park" if from_ngulia else row["other_region"] or None,
            "ringCountry": "Kenya" if from_ngulia else row["other_country"] or None,
            "encounterCondition": row["encounter_condition"] or None,
            "mortalityCauseClass": row["mortality_cause_class"] or None,
            "recoverDate": encounter_date or None, "recoverDatePrecision": date_precision(encounter_date),
            "reportDate": row["report_date"] or None,
            "recoverySite": row["other_site"] or None if from_ngulia else "Ngulia",
            "recoveryProvince": row["other_region"] or None if from_ngulia else "Tsavo West National Park",
            "recoveryCountry": row["other_country"] or None if from_ngulia else "Kenya",
            "recoverSite": row["other_site"] or None, "recoverProvince": row["other_region"] or None,
            "recoverCountry": row["other_country"] or None,
            "latitude": lat, "longitude": lng,
            "coordinateSource": "zenodo" if lat is not None and lng is not None else "unknown",
            "durationDays": duration, "distanceKm": distance_km(lat, lng) if lat is not None and lng is not None else None,
            "curationNotes": row["curation_notes"] or None,
        })
    countries = sorted({item["recoverCountry"] for item in items if item["recoverCountry"]})
    located = [item for item in items if item["distanceKm"] is not None]
    farthest = max(located, key=lambda item: item["distanceKm"]) if located else None
    by_species = defaultdict(list)
    for item in items:
        by_species[item["speciesId"]].append(item)
    return {
        "summary": {"totalRecoveries": len(items), "totalCountries": len(countries), "countries": countries,
                    "farthestRecovery": {"speciesName": farthest["speciesName"], "country": farthest["recoverCountry"], "distanceKm": farthest["distanceKm"]} if farthest else None},
        "items": items, "bySpeciesId": dict(by_species),
    }


def phenology_rows(counts: Counter, years: dict) -> list[dict]:
    return [{"dayOfYear": (date.fromisoformat(f"2001-{label}") - date(2001, 1, 1)).days + 1,
             "label": label, "count": counts[label], "effortYears": len(years[label])} for label in sorted(counts)]


def build_dashboard(rows: list[dict], taxonomy: dict, recoveries: dict) -> dict:
    annual = defaultdict(Counter)
    phenology = defaultdict(Counter)
    phenology_years = defaultdict(lambda: defaultdict(set))
    yearly_species = defaultdict(set)
    total_phenology = Counter()
    total_years = defaultdict(set)
    for row in rows:
        count = int(row["n_records"])
        if count <= 0:
            continue
        species_id, year = row["avibase_id"], int(row["season"])
        annual[species_id][year] += count
        yearly_species[year].add(species_id)
        if row["ringing_date"]:
            label = row["ringing_date"][5:10]
            phenology[species_id][label] += count
            phenology_years[species_id][label].add(year)
            total_phenology[label] += count
            total_years[label].add(year)
    species_list = []
    for species_id in sorted(annual, key=lambda key: (-sum(annual[key].values()), key)):
        photo = f"./species-photos/{species_id}.jpg"
        species_list.append({
            **taxonomy[species_id], "total": sum(annual[species_id].values()),
            "annual": [{"year": year, "count": count} for year, count in sorted(annual[species_id].items())],
            "phenology": phenology_rows(phenology[species_id], phenology_years[species_id]),
            "photo": photo if (ROOT_DIR / "public" / photo).exists() else None,
            "recoveries": recoveries["bySpeciesId"].get(species_id, []),
        })
    yearly = [{"year": year, "totalRings": sum(annual[key][year] for key in yearly_species[year]),
               "totalSpecies": len(yearly_species[year])} for year in sorted(yearly_species)]
    return {
        "summary": {"totalBirds": sum(species["total"] for species in species_list), "totalSpecies": len(species_list),
                    "yearStart": yearly[0]["year"], "yearEnd": yearly[-1]["year"],
                    "totalRecoveries": recoveries["summary"]["totalRecoveries"], "recoveryCountries": recoveries["summary"]["totalCountries"]},
        "yearly": yearly, "phenology": phenology_rows(total_phenology, total_years),
        "topSpecies": [{key: species[key] for key in ("id", "name", "latin", "code", "links", "total", "photo")} for species in species_list[:15]],
        "speciesExplorer": species_list,
    }


def build_ranges(species_list: list[dict]) -> dict:
    existing = json.loads((ROOT_DIR / "scripts" / "species_ranges.json").read_text(encoding="utf-8"))
    species = {}
    for item in species_list:
        meta = {key: item[key] for key in ("id", "name", "latin", "birdlifeId")}
        static = existing["species"].get(item["id"], {})
        if static.get("path") and (OUTPUT_DIR / static["path"]).exists():
            meta.update({key: static[key] for key in ("path", "rangeTypes", "featureCount", "birdlifeScientificName", "birdlifeCommonName") if key in static})
            meta["available"] = True
        else:
            meta.update(available=False, missingReason="not-exported")
        species[item["id"]] = meta
    available = sum(item["available"] for item in species.values())
    return {"metadata": existing["metadata"], "summary": {"totalSpecies": len(species), "matchedSpecies": available, "availableSpecies": available}, "species": species}


# Preserve the home-page prototype's coarse land mask and density parameters.
def point_in_polygon(lng: float, lat: float, polygon: list) -> bool:
    inside = False
    xj, yj = polygon[-1]
    for xi, yi in polygon:
        if (yi > lat) != (yj > lat) and lng < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        xj, yj = xi, yi
    return inside


def is_land(lng: float, lat: float) -> bool:
    return any(point_in_polygon(lng, lat, polygon) for polygon in LAND_POLYGONS) and not any(point_in_polygon(lng, lat, polygon) for polygon in WATER_HOLES)


def normalize_surface(values: list[float]) -> list[float]:
    total = sum(values)
    return [round(value / total, 9) for value in values] if total else values


def gaussian_surface(points: list, cells: list, northern: bool) -> list[float]:
    values = []
    for lng, lat, land in cells:
        eligible = lat > NGULIA["latitude"] if northern else lat <= NGULIA["latitude"] and not (lat < NGULIA["latitude"] and lng > 37.5)
        values.append(sum(math.exp(-0.5 * (((lng - point["longitude"]) / 5.2) ** 2 + ((lat - point["latitude"]) / 4.5) ** 2)) for point in points) if land and eligible else 0)
    return normalize_surface(values)


def build_migration(items: list[dict]) -> dict:
    cells = []
    for y in range(GRID["height"]):
        for x in range(GRID["width"]):
            lng = BOUNDS["west"] + (x + 0.5) * (BOUNDS["east"] - BOUNDS["west"]) / GRID["width"]
            lat = BOUNDS["south"] + (y + 0.5) * (BOUNDS["north"] - BOUNDS["south"]) / GRID["height"]
            cells.append((lng, lat, is_land(lng, lat)))
    points = [item for item in items if item["coordinateSource"] != "unknown" and -35 <= item["latitude"] <= 62 and -12 <= item["longitude"] <= 78 and abs(item["latitude"] - NGULIA["latitude"]) > 500 / 111.32]
    north = [item for item in points if item["latitude"] > NGULIA["latitude"]]
    south = [item for item in points if item["latitude"] < NGULIA["latitude"]]
    departure = [item for item in north if is_land(item["longitude"], item["latitude"])] or [{"latitude": 42, "longitude": 42}]
    landing = [item for item in south if is_land(item["longitude"], item["latitude"])] or [{"latitude": -15, "longitude": 35}]
    corridor = [math.exp(-0.5 * ((lng - (NGULIA["longitude"] + 0.12 * (lat - NGULIA["latitude"]))) / 8.5) ** 2) * (0.35 + 0.65 * math.exp(-0.5 * ((lng - NGULIA["longitude"]) / 18) ** 2)) if land else 0 for lng, lat, land in cells]
    return {
        "metadata": {
            "description": "Browser-sampled migration probability grids for the Ngulia home-page deck.gl prototype.",
            "crs": "EPSG:4326", "site": {"name": "Ngulia", **NGULIA},
            "normalization": "Each values array sums to one and can be sampled as a discrete probability distribution.",
            "source": "Departure densities are smoothed from recoveries north of Ngulia; landing densities are smoothed from recoveries south of Ngulia.",
            "landMask": "Coarse in-script land polygons with broad water holes for rapid prototype iteration.", "exclusionBandKm": 500,
        },
        "bounds": BOUNDS, "grid": GRID, "landMask": [land for lng, lat, land in cells],
        "departure": {"label": "Northern departure probability", "recordCount": len(north), "values": gaussian_surface(departure, cells, northern=True)},
        "landing": {"label": "Southern landing probability", "recordCount": len(south), "values": gaussian_surface(landing, cells, northern=False)},
        "movementSuitability": {"label": "Broad north-south corridor prior", "values": normalize_surface(corridor)},
    }


def main() -> None:
    load_env_file(ROOT_DIR / ".env.pipeline.local")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=os.getenv("NGULIA_ZENODO_SOURCE_DIR"), help="Use a local Zenodo export instead of downloading")
    parser.add_argument("--record-id", default=os.getenv("NGULIA_ZENODO_RECORD_ID"), help="Published Zenodo record ID; always resolves to the latest version")
    args = parser.parse_args()
    acquire_source(args.source_dir, args.record_id)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    taxonomy = {row["avibase_id"]: species_metadata(row) for row in read_csv("taxonomy.csv")}
    recoveries = build_recoveries(read_csv("recoveries.csv"), taxonomy)
    dashboard = build_dashboard(read_csv("daily_counts.csv"), taxonomy, recoveries)
    write_json(dashboard, OUTPUT_DIR / "dashboard.json")
    write_json(recoveries, OUTPUT_DIR / "recoveries.json")
    write_json(build_ranges(dashboard["speciesExplorer"]), OUTPUT_DIR / "species-ranges-index.json")
    write_json(build_migration(recoveries["items"]), OUTPUT_DIR / "migration-probabilities.json", compact=True)
    print(f"Generated {len(dashboard['speciesExplorer'])} species and {len(recoveries['items'])} recoveries in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
