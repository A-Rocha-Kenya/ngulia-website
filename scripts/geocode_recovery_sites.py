from __future__ import annotations

import argparse
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import xlrd


ROOT_DIR = Path(__file__).resolve().parent.parent
PIPELINE_ENV_PATH = ROOT_DIR / ".env.pipeline.local"
DEFAULT_OVERRIDES_PATH = ROOT_DIR / "scripts" / "recovery_site_coordinates.json"
DEFAULT_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def normalize(value: object) -> str:
    text = str(value or "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).strip().lower()
    return text


def clean_text(value: object) -> str:
    return str(value or "").strip()


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
RECOVERIES_PATH = SOURCE_DATA_DIR / "Data - management and analysis" / "05 Recoveries" / "0709 Ngulia Recoveries and Controls.xls"


def override_key(site: object, province: object, country: object) -> str:
    return f"{normalize(site)}|{normalize(province)}|{normalize(country)}"


def load_overrides(path: Path) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    if not path.exists():
        return {"overrides": {}}, {}

    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "overrides" in payload and isinstance(payload["overrides"], dict):
        return payload, payload["overrides"]
    if isinstance(payload, dict):
        wrapped = {"overrides": payload}
        return wrapped, wrapped["overrides"]
    return {"overrides": {}}, {}


def save_overrides(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def is_success(entry: dict[str, object]) -> bool:
    if not isinstance(entry, dict):
        return False
    lat = entry.get("latitude")
    lon = entry.get("longitude")
    return isinstance(lat, (int, float)) and isinstance(lon, (int, float)) and not entry.get("error")


def location_queries(site: str, province: str, country: str) -> list[str]:
    queries = [
        ", ".join([part for part in [site, province, country] if part]),
        ", ".join([part for part in [site, country] if part]),
        ", ".join([part for part in [province, country] if part]),
        country,
    ]
    return [query for index, query in enumerate(queries) if query and query not in queries[:index]]


def geocode_google(query: str, api_key: str, api_url: str) -> dict[str, object]:
    params = urllib.parse.urlencode({"address": query, "key": api_key})
    request = urllib.request.Request(f"{api_url}?{params}")
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    status = payload.get("status")
    if status != "OK":
        return {"status": status, "result": None, "error_message": payload.get("error_message", "")}

    result = (payload.get("results") or [None])[0]
    return {"status": status, "result": result, "error_message": ""}


def extract_non_ngulia_locations() -> dict[str, dict[str, str]]:
    workbook = xlrd.open_workbook(RECOVERIES_PATH)
    sheet = workbook.sheet_by_index(0)
    rows = [sheet.row_values(i) for i in range(sheet.nrows)]

    section_status = ""
    locations: dict[str, dict[str, str]] = {}

    for row in rows:
        section_label = normalize(row[0])
        if section_label == "ringed at ngulia":
            section_status = "ringed"
            continue
        if section_label == "controlled at ngulia":
            section_status = "controlled"
            continue

        species_code = clean_text(row[0])
        if species_code == "SPECIES" or not re.match(r"^[A-Z]{5,7}$", species_code):
            continue

        if section_status == "controlled":
            site = clean_text(row[4])
            province = clean_text(row[5])
            country = clean_text(row[6])
        else:
            site = clean_text(row[15])
            province = clean_text(row[16])
            country = clean_text(row[17])

        if not country:
            continue

        key = override_key(site, province, country)
        if key not in locations:
            locations[key] = {"site": site, "province": province, "country": country}

    return locations


def main() -> None:
    parser = argparse.ArgumentParser(description="Build recovery site coordinates from Google Geocoding API.")
    parser.add_argument("--api-key", default=os.getenv("GOOGLE_MAPS_API_KEY", ""), help="Google Geocoding API key. Falls back to GOOGLE_MAPS_API_KEY.")
    parser.add_argument("--overrides-file", type=Path, default=DEFAULT_OVERRIDES_PATH, help="JSON recovery site coordinate file to read and update.")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="Geocoding API URL.")
    parser.add_argument("--force", action="store_true", help="Re-query entries even when they already have successful coordinates.")
    parser.add_argument("--force-locked", action="store_true", help="Also overwrite entries marked with locked=true.")
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of locations to query in this run (0 = no limit).")
    parser.add_argument("--sleep-seconds", type=float, default=0.15, help="Delay between API requests.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned queries without calling the API or writing output.")
    args = parser.parse_args()

    if not args.dry_run and not args.api_key:
        raise SystemExit("Missing API key. Pass --api-key or set GOOGLE_MAPS_API_KEY.")

    payload, overrides = load_overrides(args.overrides_file)
    locations = extract_non_ngulia_locations()
    keys = sorted(locations.keys())

    stats = {"skipped_existing": 0, "skipped_locked": 0, "requested": 0, "success": 0, "failed": 0}
    scheduled = 0

    for key in keys:
        location = locations[key]
        existing = overrides.get(key, {})
        locked = bool(existing.get("locked")) if isinstance(existing, dict) else False

        if locked and not args.force_locked:
            stats["skipped_locked"] += 1
            continue
        if is_success(existing) and not args.force:
            stats["skipped_existing"] += 1
            continue
        if args.limit and scheduled >= args.limit:
            break
        scheduled += 1

        queries = location_queries(location["site"], location["province"], location["country"])
        if args.dry_run:
            print(f"[dry-run] {key}: {queries[0] if queries else '(no query)'}")
            continue

        stats["requested"] += 1
        resolved = None
        last_status = ""
        last_error = ""
        used_query = ""

        for query in queries:
            try:
                response = geocode_google(query, args.api_key, args.api_url)
            except urllib.error.HTTPError as exc:
                response = {"status": "HTTP_ERROR", "result": None, "error_message": str(exc)}
            except urllib.error.URLError as exc:
                response = {"status": "URL_ERROR", "result": None, "error_message": str(exc)}
            except TimeoutError as exc:
                response = {"status": "TIMEOUT", "result": None, "error_message": str(exc)}

            last_status = str(response.get("status") or "")
            last_error = str(response.get("error_message") or "")

            if response.get("status") == "OK" and response.get("result"):
                resolved = response["result"]
                used_query = query
                break

            time.sleep(args.sleep_seconds)

        next_entry = dict(existing) if isinstance(existing, dict) else {}
        next_entry.update(location)
        next_entry["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        next_entry["query"] = used_query or (queries[0] if queries else "")
        next_entry["geocoder"] = "google-geocoding"

        if resolved:
            geometry = resolved.get("geometry", {})
            geo_loc = geometry.get("location", {})
            next_entry["latitude"] = float(geo_loc["lat"])
            next_entry["longitude"] = float(geo_loc["lng"])
            next_entry["locationType"] = geometry.get("location_type", "")
            next_entry["formattedAddress"] = resolved.get("formatted_address", "")
            next_entry["placeId"] = resolved.get("place_id", "")
            next_entry["source"] = "site-override-google"
            next_entry["status"] = "success"
            next_entry["error"] = ""
            stats["success"] += 1
        else:
            next_entry["status"] = last_status or "ZERO_RESULTS"
            next_entry["error"] = last_error
            if "latitude" not in next_entry:
                next_entry["latitude"] = None
                next_entry["longitude"] = None
            stats["failed"] += 1

        overrides[key] = next_entry
        time.sleep(args.sleep_seconds)

    payload["overrides"] = dict(sorted(overrides.items()))

    if not args.dry_run:
        payload["meta"] = {
            "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "totalLocations": len(locations),
            "note": "You can manually edit entries and set locked=true to prevent updates.",
        }
        save_overrides(args.overrides_file, payload)

    print(
        json.dumps(
            {
                "totalLocations": len(locations),
                "requested": stats["requested"],
                "success": stats["success"],
                "failed": stats["failed"],
                "skippedExisting": stats["skipped_existing"],
                "skippedLocked": stats["skipped_locked"],
                "overridesFile": str(args.overrides_file),
                "dryRun": args.dry_run,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
